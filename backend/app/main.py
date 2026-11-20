import sqlite3, hashlib, secrets, re, os, base64
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from app.settings import settings

app=FastAPI(title="Chat.com",version="0.3.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
ROOT=Path(__file__).resolve().parents[2]; FRONT=ROOT/"index.html"
DB=Path(os.environ.get("CHAT_DATABASE_PATH",str(Path(__file__).resolve().parents[1]/"data"/"chat_com_preview.db")))
def db():
 DB.parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def now():return datetime.now(timezone.utc).isoformat()
def init():
 with db() as c:c.executescript("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL,created_at TEXT NOT NULL);CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id INTEGER NOT NULL,created_at TEXT NOT NULL);CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY,sender_id INTEGER NOT NULL,receiver_id INTEGER NOT NULL,text TEXT NOT NULL,media_data TEXT,media_type TEXT,created_at TEXT NOT NULL);""")
@app.on_event("startup")
def startup():init()
class Credentials(BaseModel):
 username:str=Field(min_length=3,max_length=24)
 password:str=Field(min_length=8,max_length=128)
class Message(BaseModel):
 to:str=Field(min_length=1,max_length=24)
 text:str=Field(default="",max_length=4000)
 media_data:str|None=None
 media_type:str|None=None
def pw(p,s):return hashlib.pbkdf2_hmac("sha256",p.encode(),s.encode(),180000).hex()
def auth(authorization:str|None=Header(default=None)):
 if not authorization or not authorization.startswith("Bearer "):raise HTTPException(401,"Please sign in")
 with db() as c:r=c.execute("SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token=?",(authorization[7:],)).fetchone()
 if not r:raise HTTPException(401,"Session invalid")
 return r
@app.get("/",include_in_schema=False)
def home():
 if not FRONT.exists():raise HTTPException(404,"index.html missing")
 return FileResponse(FRONT)
@app.get("/health")
def health():return {"status":"healthy","service":"chat-com","version":"0.3.0"}
@app.post("/api/v1/auth/register")
def register(a:Credentials):
 u=a.username.lower()
 if not re.fullmatch(r"[a-z0-9_.]{3,24}",u):raise HTTPException(400,"Username must be 3–24 letters, digits, . or _")
 salt=secrets.token_hex(16); token=secrets.token_urlsafe(32)
 with db() as c:
  try:uid=c.execute("INSERT INTO users(username,password_hash,created_at) VALUES(?,?,?)",(u,salt+":"+pw(a.password,salt),now())).lastrowid
  except sqlite3.IntegrityError:raise HTTPException(409,"Username already taken")
  c.execute("INSERT INTO sessions(token,user_id,created_at) VALUES(?,?,?)",(token,uid,now()))
 return {"token":token,"username":u}
@app.post("/api/v1/auth/login")
def login(a:Credentials):
 with db() as c:r=c.execute("SELECT * FROM users WHERE username=?",(a.username.lower(),)).fetchone()
 if not r:raise HTTPException(401,"Incorrect username or password")
 salt,stored=r["password_hash"].split(":",1)
 if not secrets.compare_digest(pw(a.password,salt),stored):raise HTTPException(401,"Incorrect username or password")
 token=secrets.token_urlsafe(32)
 with db() as c:c.execute("INSERT INTO sessions(token,user_id,created_at) VALUES(?,?,?)",(token,r["id"],now()))
 return {"token":token,"username":r["username"]}
@app.post("/api/v1/auth/logout")
def logout(u=Depends(auth),authorization:str|None=Header(default=None)):
 with db() as c:c.execute("DELETE FROM sessions WHERE token=?",(authorization[7:],))
 return {"ok":True}
@app.get("/api/v1/me")
def me(u=Depends(auth)):return {"username":u["username"]}
@app.get("/api/v1/users/{username}")
def lookup(username:str,u=Depends(auth)):
 with db() as c:r=c.execute("SELECT username FROM users WHERE username=?",(username.lower(),)).fetchone()
 if not r or r["username"]==u["username"]:raise HTTPException(404,"User not found")
 return dict(r)
@app.get("/api/v1/contacts")
def contacts(u=Depends(auth)):
 with db() as c:r=c.execute("SELECT DISTINCT p.username FROM messages m JOIN users p ON p.id=CASE WHEN m.sender_id=? THEN m.receiver_id ELSE m.sender_id END WHERE m.sender_id=? OR m.receiver_id=? ORDER BY p.username",(u["id"],u["id"],u["id"])).fetchall()
 return {"users":[x["username"] for x in r]}
@app.get("/api/v1/messages/{username}")
def get_messages(username:str,u=Depends(auth)):
 with db() as c:
  t=c.execute("SELECT id FROM users WHERE username=?",(username.lower(),)).fetchone()
  if not t:raise HTTPException(404,"User not found")
  r=c.execute("SELECT m.id,m.text,m.media_data,m.media_type,m.created_at,s.username sender,r.username receiver FROM messages m JOIN users s ON s.id=m.sender_id JOIN users r ON r.id=m.receiver_id WHERE (m.sender_id=? AND m.receiver_id=?) OR (m.sender_id=? AND m.receiver_id=?) ORDER BY m.id LIMIT 300",(u["id"],t["id"],t["id"],u["id"])).fetchall()
 return {"messages":[dict(x) for x in r]}
@app.post("/api/v1/messages",status_code=201)
def send(m:Message,u=Depends(auth)):
 if not m.text.strip() and not m.media_data:raise HTTPException(400,"Empty message")
 if m.media_data and len(m.media_data)>7000000:raise HTTPException(413,"Image too large (max ~5 MB)")
 if m.media_data and m.media_type not in ("image/jpeg","image/png","image/webp","image/gif"):raise HTTPException(400,"Unsupported image type")
 with db() as c:
  t=c.execute("SELECT id FROM users WHERE username=?",(m.to.lower(),)).fetchone()
  if not t:raise HTTPException(404,"User not found")
  mid=c.execute("INSERT INTO messages(sender_id,receiver_id,text,media_data,media_type,created_at) VALUES(?,?,?,?,?,?)",(u["id"],t["id"],m.text.strip(),m.media_data,m.media_type,now())).lastrowid
  r=c.execute("SELECT m.id,m.text,m.media_data,m.media_type,m.created_at,s.username sender,r.username receiver FROM messages m JOIN users s ON s.id=m.sender_id JOIN users r ON r.id=m.receiver_id WHERE m.id=?",(mid,)).fetchone()
 return dict(r)

package com.chatcom.exhibition;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.widget.Toast;
import android.webkit.ValueCallback;
import android.content.Intent;
import android.net.Uri;

public class MainActivity extends Activity {
    WebView web;
    ValueCallback<Uri[]> uploadCallback;
    static final int FILE_CHOOSER=100;
    @Override public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        web=new WebView(this); setContentView(web);
        WebSettings s=web.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(true); s.setAllowContentAccess(true);
        web.setWebViewClient(new WebViewClient()); web.setWebChromeClient(new WebChromeClient(){
            @Override public boolean onShowFileChooser(WebView w,ValueCallback<Uri[]> cb,FileChooserParams p){
                if(uploadCallback!=null)uploadCallback.onReceiveValue(null); uploadCallback=cb;
                Intent i=p.createIntent(); try{startActivityForResult(i,FILE_CHOOSER);}catch(Exception e){uploadCallback=null;Toast.makeText(MainActivity.this,"Unable to open gallery",Toast.LENGTH_SHORT).show();return false;} return true;
            }
        });
        web.loadUrl("https://chat-com-username-messaging.onrender.com/");
    }
    @Override protected void onActivityResult(int req,int res,Intent data){super.onActivityResult(req,res,data);if(req==FILE_CHOOSER&&uploadCallback!=null){Uri u=(res==RESULT_OK&&data!=null)?data.getData():null;uploadCallback.onReceiveValue(u==null?null:new Uri[]{u});uploadCallback=null;}}
    @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else super.onBackPressed();}
}

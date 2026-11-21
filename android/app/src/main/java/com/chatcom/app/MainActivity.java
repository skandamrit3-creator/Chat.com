package com.chatcom.app;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.*;
import android.content.Intent;
import android.net.Uri;
import android.widget.Toast;

public class MainActivity extends Activity {
  private WebView web;
  private ValueCallback<Uri[]> uploadCallback;
  private static final int FILE_PICKER = 100;
  @Override public void onCreate(Bundle saved) {
    super.onCreate(saved);
    web = new WebView(this);
    web.getSettings().setJavaScriptEnabled(true);
    web.getSettings().setDomStorageEnabled(true);
    web.getSettings().setAllowFileAccess(false);
    web.getSettings().setAllowContentAccess(true);
    web.setWebViewClient(new WebViewClient());
    web.setWebChromeClient(new WebChromeClient(){
      @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params){
        if(uploadCallback!=null) uploadCallback.onReceiveValue(null);
        uploadCallback=callback;
        Intent intent=new Intent(Intent.ACTION_GET_CONTENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("*/*");
        intent.putExtra(Intent.EXTRA_MIME_TYPES,new String[]{"image/*","video/mp4","video/webm","video/quicktime"});
        try { startActivityForResult(Intent.createChooser(intent,"Select media"),FILE_PICKER); }
        catch(Exception e){uploadCallback=null;return false;}
        return true;
      }
    });
    setContentView(web);
    web.loadUrl("https://chat-com-text-only-preview.onrender.com/");
  }
  @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){
    super.onActivityResult(requestCode,resultCode,data);
    if(requestCode==FILE_PICKER && uploadCallback!=null){
      Uri uri=(resultCode==RESULT_OK && data!=null)?data.getData():null;
      uploadCallback.onReceiveValue(uri==null?null:new Uri[]{uri});uploadCallback=null;
    }
  }
  @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else super.onBackPressed();}
}

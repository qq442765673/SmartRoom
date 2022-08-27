package com.example.smarthouse;

import static android.content.ContentValues.TAG;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.content.Intent;
import android.widget.TextView;



import java.text.SimpleDateFormat;


public class MainActivity extends AppCompatActivity {

    public static final String EXTRA_MESSAGE = "com.example.myfirstapp.MESSAGE";
    private String API_KEY = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk";
    private String tempVarId = "62c623211d847242bc769a5c";
    private String humVarId = "62c623201d84724415174167";
    private String LightId = "62cc42c61d8472033ed773af";
    private String MotionId = "62cc43441d8472031ec566c1";
    private String LightswtichId = "62edabc81d84720d2adde8e9";
    private String fanswtichId = "62edac161d84720d2978be8c";
    private static final SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
    public String temperature = "0";
    public String Humidity = "0";
    public String Lightsens = "0";
    public Float Motion = 0f;
    public Float Lightswtich = 0f;
    public Float fanswtich = 0f;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        (new UbidotsClient()).handleUbidots(tempVarId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            temperature = String.valueOf(ccc);
        });
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView tempureturetext = (TextView) findViewById(R.id.textView5);
                Log.d("tempure", temperature);
                tempureturetext.setText(temperature);
            }
        }, 2000);


        (new UbidotsClient()).handleUbidots(humVarId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Humidity = String.valueOf(ccc);
        });
        Handler handler1 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Humiditytext = (TextView) findViewById(R.id.textView6);
                Log.d("Humidity", Humidity);
                Humiditytext.setText(Humidity);
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(LightId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Lightsens = String.valueOf(ccc);
        });
        Handler handler2 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Lightsenstext = (TextView) findViewById(R.id.textView7);
                Log.d("Lightsens", Lightsens);
                Lightsenstext.setText(Lightsens);
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(LightswtichId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Lightswtich = ccc;
        });
        Handler handler3 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Lightswtichtext = (TextView) findViewById(R.id.textView8);
                Log.d("Lightswtich", Lightswtich.toString());
                if(Lightswtich==1){
                    Lightswtichtext.setText("on");
                }
                else if (Lightswtich==0){
                    Lightswtichtext.setText("off");
                }
                else {
                    Lightswtichtext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(fanswtichId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            fanswtich = ccc;
        });
        Handler handler4 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView fanswtichtext = (TextView) findViewById(R.id.textView9);
                Log.d("fanswtich", fanswtich.toString());
                if(fanswtich==1){
                    fanswtichtext.setText("on");
                }
                else if (fanswtich==0){
                    fanswtichtext.setText("off");
                }
                else {
                    fanswtichtext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(MotionId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(99).value;
            Motion = ccc;
        });
        Handler handler5 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Motiontext = (TextView) findViewById(R.id.textView11);
                Log.d("Motion", Motion.toString());
                if(Motion==1){
                    Motiontext.setText("Occupied");
                }
                else if (Motion==0){
                    Motiontext.setText("Empty");
                }
                else {
                    Motiontext.setText("error");
                }
            }
        }, 2000);
    }

    public void onCreateView (View view){
        // Inflate the layout for this fragment

        (new UbidotsClient()).handleUbidots(tempVarId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            temperature = String.valueOf(ccc);
        });
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView tempureturetext = (TextView) findViewById(R.id.textView5);
                Log.d("tempure", temperature);
                tempureturetext.setText(temperature);
            }
        }, 2000);


        (new UbidotsClient()).handleUbidots(humVarId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Humidity = String.valueOf(ccc);
        });
        Handler handler1 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Humiditytext = (TextView) findViewById(R.id.textView6);
                Log.d("Humidity", Humidity);
                Humiditytext.setText(Humidity);
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(LightId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Lightsens = String.valueOf(ccc);
        });
        Handler handler2 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Lightsenstext = (TextView) findViewById(R.id.textView7);
                Log.d("Lightsens", Lightsens);
                Lightsenstext.setText(Lightsens);
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(LightswtichId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Lightswtich = ccc;
        });
        Handler handler3 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Lightswtichtext = (TextView) findViewById(R.id.textView8);
                Log.d("Lightswtich", Lightswtich.toString());
                if(Lightswtich==1){
                    Lightswtichtext.setText("on");
                }
                else if (Lightswtich==0){
                    Lightswtichtext.setText("off");
                }
                else {
                    Lightswtichtext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(fanswtichId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            fanswtich = ccc;
        });
        Handler handler4 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView fanswtichtext = (TextView) findViewById(R.id.textView9);
                Log.d("fanswtich", fanswtich.toString());
                if(fanswtich==1){
                    fanswtichtext.setText("on");
                }
                else if (fanswtich==0){
                    fanswtichtext.setText("off");
                }
                else {
                    fanswtichtext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(MotionId, API_KEY, result -> {
            Log.d("Chart", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Motion = ccc;
        });
        Handler handler5 = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Motiontext = (TextView) findViewById(R.id.textView11);
                Log.d("Motion", Motion.toString());
                if(Motion==1){
                    Motiontext.setText("Occupied");
                }
                else if (Motion==0){
                    Motiontext.setText("Empty");
                }
                else {
                    Motiontext.setText("error");
                }
            }
        }, 2000);

    }

    public void lighswitch (View view)
        {
            TextView Lightswtichtext = (TextView) findViewById(R.id.textView8);
            Lightswitch lightswtich1= new  Lightswitch();
            Log.d(TAG, "Lightswtichtext: " +Lightswtichtext.getText());
            if (Lightswtichtext.getText()=="on")
            {lightswtich1.switchoff(this);}
            else {
                lightswtich1.switchon(this);
            }


    }
    public void fanswitch (View view)
    {
        TextView fanswtichtext = (TextView) findViewById(R.id.textView9);
        Fanswitch fanswtich1= new  Fanswitch();
        Log.d(TAG, "fanswtichtext: " +fanswtichtext.getText());
        if (fanswtichtext.getText()=="on")
        {fanswtich1.switchoff(this);}
        else {
            fanswtich1.switchon(this);
        }


    }
    public void AutoLight (View view)
    {
        TextView Lightswtichtext = (TextView) findViewById(R.id.textView18);
        Lightswitch lightswtich1= new  Lightswitch();
        Log.d(TAG, "Lightswtichtext: " +Lightswtichtext.getText());
        if (Lightswtichtext.getText()=="on")
        {lightswtich1.switchoff(this);}
        else {
            lightswtich1.switchon(this);
        }


    } public void Autofan (View view)
    {
        TextView Lightswtichtext = (TextView) findViewById(R.id.textView8);
        Lightswitch lightswtich1= new  Lightswitch();
        Log.d(TAG, "Lightswtichtext: " +Lightswtichtext.getText());
        if (Lightswtichtext.getText()=="on")
        {lightswtich1.switchoff(this);}
        else {
            lightswtich1.switchon(this);
        }


    }
    public void SetRules(View view) {
        Intent intent = new Intent(this, Set_Rules.class);
        TextView textView = (TextView) findViewById(R.id.hw);
        String message = textView.getText().toString();
        intent.putExtra(EXTRA_MESSAGE, message);
        startActivity(intent);
    }


}
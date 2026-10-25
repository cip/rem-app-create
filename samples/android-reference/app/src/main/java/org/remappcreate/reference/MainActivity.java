package org.remappcreate.reference;

import android.app.Activity;
import android.os.Bundle;
import android.widget.LinearLayout;
import android.widget.TextView;

public final class MainActivity extends Activity {
    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(32, 48, 32, 32);
        TextView greeting = new TextView(this);
        greeting.setText(MessageFormatter.greeting("REM Android Reference"));
        greeting.setTextSize(22f);
        layout.addView(greeting);
        TextView version = new TextView(this);
        version.setText("Version " + BuildConfig.VERSION_NAME + " (" + BuildConfig.VERSION_CODE + ")");
        version.setTextSize(16f);
        layout.addView(version);
        setContentView(layout);
    }
}

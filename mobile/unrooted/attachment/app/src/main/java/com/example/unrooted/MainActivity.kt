package com.example.unrooted

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val input = findViewById<EditText>(R.id.flagInput)
        val button = findViewById<Button>(R.id.checkButton)
        val result = findViewById<TextView>(R.id.resultText)

        val status = NativeCheck.checkEnvironment(this)
        if (status != 0) {
            result.text = "Environment not clean (0x%x). Refusing to run.".format(status)
            button.isEnabled = false
        }

        button.setOnClickListener {
            result.text = if (FlagChecker.verify(this, input.text.toString())) {
                "Correct! Welcome to the unrooted side :)"
            } else {
                "Wrong flag, try harder."
            }
        }
    }
}

package com.example.myapp

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

        button.setOnClickListener {
            result.text = if (FlagChecker.verify(input.text.toString())) {
                "Correct! You are an Android reverser now :)"
            } else {
                "Wrong flag, try harder."
            }
        }
    }
}

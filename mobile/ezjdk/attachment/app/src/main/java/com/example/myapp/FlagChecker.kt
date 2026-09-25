package com.example.myapp

import android.util.Base64

object FlagChecker {

    private val secret = "LTk+IhASSQYHWwhJNRBbOk4EABlVSw47GVYMWRYYVgc="
    private val mask = "ezjdk"

    fun verify(input: String): Boolean {
        val raw = input.toByteArray(Charsets.UTF_8)
        val enc = ByteArray(raw.size) { i ->
            (raw[i].toInt() xor mask[i % mask.length].code).toByte()
        }
        return Base64.encodeToString(enc, Base64.NO_WRAP) == secret
    }
}

/*
 * unrooted - Frida bypass script
 *
 * Usage:
 *   frida -U -f com.example.unrooted -l bypass.js
 *
 * This only neutralises the native environment check, so the app runs the real
 * flag verification afterwards. Enter the recovered flag to get "Correct!".
 *
 * Only native hooks are used on purpose: the target put its detection logic in
 * libunrooted.so, so the cleanest bypass is to hook the exported JNI function
 * Java_com_example_unrooted_NativeCheck_checkEnvironment and force it to 0.
 */

const LIB = 'libunrooted.so';
const CHECK = 'Java_com_example_unrooted_NativeCheck_checkEnvironment';

let hooked = false;

function hookCheck() {
  const symbol = Module.findExportByName(LIB, CHECK);
  if (symbol === null) {
    return false;
  }
  Interceptor.attach(symbol, {
    onLeave: function (retval) {
      retval.replace(0);
    },
  });
  console.log('[+] hooked ' + LIB + '!' + CHECK + ' -> 0');
  return true;
}

function waitForLibrary() {
  if (hookCheck()) {
    hooked = true;
    return;
  }

  const dlopen = Module.findExportByName(null, 'android_dlopen_ext');
  if (dlopen !== null) {
    Interceptor.attach(dlopen, {
      onEnter: function (args) {
        try {
          this.path = args[0].readCString();
        } catch (e) {
          this.path = null;
        }
      },
      onLeave: function () {
        if (this.path !== null && this.path.indexOf(LIB) !== -1 && hookCheck()) {
          hooked = true;
        }
      },
    });
    console.log('[+] waiting for ' + LIB + ' via android_dlopen_ext');
  }

  const timer = setInterval(function () {
    if (hooked || hookCheck()) {
      hooked = true;
      clearInterval(timer);
    }
  }, 50);
}

setImmediate(waitForLibrary);

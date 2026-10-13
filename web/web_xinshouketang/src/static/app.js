/* CTF 新手课堂：打卡按钮 + 结课五框拼 flag + 键盘翻页 */
function esc(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

/* 我已学会：打卡领奖励 */
var learnBtn = document.getElementById("learn-btn");
if (learnBtn) {
  learnBtn.addEventListener("click", function () {
    var box = document.getElementById("learn-result");
    fetch("/api/learn/" + learnBtn.dataset.lesson, { method: "POST" })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        box.hidden = false;
        var html = esc(d.msg) + ' <code>' + esc(d.flag_part || "") + "</code>";
        if (d.extra) html += "<br>" + esc(d.extra);
        box.innerHTML = html;
        learnBtn.textContent = "已打卡";
        learnBtn.disabled = true;
      })
      .catch(function () {
        box.hidden = false;
        box.textContent = "网络开了点小差，再点一次试试";
      });
  });
}

/* 结课测试：五个框拼出完整 flag（客户端拼接，校验在平台） */
var assembleBtn = document.getElementById("assemble-btn");
if (assembleBtn) {
  var resultBox = document.getElementById("flag-result");
  var flagText = document.getElementById("flag-text");

  assembleBtn.addEventListener("click", function () {
    var vals = [];
    for (var i = 1; i <= 5; i++) {
      var input = document.querySelector('[data-piece="' + i + '"]');
      vals.push(input ? input.value.trim() : "");
    }
    resultBox.hidden = false;
    if (vals.some(function (v) { return !v; })) {
      flagText.textContent = "还有框没填满，五块都要填上";
      return;
    }
    var prefix = assembleBtn.dataset.prefix || "hctf";
    flagText.textContent = prefix + "{" + vals.join("_") + "}";
  });

  var copyBtn = document.getElementById("copy-btn");
  copyBtn.addEventListener("click", function () {
    var text = flagText.textContent;
    if (!text || text.indexOf("{") < 0) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        copyBtn.textContent = "已复制";
      }, function () {
        copyBtn.textContent = "复制失败，手动选";
      });
    } else {
      copyBtn.textContent = "复制失败，手动选";
    }
  });
}

/* 左右方向键翻页 */
var prev = document.querySelector("a.nav-prev");
var next = document.querySelector("a.nav-next");
document.addEventListener("keydown", function (e) {
  var tag = (e.target.tagName || "").toUpperCase();
  if (tag === "INPUT" || tag === "TEXTAREA") return;
  if (e.key === "ArrowLeft" && prev) location.href = prev.href;
  if (e.key === "ArrowRight" && next) location.href = next.href;
});

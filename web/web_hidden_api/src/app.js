/*
 * 内部系统 · 前端逻辑
 * ------------------------------------------------------------------
 * 小课堂：
 * 前端 JavaScript 会完整地发送到浏览器，任何人都能阅读。
 * 千万不要把密钥、口令、后台接口写死在前端里——可惜我们这位
 * "运维同学"显然没听过这句话。
 * ------------------------------------------------------------------
 */

const API_BASE = "/api/v2";

// TODO(运维): 上线前务必删除下面的调试后门！！！
// 备份接口需要一个调试 key。为什么写在前端？问就是"临时方案，下周就改"。
// 为了"安全"，还特意做了 base64 —— 你看，连注释都在骗自己。
const _debugKey = atob("bGV0bWVpbl8yMDI2"); // 自己解码去 :)

/**
 * 备份接口（内部）：
 *   GET ${API_BASE}/backup?key=<_debugKey>
 * 成功时返回 { ok: true, flag: "..." }
 */
async function login() {
  const u = document.getElementById("u").value;
  const p = document.getElementById("p").value;
  const msg = document.getElementById("msg");
  msg.textContent = "";
  try {
    const r = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, password: p }),
    }).then((res) => res.json());
    msg.textContent = r.msg || "登录失败";
  } catch (e) {
    msg.textContent = "网络错误";
  }
}

document.getElementById("btn").addEventListener("click", login);

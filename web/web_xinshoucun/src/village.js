/* ============================================================
 * 新手村村民活动脚本 v1.0 —— 村委会出品
 * （在"查看源代码"里你只能看到对它的引用；
 *   想读内容？F12 → Network / Sources 面板走起。）
 * ============================================================ */
(function () {
  // ---- 村民闲聊：纯彩蛋，跟通关无关，图一乐 ----
  var chat = [
    '村民甲：村口的告示牌被独眼老兵施了隐形魔法，谁都看不见……',
    '村民乙：驿站站长梅琳只跟"专业的信使"打交道，还得带介绍信。',
    '村民丙：铁匠铺那台"验钞机"是上周才装的，唬人的。',
    '村民丁：探险家艾拉常说——"禁止进入"四个字，读作"欢迎光临"。'
  ];

  // ---- 隐形告示牌 ----
  // 村民每天用 JS 把告示牌挂到页面最底部，还罩了 display:none：
  // 肉眼看不见，"查看源代码"里也没有（源码是服务器发来的原始 HTML，
  // 这个节点是浏览器跑完 JS 之后才出现的）。
  // 但在 Elements 的实时 DOM 里，它无所遁形。
  var board = document.createElement('div');
  board.id = 'notice-board';
  board.style.display = 'none';
  board.setAttribute('data-owner', '独眼老兵·凯恩');
  board.textContent =
    '【隐形告示牌】冒险者口令：eyes-open —— 凭此口令向独眼老兵报到。';
  document.body.appendChild(board);

  // ---- 把村民闲聊塞进页脚（这个是可见的）----
  var slot = document.querySelector('.chat-slot');
  if (slot) {
    var foot = document.createElement('div');
    foot.className = 'village-chat';
    foot.textContent = '【村民闲聊】' + chat.join('　');
    slot.appendChild(foot);
  }
})();

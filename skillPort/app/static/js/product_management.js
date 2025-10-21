// ===== 商品管理ページの簡易スクリプト =====
document.addEventListener('DOMContentLoaded', () => {
  const moreBtn = document.querySelector('.more-btn');
  if (!moreBtn) return;

  // 「もっと見る」をクリック → ダミー商品を追加
  moreBtn.addEventListener('click', () => {
    const original = moreBtn.textContent;
    moreBtn.disabled = true;
    moreBtn.textContent = '読み込み中…';

    setTimeout(() => {
      const grid = document.querySelector('.grid');
      if (grid) {
        // 6枚分のカードを追加（ダミーデータ）
        for (let i = 0; i < 6; i++) {
          const el = document.createElement('article');
          el.className = 'card';
          el.innerHTML = `
            <div class="thumb">
              <img src="../../static/media/monkey.png" alt="item">
            </div>
            <div class="ops">
              <span class="badge">出品中</span>
              <button class="ghost-sm">編集</button>
            </div>
          `;
          grid.appendChild(el);
        }
      }
      moreBtn.disabled = false;
      moreBtn.textContent = original;
    }, 650);
  });
});
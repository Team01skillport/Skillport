// ヘッダードロップダウンの開閉（簡易）
document.addEventListener('click', (e) => {
  const dd = document.getElementById('nav-category');
  if (!dd) return;
  if (dd.contains(e.target)) {
    dd.classList.toggle('open');
  } else {
    dd.classList.remove('open');
  }
});

// サムネイルクリックでメイン画像切替
document.addEventListener('DOMContentLoaded', () => {
  const main = document.getElementById('mainImage');
  document.querySelectorAll('.thumbnails img').forEach(img => {
    img.addEventListener('click', () => {
      document.querySelectorAll('.thumbnails img').forEach(t => t.classList.remove('active'));
      img.classList.add('active');
      main.src = img.src;
    });
  });
});
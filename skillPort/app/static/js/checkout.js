// ==========================================================
// !! 注意 !!
// 以下のコードは、 base.html から継承されたヘッダーの
// カテゴリドロップダウンを動作させるために必要です。
// base.html を変更しない前提であるため、このコードは
// product_detail.js など他のJSファイルと重複しますが、
// 意図的に残しています。
// ==========================================================
document.addEventListener('click', (e) => {
  const dd = document.getElementById('nav-category');
  if (!dd) return;
  if (dd.contains(e.target)) {
    dd.classList.toggle('open');
  } else {
    dd.classList.remove('open');
  }
});
// ==========================================================
// 共通JSここまで
// ==========================================================


// 支払い方法の表示を右側サマリーへ反映
document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('paymentSelect');
  const sumPayment = document.getElementById('sumPayment');

  if (select && sumPayment) {
    const sync = () => (sumPayment.textContent = select.value);
    select.addEventListener('change', sync);
    sync(); // 初期表示
  }

  // 「購入する」ボタン（ダミー動作）
  const buy = document.getElementById('btnPurchase');
  buy?.addEventListener('click', () => {
    alert('購入が完了しました。ありがとうございます！');
  });

  // ダミーの「変更」ボタン
  document.getElementById('btnEditPayment')?.addEventListener('click', () => {
    select.focus();
  });
  document.getElementById('btnEditAddress')?.addEventListener('click', () => {
    alert('配送先の編集は現在準備中です。');
  });
});
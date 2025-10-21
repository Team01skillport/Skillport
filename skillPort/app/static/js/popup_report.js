// ===== 商品通報ポップアップ制御 =====
document.addEventListener("DOMContentLoaded", () => {
  const reportBtn = document.getElementById("reportBtn");
  const reportModal = document.getElementById("reportModal");
  const closeModal = document.getElementById("closeModal");
  const reportForm = document.getElementById("reportForm");

  if (!reportModal) return;

  // 通報ボタンを押す → モーダル表示
  if (reportBtn) {
    reportBtn.addEventListener("click", (e) => {
      e.preventDefault();
      reportModal.classList.remove("hidden");
    });
  }

  // キャンセルボタン → 閉じる
  closeModal?.addEventListener("click", () => {
    reportModal.classList.add("hidden");
  });

  // 背景クリックでも閉じる
  reportModal.addEventListener("click", (e) => {
    if (e.target === reportModal) {
      reportModal.classList.add("hidden");
    }
  });

  // フォーム送信
  reportForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const reason = reportForm.reason.value;
    const detail = reportForm.detail.value.trim();
    if (!reason) return alert("通報理由を選択してください。");
    alert("通報を受け付けました。ありがとうございます！");
    reportModal.classList.add("hidden");
    reportForm.reset();
  });
});
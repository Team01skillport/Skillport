document.addEventListener("DOMContentLoaded", function () {
  const profileImage = document.querySelector(".profile-set-img");
  const fileInput = document.getElementById("fileInput");
  const profileForm = document.getElementById("profileForm");
  const personalInfoForm = document.getElementById("personalInfoForm");

  // ===========================
  // 1. プロフィール画像のプレビュー機能
  // ===========================
  if (fileInput && profileImage) {
    fileInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          profileImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ===========================
  // 2. テキストエリアの自動リサイズ
  // ===========================
  function autoResizeTextarea(textarea) {
    if (textarea && textarea.tagName === "TEXTAREA") {
      textarea.style.height = "auto"; // Reset height to recalculate
      textarea.style.height = textarea.scrollHeight + "px"; // Set to scroll height
    }
  }

  // すべてのtextareaに対して適用
  document.querySelectorAll("textarea").forEach((textarea) => {
    textarea.addEventListener("input", () => autoResizeTextarea(textarea));
    // 初期ロード時にもリサイズを実行して、DBからの初期値に対応
    autoResizeTextarea(textarea);
  });

  // ===========================
  // 3. フォーム送信の処理 (フロントエンドでの仮の処理)
  // ===========================

  // ===========================
  // 4. 初期値のプレースホルダー処理 (例: 年/月/日)
  // ===========================
  const dateInputs = document.querySelectorAll(
    '.date-inputs input[type="number"]'
  );
  dateInputs.forEach((input) => {
    // 初期値がプレースホルダーと同じ場合、空にする
    if (input.value === input.placeholder) {
      input.value = "";
    }
    input.addEventListener("focus", function () {
      if (this.value === this.placeholder) {
        this.value = "";
      }
    });
    input.addEventListener("blur", function () {
      if (this.value === "") {
        this.value = this.placeholder;
      }
    });
  });

  // 初期値が "元の情報を載せます" の場合も同様に処理
  document.querySelectorAll('input[type="text"], textarea').forEach((input) => {
    if (input.value === "元の情報を載せます") {
      input.value = "";
      input.placeholder = "元の情報を載せます"; // Placeholderとして表示
    }
  });


  // ===========================
  // ⭐️ 5. 電話番号の入力制限 (数字のみ許可) ⭐️
  // ===========================
  const phoneInput = document.getElementById('phoneNumInput');
  
  if (phoneInput) {
    // inputイベント（入力が発生するたび）を監視
    phoneInput.addEventListener('input', function(e) {
      // 0-9の数字以外の文字をすべて空文字（""）に置き換える
      // これにより、リアルタイムで数字以外の入力が削除される
      this.value = this.value.replace(/[^0-9]/g, '');
    });
  }
});
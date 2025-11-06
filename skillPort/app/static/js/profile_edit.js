document.addEventListener('DOMContentLoaded', function() {
    const profileImage = document.querySelector('.profile-set-img');
    const fileInput = document.getElementById('fileInput');
    const profileForm = document.getElementById('profileForm');
    const personalInfoForm = document.getElementById('personalInfoForm');

    // ===========================
    // 1. プロフィール画像のプレビュー機能
    // ===========================
    if (fileInput && profileImage) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
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
        if (textarea && textarea.tagName === 'TEXTAREA') {
            textarea.style.height = 'auto'; // Reset height to recalculate
            textarea.style.height = textarea.scrollHeight + 'px'; // Set to scroll height
        }
    }

    // すべてのtextareaに対して適用
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', () => autoResizeTextarea(textarea));
        // 初期ロード時にもリサイズを実行して、DBからの初期値に対応
        autoResizeTextarea(textarea); 
    });


    // ===========================
    // 3. フォーム送信の処理 (フロントエンドでの仮の処理)
    // ===========================
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault(); // デフォルトのフォーム送信を防止
            alert('プロフィール情報が更新されました！（仮の処理。実際はサーバーにデータを送信します）');
            // ここに実際のフォーム送信やAjaxリクエストのロジックを追加します
            // 例: const formData = new FormData(profileForm);
            // fetch('/api/profile/update', { method: 'POST', body: formData })
            //   .then(response => response.json())
            //   .then(data => console.log(data));
        });
    }

    if (personalInfoForm) {
        personalInfoForm.addEventListener('submit', function(e) {
            e.preventDefault(); // デフォルトのフォーム送信を防止
            alert('個人情報が更新されました！（仮の処理。実際はサーバーにデータを送信します）');
            // ここに実際のフォーム送信やAjaxリクエストのロジックを追加します
        });
    }

    // ===========================
    // 4. 初期値のプレースホルダー処理 (例: 年/月/日)
    //    Jinja2で直接DBの値を'value'属性に出力するのが理想的ですが、
    //    JavaScriptで制御する場合の例です。
    // ===========================
    const dateInputs = document.querySelectorAll('.date-inputs input[type="number"]');
    dateInputs.forEach(input => {
        // 初期値がプレースホルダーと同じ場合、空にする
        if (input.value === input.placeholder) {
            input.value = '';
        }
        input.addEventListener('focus', function() {
            if (this.value === this.placeholder) {
                this.value = '';
            }
        });
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.value = this.placeholder;
            }
        });
    });

    // 初期値が "元の情報を載せます" の場合も同様に処理
    document.querySelectorAll('input[type="text"], textarea').forEach(input => {
        if (input.value === '元の情報を載せます') {
            input.value = '';
            input.placeholder = '元の情報を載せます'; // Placeholderとして表示
        }
    });

});
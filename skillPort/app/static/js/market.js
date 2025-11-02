// --- グローバル変数・定数 ---------------------------------
let categories_from_db = []; // 初期値を空配列に設定

// --- 関数定義 --------------------------------------------

/**
 * 各フィルターセクションの展開/折りたたみを処理
 * @param {Event} event - クリックイベント
 */
function handleFilterToggle(event) {
    const button = event.currentTarget;
    const filterSection = button.closest('.filter-section');
    const content = filterSection.querySelector('.filter-content');

    if (!content) return;

    const isOpen = button.classList.contains('open');

    // すべてのセクションを閉じる
    document.querySelectorAll('.filter-section .filter-content').forEach(otherContent => {
        otherContent.style.display = 'none';
        otherContent.closest('.filter-section').querySelector('.toggle-filter-btn').classList.remove('open');
    });

    // もしクリックしたセクションが閉じていたら、開く
    if (!isOpen) {
        button.classList.add('open');
        content.style.display = 'block';
        
        if (filterSection.id === 'categoryFilter' && content.innerHTML.trim() === '') {
            renderCategories(categories_from_db, content);
        }
    }
}


/**
 * カテゴリーリストをHTMLとして生成・描画
 * @param {Array<{id: string, name: string}>} categories - カテゴリーデータの配列
 * @param {HTMLElement} container - 描画先のコンテナ要素
 */
function renderCategories(categories, container) {
    
    // カテゴリーが null や空配列でないか確認
    if (!Array.isArray(categories) || categories.length === 0) {
        container.innerHTML = '<p style="font-size: 13px; color: #777; padding-left: 5px;">カテゴリーが見つかりません。</p>';
        return; // クラッシュを防ぐ
    }

    const checkboxGroup = document.createElement('div');
    checkboxGroup.className = 'filter-checkbox-group';
    
    const html = categories.map(cat => `
        <label>
            <input type="checkbox" name="category" value="${cat.id}" /> ${cat.name}
        </label>
    `).join('');
    
    checkboxGroup.innerHTML = html;
    container.appendChild(checkboxGroup);
}

// ▼ 価格スライダーの処理 START ▼
/**
 * 価格スライダーの値が変更されたときに表示を更新
 * [変更] スライダーの値を「最大価格」の入力欄にも反映する
 * @param {Event} event - inputイベント
 */
function updatePriceDisplay(event) {
    const priceValueSpan = document.getElementById('priceValue');
    // [新] Maxの入力欄を取得
    const maxPriceInput = document.querySelector('.price-inputs input[name="max_price"]'); 
    
    const numericValue = parseInt(event.target.value);
    const formattedValue = numericValue.toLocaleString(); // 3桁区切りのカンマ

    if (priceValueSpan) {
        priceValueSpan.textContent = formattedValue;
    }
    if (maxPriceInput) {
        maxPriceInput.value = numericValue; // [新] Maxの入力欄に値を設定
    }
}
// ▲ 価格スライダーの処理 END ▲


/**
 * マーケットページの初期化処理
 */
function initMarketPage() {
    
    // 1. HTML (form.sidebar) から 'data-categories' 属性を読み込む
    const sidebarElement = document.querySelector('.sidebar');
    if (sidebarElement && sidebarElement.dataset.categories) {
        try {
            const parsedData = JSON.parse(sidebarElement.dataset.categories);
            // 2. 変換後のデータが 'null' や 'undefined' ではなく、配列であることを確認
            if (Array.isArray(parsedData)) {
                categories_from_db = parsedData; // グローバル変数に格納
            } else {
                categories_from_db = []; // 'null' などの場合は空配列をセット
            }
        } catch (e) {
            console.error("カテゴリーデータの読み込みに失敗しました:", e);
            categories_from_db = []; // エラーの場合は空にする
        }
    }

    // 各フィルターセクションのトグルボタンを取得
    const allToggleButtons = document.querySelectorAll('.toggle-filter-btn');

    // ▼ 価格スライダーの要素を取得 ▼
    const priceRangeSlider = document.getElementById('priceRange');
    
    // --- [▼▼▼ 新增代码 ▼▼▼] ---
    // ページ読み込み時に、スライダーの初期値をMin/Max入力欄に設定する
    const minPriceInput = document.querySelector('.price-inputs input[name="min_price"]');
    const maxPriceInput = document.querySelector('.price-inputs input[name="max_price"]');
    // --- [▲▲▲ 新增代码 ▲▲▲] ---


    // 各フィルターセクションの展開/折りたたみイベントを設定
    allToggleButtons.forEach(button => {
        button.type = 'button'; 
        button.addEventListener('click', handleFilterToggle);
    });

    // ▼ 価格スライダーのイベントを設定 ▼
    if (priceRangeSlider) {
        const priceValueSpan = document.getElementById('priceValue');
        const initialNumericValue = parseInt(priceRangeSlider.value);
        
        if (priceValueSpan) {
            priceValueSpan.textContent = initialNumericValue.toLocaleString();
        }

        // --- [▼▼▼ 新增代码 ▼▼▼] ---
        // 1. Min入力欄にスライダーの最小値を設定
        if (minPriceInput && minPriceInput.value === '') { // ユーザーが既に入力していない場合
            minPriceInput.value = priceRangeSlider.min;
        }
        // 2. Max入力欄にスライダーの現在の値を設定
        if (maxPriceInput && maxPriceInput.value === '') {
            maxPriceInput.value = initialNumericValue;
        }
        // --- [▲▲▲ 新增代码 ▲▲▲] ---

        priceRangeSlider.addEventListener('input', updatePriceDisplay);
    }
}

// --- 実行 --------------------------------------------------
document.addEventListener('DOMContentLoaded', initMarketPage);
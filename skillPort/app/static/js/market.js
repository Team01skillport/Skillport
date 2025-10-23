// --- グローバル変数・定数 ---------------------------------

/** サンプル商品データ */
const allProducts = [
    { id: 1, title: "ChatGPTと学ぶPython入門", price: 1100, image: "monkey-selfie-david-slater.jpg" },
    { id: 2, title: "キャラクターデザイン講座", price: 2500, image: "monkey-selfie-david-slater.jpg" },
    { id: 3, title: "ウェブサイト制作チュートリアル", price: 1800, image: "monkey-selfie-david-slater.jpg" },
    { id: 4, title: "最新アニメ技術解説", price: 3200, image: "monkey-selfie-david-slater.jpg" },
    { id: 5, title: "音楽制作の基礎", price: 1500, image: "monkey-selfie-david-slater.jpg" },
    { id: 6, title: "野生動物の撮影テクニック", price: 2800, image: "monkey-selfie-david-slater.jpg" },
    { id: 7, title: "ChatGPTと学ぶPython入門", price: 1100, image: "monkey-selfie-david-slater.jpg" },
    { id: 8, title: "キャラクターデザイン講座", price: 2500, image: "monkey-selfie-david-slater.jpg" },
    { id: 9, title: "ウェブサイト制作チュートリアル", price: 1800, image: "monkey-selfie-david-slater.jpg" },
    { id: 10, title: "最新アニメ技術解説", price: 3200, image: "monkey-selfie-david-slater.jpg" },
    { id: 11, title: "音楽制作の基礎", price: 1500, image: "monkey-selfie-david-slater.jpg" },
    { id: 12, title: "野生動物の撮影テクニック", price: 2800, image: "monkey-selfie-david-slater.jpg" },
    { id: 13, title: "追加の商品A", price: 1000, image: "monkey-selfie-david-slater.jpg" },
    { id: 14, title: "追加の商品B", price: 2000, image: "monkey-selfie-david-slater.jpg" },
    { id: 15, title: "追加の商品C", price: 3000, image: "monkey-selfie-david-slater.jpg" },
    { id: 16, title: "追加の商品D", price: 4000, image: "monkey-selfie-david-slater.jpg" },
    { id: 17, title: "最後の商品E", price: 5000, image: "monkey-selfie-david-slater.jpg" }
];

/** サンプルカテゴリーデータ */
const learningCategories = [
    { id: 1, name: "本・雑誌・漫画" }, { id: 2, name: "資格・学習参考書" },
    { id: 3, name: "PC・タブレット・周辺機器" }, { id: 4, name: "カメラ・オーディオ・楽器" },
    { id: 5, name: "スポーツ・フィットネス" }, { id: 6, name: "趣味・ホビー" }
];

// ページネーション設定
const ITEMS_PER_PAGE = 8;
let currentPage = 1;

// DOM要素 (グローバル)
let productGrid = null;
let loadMoreBtn = null;
let categoryListContainer = null;
let toggleFiltersBtn = null;      // !!! 新しい変数 !!! 「絞り込み」ボタン
let filterSectionsContainer = null; // !!! 新しい変数 !!! フィルター全体のコンテナ


// --- 関数定義 --------------------------------------------

/** 商品カードHTML生成 */
function createProductCard(product) {
    const imageUrl = `${STATIC_MEDIA_URL}${product.image}`;
    const detailUrl = `${PRODUCT_DETAIL_URL_BASE}${product.id}`;
    return `
        <a href="${detailUrl}" class="product-card-link">
            <div class="product-card" data-id="${product.id}">
                <img src="${imageUrl}" alt="${product.title}" class="product-image">
                <div class="product-info">
                    <div class="product-title">${product.title}</div>
                    <div class="product-price">¥${product.price}</div>
                </div>
            </div>
        </a>
    `;
}

/** 指定ページの商品を描画 */
function renderProducts(page) {
    const start = (page - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const productsToRender = allProducts.slice(start, end);

    if (productsToRender.length > 0) {
        productGrid.innerHTML += productsToRender.map(createProductCard).join('');
    }

    if (end >= allProducts.length) {
        loadMoreBtn.style.display = 'none';
    } else {
        loadMoreBtn.style.display = 'block';
    }
}

/** 「もっと見る」ボタン処理 */
function handleLoadMoreClick() {
    currentPage++;
    renderProducts(currentPage);
}

/** カテゴリーリスト生成 */
function renderCategories(categories) {
    categoryListContainer.innerHTML = '';
    const html = categories.map(cat => `
        <button class="filter-list-item" data-category-id="${cat.id}">
            <span>${cat.name}</span>
            <span class="arrow">＞</span>
        </button>
    `).join('');
    categoryListContainer.innerHTML = html;
    categoryListContainer.querySelectorAll('.filter-list-item').forEach(item => {
        item.addEventListener('click', handleCategoryClick);
    });
}

/** カテゴリー項目クリック処理 */
function handleCategoryClick(event) {
    categoryListContainer.querySelectorAll('.filter-list-item').forEach(item => {
        item.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
    const selectedCategoryId = event.currentTarget.dataset.categoryId;
    console.log(`選択された親カテゴリID: ${selectedCategoryId}`);
    // TODO: 商品フィルターロジック
    // (現在はダミーとして全商品再描画)
    // productGrid.innerHTML = '';
    // currentPage = 1;
    // renderProducts(currentPage);
}

/**
 * フィルターセクション「内部」の展開/折りたたみを処理
 * (例: カテゴリーリスト、価格入力欄など)
 * @param {Event} event - クリックイベント
 */
function handleFilterToggle(event) {
    const button = event.currentTarget;
    const filterSection = button.closest('.filter-section');
    const content = filterSection.querySelector('.filter-content');

    if (!content) return;

    button.classList.toggle('open');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        if (filterSection.id === 'categoryFilter' && categoryListContainer.innerHTML === '') {
            renderCategories(learningCategories);
        }
    } else {
        content.style.display = 'none';
    }
}

/**
 * !!! 新しい関数 !!!
 * 「絞り込み」ボタンクリックでフィルター全体を表示/非表示
 */
function handleToggleAllFilters() {
    /* なぜ？: 「絞り込み」ボタン をクリックした時に、
             フィルター項目全体 (filterSectionsContainer) の表示を切り替えるため。*/
             
    toggleFiltersBtn.classList.toggle('open'); // アイコン回転用クラス
    
    if (filterSectionsContainer.style.display === 'none') {
        filterSectionsContainer.style.display = 'block';
    } else {
        filterSectionsContainer.style.display = 'none';
    }
}

/**
 * マーケットページの初期化処理
 */
function initMarketPage() {
    // DOM要素の取得
    productGrid = document.getElementById('productGrid');
    loadMoreBtn = document.querySelector('.load-more');
    categoryListContainer = document.getElementById('categoryListContainer');
    // !!! 新しい要素を取得 !!!
    toggleFiltersBtn = document.getElementById('toggleFiltersBtn');
    filterSectionsContainer = document.getElementById('filterSectionsContainer'); 
    
    // 各フィルターセクション「内部」のトグルボタンを取得
    const allInnerToggleButtons = document.querySelectorAll('.toggle-filter-btn');

    /* なぜチェック？: 必須要素が見つからない場合にエラーを防ぐため。*/
    if (!productGrid || !loadMoreBtn || !categoryListContainer || !toggleFiltersBtn || !filterSectionsContainer) { 
        console.error('Market page critical elements not found.');
        return;
    }

    productGrid.innerHTML = ''; 
    currentPage = 1;
    renderProducts(currentPage);

    // 「もっと見る」ボタンのイベント
    loadMoreBtn.addEventListener('click', handleLoadMoreClick);

    // !!! 新しいイベント !!! 
    // 「絞り込み」ボタンでフィルター全体をトグル
    toggleFiltersBtn.addEventListener('click', handleToggleAllFilters);

    // !!! 変更 !!! 
    // 各フィルターセクション「内部」のトグルイベントを設定
    // (これは handleFilterToggle を呼び出す)
    allInnerToggleButtons.forEach(button => {
        button.addEventListener('click', handleFilterToggle);
    });
}


// --- 実行 --------------------------------------------------
document.addEventListener('DOMContentLoaded', initMarketPage);
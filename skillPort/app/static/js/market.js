// --- グローバル変数・定数 ---------------------------------

/**
 * サンプル商品データ
 * 将来的にはAPIから非同期で取得することを想定
 */
const allProducts = [
    { id: 1, title: "ChatGPTと学ぶPython入門", price: 1100, image: "monkey-selfie-david-slater.jpg" },
    { id: 2, title: "キャラクターデザイン講座", price: 2500, image: "monkey-selfie-david-slater.jpg" },
    { id: 3, title: "ウェブサイト制作チュートリアル", price: 1800, image: "monkey-selfie-david-slater.jpg" },
    { id: 4, title: "最新アニメ技術解説", price: 3200, image: "monkey-selfie-david-slater.jpg" },
    { id: 5, title: "音楽制作の基礎", price: 1500, image: "monkey-selfie-david-slater.jpg" },
    { id: 6, title: "野生動物の撮影テクニック", price: 2800, image: "monkey-selfie-david-slater.jpg" },
    { id: 7, title: "ChatGPTと学ぶPython入門", price: 1100, image: "monkey-selfie-david-slater.jpg" },
    { id: 8, title: "キャラクターデザイン講座", price: 2500, image: "monkey-selfie-david-slater.jpg" },
    // 「もっと見る」用の追加データ
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

/**
 * !!! 新しいカテゴリーデータ !!!
 * ご要望に基づき、「学習」テーマで 6 つの親カテゴリーを作成
 */
const learningCategories = [
    { id: 1, name: "本・雑誌・漫画" },
    { id: 2, name: "資格・学習参考書" },
    { id: 3, name: "PC・タブレット・周辺機器" },
    { id: 4, name: "カメラ・オーディオ・楽器" },
    { id: 5, name: "スポーツ・フィットネス" },
    { id: 6, name: "趣味・ホビー" }
];

// ページネーション（分割表示）設定
const ITEMS_PER_PAGE = 8;
let currentPage = 1;

// DOM要素 (グローバル)
let productGrid = null;
let loadMoreBtn = null;
let categoryListContainer = null; // (旧: categoryList)


// --- 関数定義 --------------------------------------------

/**
 * 1つの商品オブジェクトからHTML文字列を生成する
 * @param {object} product - 商品情報オブジェクト
 * @returns {string} 商品カードのHTML
 */
function createProductCard(product) {
    /* なぜ？: HTML 側で定義されたグローバル変数から
             静的ファイル（画像）への正しいパスを取得する。*/
    const imageUrl = `${STATIC_MEDIA_URL}${product.image}`;

    /* なぜ？: 同様に、HTML 側で定義された
             商品詳細ページへの基本URLを取得する。*/
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

/**
 * 指定されたページの商品をグリッドに追加描画する
 * @param {number} page - 読み込むページ番号
 */
function renderProducts(page) {
    const start = (page - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const productsToRender = allProducts.slice(start, end);

    if (productsToRender.length > 0) {
        const productsHTML = productsToRender.map(createProductCard).join('');
        productGrid.innerHTML += productsHTML;
    }

    if (end >= allProducts.length) {
        loadMoreBtn.style.display = 'none';
    } else {
        loadMoreBtn.style.display = 'block';
    }
}

/**
 * 「もっと見る」ボタンがクリックされた時の処理
 */
function handleLoadMoreClick() {
    currentPage++;
    renderProducts(currentPage);
}

/**
 * !!! 変更 !!!
 * (旧: renderSubcategories)
 * 新しい親カテゴリーリストを生成し、DOMに挿入する
 * @param {Array} categories - 親カテゴリーオブジェクトの配列
 */
function renderCategories(categories) {
    categoryListContainer.innerHTML = ''; // まずリストをクリア
    
    /* なぜ？: 'image_e05b80' のデザインに合わせるため、
             右側に矢印(＞)を持つボタンを生成する。*/
    const html = categories.map(cat => `
        <button class="filter-list-item" data-category-id="${cat.id}">
            <span>${cat.name}</span>
            <span class="arrow">＞</span>
        </button>
    `).join('');
    
    categoryListContainer.innerHTML = html;

    // カテゴリー項目にクリックイベントを設定
    categoryListContainer.querySelectorAll('.filter-list-item').forEach(item => {
        item.addEventListener('click', handleCategoryClick);
    });
}

/**
 * !!! 変更 !!!
 * (旧: handleSubcategoryClick)
 * 親カテゴリー項目がクリックされた時の処理
 * @param {Event} event - クリックイベント
 */
function handleCategoryClick(event) {
    /* なぜ？: 将来的に、クリックされた親カテゴリーの
             「サブカテゴリー」を表示する処理をここに追加するため。*/
    
    // (一旦、選択されたことを示すためにクラスを追加)
    categoryListContainer.querySelectorAll('.filter-list-item').forEach(item => {
        item.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');

    const selectedCategoryId = event.currentTarget.dataset.categoryId;
    console.log(`選択された親カテゴリID: ${selectedCategoryId}`);
    
    // TODO: ここでサブカテゴリーのリストを表示するロジックを将来的に追加
    
    // (現在はダミーとして、全商品を再描画)
    // productGrid.innerHTML = '';
    // currentPage = 1;
    // renderProducts(currentPage);
}

/**
 * 汎用トグル関数
 * 全てのフィルターセクションの展開/折りたたみを処理する
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
        
        /* なぜチェック？: 「カテゴリー」フィルター を開いた時だけ、
                         中身が空であれば動的に「親カテゴリー」を生成するため。*/
        if (filterSection.id === 'categoryFilter' && categoryListContainer.innerHTML === '') {
            renderCategories(learningCategories); // 新しいデータ を使用
        }
    } else {
        content.style.display = 'none';
    }
}

/**
 * マーケットページの初期化処理
 */
function initMarketPage() {
    // グローバル変数にDOM要素を割り当てる
    productGrid = document.getElementById('productGrid');
    loadMoreBtn = document.querySelector('.load-more');
    // !!! 変更 !!! (IDを 'categoryList' から変更)
    categoryListContainer = document.getElementById('categoryListContainer'); 

    const allToggleButtons = document.querySelectorAll('.toggle-filter-btn');

    /* なぜチェック？: 要素が見つからない場合にエラーで停止するのを防ぐため。*/
    if (!productGrid || !loadMoreBtn || !categoryListContainer) { 
        console.error('Market page critical elements not found.');
        return;
    }

    productGrid.innerHTML = ''; 
    currentPage = 1;
    renderProducts(currentPage);

    loadMoreBtn.addEventListener('click', handleLoadMoreClick);

    // すべてのトグルボタンに汎用トグル関数を割り当て
    allToggleButtons.forEach(button => {
        button.addEventListener('click', handleFilterToggle);
    });
}


// --- 実行 --------------------------------------------------
document.addEventListener('DOMContentLoaded', initMarketPage);
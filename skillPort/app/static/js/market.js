// --- グローバル変数・定数 ---------------------------------

// サンプル商品データ
// （将来的にはAPIから非同期で取得する）
const allProducts = [
    { id: 1, title: "ChatGPTと学ぶPython入門", price: 1100, image: "market_commodity_book01.png" },
    { id: 2, title: "キャラクターデザイン講座", price: 2500, image: "market_commodity_book01.png" },
    { id: 3, title: "ウェブサイト制作チュートリアル", price: 1800, image: "market_commodity_book01.png" },
    { id: 4, title: "最新アニメ技術解説", price: 3200, image: "market_commodity_book01.png" },
    { id: 5, title: "音楽制作の基礎", price: 1500, image: "market_commodity_book01.png" },
    { id: 6, title: "野生動物の撮影テクニック", price: 2800, image: "market_commodity_book01.png" },
    { id: 7, title: "ChatGPTと学ぶPython入門", price: 1100, image: "market_commodity_book01.png" },
    { id: 8, title: "キャラクターデザイン講座", price: 2500, image: "market_commodity_book01.png" },
    // 「もっと見る」用の追加データ
    { id: 9, title: "ウェブサイト制作チュートリアル", price: 1800, image: "market_commodity_book01.png" },
    { id: 10, title: "最新アニメ技術解説", price: 3200, image: "market_commodity_book01.png" },
    { id: 11, title: "音楽制作の基礎", price: 1500, image: "market_commodity_book01.png" },
    { id: 12, title: "野生動物の撮影テクニック", price: 2800, image: "market_commodity_book01.png" },
    { id: 13, title: "追加の商品A", price: 1000, image: "market_commodity_book01.png" },
    { id: 14, title: "追加の商品B", price: 2000, image: "market_commodity_book01.png" },
    { id: 15, title: "追加の商品C", price: 3000, image: "market_commodity_book01.png" },
    { id: 16, title: "追加の商品D", price: 4000, image: "market_commodity_book01.png" },
    { id: 17, title: "最後の商品E", price: 5000, image: "market_commodity_book01.png" }
];

// ページネーション（分割表示）設定
const ITEMS_PER_PAGE = 8;
let currentPage = 1;

// DOM要素
// （initMarketPage 関数内で取得）
let productGrid = null;
let loadMoreBtn = null;


// --- 関数定義 --------------------------------------------

/**
 * 1つの商品オブジェクトからHTML文字列を生成する
 * * @param {object} product - 商品情報オブジェクト
 * @returns {string} 商品カードのHTML
 */
function createProductCard(product) {
    // なぜ `STATIC_MEDIA_URL` を使うのか？
    // このJSファイルは 'url_for' を使えないため、
    // HTML 側で定義されたグローバル変数から
    // 静的ファイル（画像）への正しいパスを取得する。
    const imageUrl = `${STATIC_MEDIA_URL}${product.image}`;

    // なぜ `PRODUCT_DETAIL_URL_BASE` を使うのか？
    // 同様に、HTML 側で定義された
    // 商品詳細ページへの基本URL（例: /market/product/）を取得する。
    const detailUrl = `${PRODUCT_DETAIL_URL_BASE}${product.id}`;

    // カード全体をクリック可能なリンク(<a>)で囲む
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
 * * @param {number} page - 読み込むページ番号
 */
function renderProducts(page) {
    // 描画する商品の範囲を計算
    const start = (page - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    const productsToRender = allProducts.slice(start, end);

    if (productsToRender.length > 0) {
        const productsHTML = productsToRender.map(createProductCard).join('');
        
        // なぜ `+=` を使うのか？
        // `innerHTML = ...` は既存の内容を上書きしてしまう。
        // `innerHTML += ...` は、既存のカードに新しいカードを「追加」する。
        productGrid.innerHTML += productsHTML;
    }

    // 次に読み込む商品がもうないかチェック
    if (end >= allProducts.length) {
        // なぜ非表示にするのか？
        // すべての商品を表示し終えたので、
        // ユーザーに「もっと見る」ボタンを見せ続ける必要がないため。
        loadMoreBtn.style.display = 'none';
    }
}

/**
 * 「もっと見る」ボタンがクリックされた時の処理
 */
function handleLoadMoreClick() {
    currentPage++; // 次のページへ
    renderProducts(currentPage);
}

/**
 * マーケットページの初期化処理
 */
function initMarketPage() {
    // グローバル変数にDOM要素を割り当てる
    productGrid = document.getElementById('productGrid');
    loadMoreBtn = document.querySelector('.load-more');

    // なぜチェックするのか？
    // 要素が見つからない場合にエラーで停止するのを防ぐため。
    if (!productGrid || !loadMoreBtn) {
        console.error('Market page elements not found.');
        return;
    }

    // なぜクリアするのか？
    // ブラウザの「戻る」ボタンで表示が重複するのを防ぐため、
    // 読み込み時にグリッドを一度空にする。
    productGrid.innerHTML = ''; 
    currentPage = 1;

    // 1. 最初のページ（1ページ目）を描画
    renderProducts(currentPage);

    // 2. 「もっと見る」ボタンにクリックイベントを設定
    loadMoreBtn.addEventListener('click', handleLoadMoreClick);
}


// --- 実行 --------------------------------------------------

// HTMLのDOMツリーが構築完了したら、初期化処理を実行
document.addEventListener('DOMContentLoaded', initMarketPage);
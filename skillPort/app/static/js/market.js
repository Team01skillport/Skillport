// Sample product data
const products = [
    {
        id: 1,
        title: "ChatGPTと学ぶPython入門",
        price: 1100,
        image: "market_commodity_book01.png" // 1. 删除了错误路径, 只保留文件名
    },
    {
        id: 2,
        title: "キャラクターデザイン講座",
        price: 2500,
        image: "market_commodity_book01.png" // (示例图片)
    },
    {
        id: 3,
        title: "ウェブサイト制作チュートリアル",
        price: 1800,
        image: "market_commodity_book01.png" // (示例图片)
    },
    {
        id: 4,
        title: "最新アニメ技術解説",
        price: 3200,
        image: "market_commodity_book01.png" // (示例图片)
    },
    {
        id: 5,
        title: "音楽制作の基礎",
        price: 1500,
        image: "market_commodity_book01.png" // (示例图片)
    },
    {
        id: 6,
        title: "野生動物の撮影テクニック",
        price: 2800,
        image: "market_commodity_book01.png" // (示例图片)
    },
    // ... 更多商品 ...
    {
        id: 12,
        title: "野生動物の撮影テクニック",
        price: 2800,
        image: "market_commodity_book01.png" // (示例图片)
    }
];

// Function to create product card HTML
function createProductCard(product) {
    
    // 2. 使用从 market.html 传来的全局变量构建 URL
    // (确保 STATIC_MEDIA_URL 和 PRODUCT_DETAIL_URL_BASE 已在 HTML 中定义)
    
    // 构建商品详情页的 URL, e.g., /market/product/1
    const detailUrl = `${PRODUCT_DETAIL_URL_BASE}${product.id}`;
    
    // 构建图片的完整 URL, e.g., /static/media/market_commodity_book01.png
    const imageUrl = `${STATIC_MEDIA_URL}${product.image}`;

    // 3. 用 <a> 标签包裹卡片, 并使用正确的图片路径
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

// Function to render products when the page loads
function renderProducts() {
    const productGrid = document.getElementById('productGrid');
    if (productGrid) {
        const productsHTML = products.map(product => createProductCard(product)).join('');
        productGrid.innerHTML = productsHTML;
    }
}

// Ensure the DOM is fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    renderProducts();
});
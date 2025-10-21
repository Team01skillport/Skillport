// Sample product data with the new unified image
const products = [
    {
        id: 1,
        title: "ChatGPTと学ぶPython入門",
        price: 1100,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 2,
        title: "キャラクターデザイン講座",
        price: 2500,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 3,
        title: "ウェブサイト制作チュートリアル",
        price: 1800,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 4,
        title: "最新アニメ技術解説",
        price: 3200,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 5,
        title: "音楽制作の基礎",
        price: 1500,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 6,
        title: "野生動物の撮影テクニック",
        price: 2800,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 7,
        title: "ChatGPTと学ぶPython入門",
        price: 1100,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 8,
        title: "キャラクターデザイン講座",
        price: 2500,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 9,
        title: "ウェブサイト制作チュートリアル",
        price: 1800,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 10,
        title: "最新アニメ技術解説",
        price: 3200,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 11,
        title: "音楽制作の基礎",
        price: 1500,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    },
    {
        id: 12,
        title: "野生動物の撮影テクニック",
        price: 2800,
        image: "../static/media/market_commodity_book01.png" // 更新图片路径
    }
];

// Function to create product card HTML
function createProductCard(product) {
    return `
        <div class="product-card" data-id="${product.id}">
            <img src="${product.image}" alt="${product.title}" class="product-image">
            <div class="product-info">
                <div class="product-title">${product.title}</div>
                <div class="product-price">¥${product.price}</div>
            </div>
        </div>
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
    // You can add other event listeners for search, buttons etc. here if needed
});
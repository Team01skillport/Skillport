// サムネイルクリックでメイン画像切り替え
document.addEventListener("DOMContentLoaded", () => {
  const main = document.getElementById("mainImage");
  document.querySelectorAll(".thumbnails img").forEach((img) => {
    img.addEventListener("click", () => {
      document
        .querySelectorAll(".thumbnails img")
        .forEach((t) => t.classList.remove("active"));
      img.classList.add("active");
      main.src = img.src;
    });
  });
});

document
  .getElementById("favorite_button")
  .addEventListener("click", function () {
    const productId = this.dataset.productId;
    console.log("AJAX RUN");

    fetch(`/market/add_favorite/${productId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  });

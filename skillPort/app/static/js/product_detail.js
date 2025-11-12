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

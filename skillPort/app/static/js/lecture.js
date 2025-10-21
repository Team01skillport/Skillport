document.addEventListener("DOMContentLoaded", () => {
  // カテゴリドロップダウン
  const dd = document.getElementById("nav-category");
  document.addEventListener("click", e=>{
    if(dd && dd.contains(e.target)){ dd.classList.toggle("open"); }
    else if(dd) dd.classList.remove("open");
  });
});
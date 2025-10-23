console.log("BASE.JS LOADED");

// 検索バーに文字列が入っているかを確認
$(".search").on("submit", function (response) {
  let keyword = $("#search_bar").val().trim();
  if (keyword === "") {
    response.preventDefault();
    $("#search_bar")
      .val("")
      .attr("placeholder", "入力をしてください")
      .addClass("error");
  }
});

// ドロップダウンメニュー制御
document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.getElementById("nav-category");
  const toggle = dropdown.querySelector(".dropdown-toggle");

  toggle.addEventListener("click", (e) => {
    e.preventDefault();
    dropdown.classList.toggle("open");
  });

  // close if click outside
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove("open");
    }
  });
});

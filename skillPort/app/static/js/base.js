console.log("BASE.JS LOADED");

$("#search_button").on("click", function () {
  console.log("CLICK");
  if ($("#search_bar").val() == "") {
    this.placeholder = "検索したいコンテンツを入力してください";
  }
});

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

// dropdown---------------------------------------------------------

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

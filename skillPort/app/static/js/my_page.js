$(document).ready(function () {
  const defaultUrl = "view_history";
  $.ajax({
    url: defaultUrl,
    dataType: "html",
    method: "GET",
  })
    .done(function (data) {
      $("#main_content").html(data);
    })
    .fail(function () {
      console.log("FAIL");
    });
});

$(".menu_link").on("click", function (e) {
  e.preventDefault();
  const url = $(this).data("target");
  $(".menu_link").removeClass("active");
  $(this).addClass("active");
  $.ajax({
    url: url,
    dataType: "html",
    method: "GET",
  })
    .done(function (data) {
      $("#main_content").html(data);
    })
    .fail(function () {
      console.log("FAILED");
    });
});

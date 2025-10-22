$(".menu_link").on("click", function (e) {
  console.log("CLICK");
  e.preventDefault();
  const url = $(this).data("target");
  console.log(url);
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
  // .always(function () {});
});

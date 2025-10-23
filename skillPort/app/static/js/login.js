console.log("JS LOADED");

$(".login-form").on("submit", function (response) {
  console.log("CLICK");

  let username = $("#userId").val();
  let password = $("#password").val();
  if (username === "") {
    response.preventDefault();
    console.log("ENTER USERNAME");

    $("#userId").attr("placeholder", "ユーザー名を入力してください");
  }
  if (password === "") {
    response.preventDefault();
    console.log("ENTER PASSWORD");

    $("#password").attr("placeholder", "パスワードを入力してください");
  }
});

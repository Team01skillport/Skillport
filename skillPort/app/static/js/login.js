console.log("JS LOADED");

$(".login-form").on("submit", function (response) {
  console.log("CLICK");

  let username = $("#userId").val();
  let password = $("#password").val();
  if (username === "") {
    response.preventDefault();
    $("#userId").attr("placeholder", "ユーザー名を入力してください");
  } else if (username !== "") {
    $("#userId").attr("placeholder", "ユーザーID");
  }
  if (password === "") {
    response.preventDefault();
    $("#password").attr("placeholder", "パスワードを入力してください");
  } else if (password !== "") {
    $("#password").attr("placeholder", "パスワード");
  }
});

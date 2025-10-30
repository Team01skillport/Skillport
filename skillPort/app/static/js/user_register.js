console.log("JS LOADED");
errorMes = new Array();
$(".register-form").on("submit", function (response) {
  console.log("CLICK");
  $(".error").remove();

  $(".register-form input").each(function (index) {
    errorMes[2] = "メールを入力してください";
    errorMes[3] = "電話番号を入力してください";
    errorMes[4] = "姓を入力してください";
    errorMes[5] = "名を入力してください";
    errorMes[6] = "姓フリガナを入力してください";
    errorMes[7] = "名フリガナを入力してください";
    errorMes[8] = "誕生日を選択してください";
    errorMes[12] = "郵便番号を入力してください";
    errorMes[13] = "都道府県を入力してください";
    errorMes[14] = "市区町村を入力してください";
    errorMes[15] = "番地・建物名を入力してください";
    if ($(this).val() == "") {
      console.log(index);
      $(this).after(`<p class='error'>${errorMes[index]}</p>`);

      response.preventDefault();
    }
  });
  $(".error").css("color", "red");
});

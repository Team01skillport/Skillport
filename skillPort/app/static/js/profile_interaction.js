// profile_interaction.js

document.addEventListener("DOMContentLoaded", () => {
  const moreButtons = document.querySelectorAll(".more-btn");

  moreButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      const targetType = event.target.dataset.target; // 'video' または 'post'
      let container, itemSelector;

      if (targetType === "video") {
        // video-link要素にhidden-itemが付いている
        container = document.getElementById("video-section");
        itemSelector = ".video-link.hidden-item";
      } else if (targetType === "post") {
        // post-card要素にhidden-itemが付いている
        container = document.getElementById("post-section");
        itemSelector = ".post-card.hidden-item";
      }

      if (container) {
        // 現在非表示になっている要素（hidden-itemクラスを持つ要素）を全て取得
        const hiddenItems = container.querySelectorAll(itemSelector);

        // 最初から3つまでの要素に対してhidden-itemクラスを削除して表示する
        for (let i = 0; i < 3 && i < hiddenItems.length; i++) {
          hiddenItems[i].classList.remove("hidden-item");
        }

        // 全ての非表示要素を表示し終わったら、「もっと見る」ボタンを非表示にする
        const remainingHiddenItems = container.querySelectorAll(itemSelector);
        if (remainingHiddenItems.length === 0) {
          event.target.style.display = "none";
        }
      }
    });
  });
});
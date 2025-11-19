// (文件: skillPort/app/static/js/product_detail.js)

document.addEventListener("DOMContentLoaded", () => {
  // ===================================
  // 1. (已有功能) 缩略图点击
  // ===================================
  const main = document.getElementById("mainImage");
  const thumbnails = document.querySelectorAll(".thumbnails img");

  if (thumbnails.length > 0 && main) {
    thumbnails.forEach((img) => {
      img.addEventListener("click", () => {
        thumbnails.forEach((t) => t.classList.remove("active"));
        img.classList.add("active");
        main.src = img.src;
      });
    });
  }

  // ===================================
  // 2. (已有功能) 收藏按钮
  // ===================================
  const favButton = document.getElementById("favorite_button");

  if (favButton) {
    favButton.addEventListener("click", function () {
      const productId = this.dataset.productId;
      console.log("AJAX RUN: Favorite");

      fetch(`/market/add_favorite/${productId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data && data.success) {
            // 假设后端返回 {success: true}
            // favButton.value = "♡ お気に入り登録済み";
            favButton.disabled = true;

            $("#favorite_button").css({
              "background-color": "#007bff",
              color: "white",
              "font-weight": "bold",
            });
          } else {
            alert((data ? data.error : null) || "お気に入り登録に失敗しました");
          }
        })
        .catch((err) => console.error("Favorite fetch error:", err));
    });
  }

  // ===================================
  // 3. [新功能] 评论发送 (AJAX)
  // ===================================

  // (获取我们在 HTML 中添加的新元素)
  const commentForm = document.querySelector(".comment-form");
  const commentSubmitBtn = document.getElementById("commentSubmitBtn");
  const commentInput = document.getElementById("commentInput");
  const commentList = document.getElementById("commentList");

  if (commentSubmitBtn && commentForm && commentInput && commentList) {
    // (为“提交评论”按钮 绑定点击事件)
    commentSubmitBtn.addEventListener("click", async () => {
      const productId = commentForm.dataset.productId; // (获取商品 ID)
      const commentText = commentInput.value.trim();

      if (commentText === "") {
        alert("コメントを入力してください。");
        return;
      }

      commentSubmitBtn.disabled = true; // 防止重复提交

      try {
        // (使用 Fetch API 将数据发送到 market.py 中创建的新路由)
        const response = await fetch("/market/product/post_comment", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // (Flask 通常还需要 CSRF 令牌，但我们暂时先省略)
          },
          body: JSON.stringify({
            product_id: productId,
            comment_text: commentText,
          }),
        });

        const result = await response.json();

        if (response.ok && result.success) {
          // [成功]
          // 1. 调用一个新函数, 在页面上动态添加新评论
          addCommentToDOM(result.comment);
          // 2. 清空输入框
          commentInput.value = "";

          // 3. 移除“还没有评论”的提示信息
          const noCommentsEl = document.getElementById("noCommentsYet");
          if (noCommentsEl) {
            noCommentsEl.remove();
          }
        } else {
          // [失败]
          alert(result.error || "コメントの送信に失敗しました。");
        }
      } catch (error) {
        console.error("Comment fetch error:", error);
        alert("通信エラーが発生しました。");
      } finally {
        commentSubmitBtn.disabled = false; // 恢复按钮
      }
    });
  }

  /**
   * 辅助函数：将新评论动态添加到评论列表的顶部
   * @param {object} comment - 后端 `market.py` 返回的评论对象
   */
  function addCommentToDOM(comment) {
    const li = document.createElement("li");

    // (解析头像路径)
    const iconUrl =
      comment.profile_icon && comment.profile_icon != "/icons/default_icon.png"
        ? `/static/${comment.profile_icon.substring(1)}`
        : "/static/media/profile_icon.png";

    // (创建与 market.html 中相同的 HTML 结构)
    li.innerHTML = `
      <img src="${iconUrl}" alt="icon">
      <div class="bubble">
        <strong>${comment.user_name}</strong>
        <p>${comment.comment_text}</p>
      </div>
    `;

    // (将新评论添加到列表的最前面)
    commentList.prepend(li);
  }
}); // (结束 DOMContentLoaded)

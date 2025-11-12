// // ============================

// // New Post composer (+ preview only; no posting)

// // ============================

// document.addEventListener("DOMContentLoaded", () => {
//   const newPost = document.querySelector(".new-post");

//   if (!newPost) return;

//   const btnAdd = newPost.querySelector(".add");

//   const btnSend = newPost.querySelector(".send"); // acts as "open create popup"

//   const inputText = newPost.querySelector(".textbox .text");

//   const filePick = newPost.querySelector(".filepick");

//   const attachment = newPost.querySelector(".textbox .attachment");

//   const textbox = newPost.querySelector(".textbox");

//   if (btnSend) btnSend.setAttribute("type", "button");

//   let objectUrl = null;

//   // ＋ -> ファイル選択

//   if (btnAdd) {
//     btnAdd.addEventListener("click", (e) => {
//       e.preventDefault();

//       filePick?.click();
//     });
//   }

//   // 選択ファイルのプレビュー（1ファイル）

//   if (filePick) {
//     filePick.addEventListener("change", () => {
//       const file = filePick.files?.[0];

//       if (!file) return;

//       if (objectUrl) URL.revokeObjectURL(objectUrl);

//       objectUrl = URL.createObjectURL(file);

//       const isImg = file.type.startsWith("image/");

//       const isVid = file.type.startsWith("video/");

//       if (isImg) {
//         attachment.innerHTML = `
// <img src="${objectUrl}" style="width:100%;max-height:220px;border-radius:8px;display:block;">
// <button class="remove-btn" title="削除">✖</button>

//         `;
//       } else if (isVid) {
//         attachment.innerHTML = `
// <video controls src="${objectUrl}" style="width:100%;max-height:220px;border-radius:8px;display:block;"></video>
// <button class="remove-btn" title="削除">✖</button>

//         `;
//       } else {
//         attachment.innerHTML = `
// <div>このファイル形式はプレビューできません</div>
// <button class="remove-btn" title="削除">✖</button>

//         `;
//       }

//       textbox.classList.add("has-attachment");

//       const removeBtn = attachment.querySelector(".remove-btn");

//       removeBtn?.addEventListener("click", () => {
//         attachment.innerHTML = "";

//         textbox.classList.remove("has-attachment");

//         filePick.value = "";

//         if (objectUrl) {
//           URL.revokeObjectURL(objectUrl);
//           objectUrl = null;
//         }
//       });
//     });
//   }

//   // ▶ -> 「新規投稿」モードでモーダルを開く（※保存/送信はしない）

//   if (btnSend) {
//     btnSend.addEventListener("click", (e) => {
//       e.preventDefault();

//       const file = filePick?.files?.[0] || null;

//       if (!window.CommunityModal?.openForCreate) {
//         console.warn("[Community] Modal API not ready.");

//         return;
//       }

//       window.CommunityModal.openForCreate({
//         text: inputText?.value.trim() || "",

//         file,
//       });
//     });
//   }

//   // GC

//   window.addEventListener("beforeunload", () => {
//     if (objectUrl) URL.revokeObjectURL(objectUrl);
//   });
// });

// ============================

// 編集/作成 共通ポップアップ（見た目だけ; no save/post/delete）

// ============================

(function () {
  const modal = document.getElementById("editModal");

  if (!modal) return;

  const ta = modal.querySelector("#editText");

  const fileInput = modal.querySelector("#editFile");

  const btnPick = modal.querySelector("#btnPickMedia");

  const btnRemove = modal.querySelector("#btnRemoveMedia");

  const preview = modal.querySelector("#mediaPreview");

  const btnSave = modal.querySelector("#btnSaveEdit"); // 編集用

  const btnPost = modal.querySelector("#btnPostSubmit"); // 新規用

  const btnDelete = modal.querySelector("#btnDeletePost"); // (表示のみ)

  const closeEls = modal.querySelectorAll(
    '[data-close="true"], .modal__overlay'
  );

  let objectUrl = null;

  let replaceFile = null;

  let removeMedia = false;

  // ------- 表示切替 -------

  function showForEditMode() {
    modal.querySelector(".modal__header h3").textContent = "投稿を編集";

    btnSave.style.display = "inline-block";

    btnPost.style.display = "none";

    btnDelete.style.display = "inline-block";
  }

  function showForCreateMode() {
    modal.querySelector(".modal__header h3").textContent = "新規投稿";

    btnSave.style.display = "none";

    btnPost.style.display = "inline-block";

    btnDelete.style.display = "none";
  }

  // ------- API: 外から開く -------

  function openForEdit({ text = "", mediaEl = null } = {}) {
    ta.value = text;

    replaceFile = null;

    removeMedia = false;

    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }

    // 既存メディアをそのままプレビュー（読み取りのみ）

    preview.innerHTML = "";

    if (mediaEl) {
      if (mediaEl.tagName === "IMG") {
        const img = document.createElement("img");

        img.src = mediaEl.src;

        preview.appendChild(img);
      } else if (mediaEl.tagName === "VIDEO") {
        const v = document.createElement("video");

        v.controls = true;

        v.src = mediaEl.currentSrc || mediaEl.src;

        preview.appendChild(v);
      }
    } else {
      const p = document.createElement("div");
      p.textContent = "（メディアなし）";

      preview.appendChild(p);
    }

    showForEditMode();

    openModal();
  }

  function openForCreate({ text = "", file = null } = {}) {
    ta.value = text;

    removeMedia = false;

    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }

    replaceFile = null;

    if (file) {
      replaceFile = file;

      objectUrl = URL.createObjectURL(file);
    }

    renderPreview();

    showForCreateMode();

    openModal();
  }

  window.CommunityModal = { openForEdit, openForCreate };

  // ------- open/close -------

  function openModal() {
    modal.classList.add("is-open");

    modal.setAttribute("aria-hidden", "false");

    setTimeout(() => ta.focus(), 0);

    document.addEventListener("keydown", onEsc);
  }

  function closeModal() {
    modal.classList.remove("is-open");

    modal.setAttribute("aria-hidden", "true");

    document.removeEventListener("keydown", onEsc);

    preview.innerHTML = "";

    replaceFile = null;

    removeMedia = false;

    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }
  }

  function onEsc(e) {
    if (e.key === "Escape") closeModal();
  }

  closeEls.forEach((el) => el.addEventListener("click", closeModal));

  // ------- プレビュー -------

  function renderPreview() {
    preview.innerHTML = "";

    if (removeMedia) {
      const p = document.createElement("div");
      p.textContent = "（メディアは削除されます）";

      preview.appendChild(p);

      return;
    }

    if (replaceFile && objectUrl) {
      if (replaceFile.type.startsWith("image/")) {
        const img = document.createElement("img");
        img.src = objectUrl;
        preview.appendChild(img);
      } else if (replaceFile.type.startsWith("video/")) {
        const v = document.createElement("video");
        v.controls = true;
        v.src = objectUrl;
        preview.appendChild(v);
      } else {
        const p = document.createElement("div");
        p.textContent = "（このファイルはプレビューできません）";

        preview.appendChild(p);
      }

      return;
    }

    const p = document.createElement("div");
    p.textContent = "（メディアなし）";

    preview.appendChild(p);
  }

  // ------- モーダル内ファイル操作（選択/削除） -------

  btnPick?.addEventListener("click", () => fileInput?.click());

  fileInput?.addEventListener("change", () => {
    removeMedia = false;

    const file = fileInput.files?.[0] || null;

    replaceFile = file;

    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }

    if (file) objectUrl = URL.createObjectURL(file);

    renderPreview();
  });

  btnRemove?.addEventListener("click", () => {
    removeMedia = true;

    replaceFile = null;

    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }

    renderPreview();
  });

  // ------- ボタン動作（見た目だけ・処理なし） -------

  btnSave?.addEventListener("click", () => {
    /* no-op */ closeModal();
  });

  btnPost?.addEventListener("click", () => {
    /* no-op */ closeModal();
  });

  btnDelete?.addEventListener("click", () => {
    /* no-op */ closeModal();
  });

  // ------- フィード内「編集」ボタン -> 編集モードで開く（見た目だけ） -------

  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".post .actions button");

    if (!btn) return;

    const post = btn.closest(".post");

    if (!post) return;

    const textEl = post.querySelector("p");

    const mediaEl = post.querySelector("img.contents, video.contents");

    openForEdit({
      text: textEl ? (textEl.textContent || "").trim() : "",

      mediaEl,
    });
  });
})();

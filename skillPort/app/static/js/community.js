/* ===========================
 * Header active state
 * =========================== */
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('#header .container');
  if (!container) return;
  const links = container.querySelectorAll('ul li a');

  function clearActive() { links.forEach(a => a.classList.remove('is-active')); }

  links.forEach(a => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const wasActive = a.classList.contains('is-active');
      clearActive();
      if (!wasActive) a.classList.add('is-active');
    });
  });

  document.addEventListener('click', (e) => {
    if (!container.contains(e.target)) clearActive();
  });
});

/* ===========================
 * Dropdown (カテゴリ)
 * =========================== */
document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.getElementById("nav-category");
  if (!dropdown) return;
  const toggle = dropdown.querySelector(".dropdown-toggle");
  if (!toggle) return;

  toggle.addEventListener("click", (e) => {
    e.preventDefault();
    dropdown.classList.toggle("open");
  });

  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) dropdown.classList.remove("open");
  });
});

/* ===========================
 * Helpers (CSRF, file -> dataURL)
 * =========================== */
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute('value') || meta.getAttribute('content') : null;
}

function fileToDataURL(file) {
  return new Promise((resolve, reject) => {
    if (!file) return resolve('');
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result || '');
    reader.onerror = (e) => reject(e);
    reader.readAsDataURL(file);  // "data:image/...;base64,xxx"
  });
}

/* ===========================
 * New Post composer (+ preview)
 * =========================== */
document.addEventListener('DOMContentLoaded', () => {
  const newPost = document.querySelector('.new-post');
  if (!newPost) return;

  const btnAdd     = newPost.querySelector('.add');
  const btnSend    = newPost.querySelector('.send');
  const inputText  = newPost.querySelector('.textbox .text');
  const filePick   = newPost.querySelector('.filepick');
  const attachment = newPost.querySelector('.textbox .attachment');
  const textbox    = newPost.querySelector('.textbox');
  const avatarEl   = newPost.querySelector('.avatar');

  // Safety: avoid accidental submit
  if (btnSend) btnSend.setAttribute('type', 'button');

  let objectUrl = null;

  // ＋ -> ファイル選択
  if (btnAdd) {
    btnAdd.addEventListener('click', (e) => {
      e.preventDefault();
      if (filePick) filePick.click();
    });
  }

  // プレビュー表示
  if (filePick) {
    filePick.addEventListener('change', () => {
      const file = filePick.files && filePick.files[0];
      if (!file) return;

      if (objectUrl) URL.revokeObjectURL(objectUrl);
      objectUrl = URL.createObjectURL(file);

      const isImg = file.type.startsWith('image/');
      const isVid = file.type.startsWith('video/');

      if (isImg) {
        attachment.innerHTML = `
          <img src="${objectUrl}" style="width:100%;max-height:220px;border-radius:8px;display:block;">
          <button class="remove-btn" title="削除">✖</button>
        `;
      } else if (isVid) {
        attachment.innerHTML = `
          <video controls src="${objectUrl}" style="width:100%;max-height:220px;border-radius:8px;display:block;"></video>
          <button class="remove-btn" title="削除">✖</button>
        `;
      } else {
        attachment.innerHTML = `
          <div>このファイル形式はプレビューできません</div>
          <button class="remove-btn" title="削除">✖</button>
        `;
      }

      textbox.classList.add('has-attachment');

      const removeBtn = attachment.querySelector('.remove-btn');
      if (removeBtn) {
        removeBtn.addEventListener('click', () => {
          attachment.innerHTML = '';
          textbox.classList.remove('has-attachment');
          filePick.value = '';
          if (objectUrl) { URL.revokeObjectURL(objectUrl); objectUrl = null; }
        });
      }
    });
  }

  // ▶ 投稿 -> 「新規投稿」モードでモーダルを開く
  if (btnSend) {
    btnSend.addEventListener('click', async (e) => {
      e.preventDefault();

      // モーダルAPIが用意できていない場合のフォールバック
      if (!window.CommunityModal || typeof window.CommunityModal.openForCreate !== 'function') {
        const fallback = document.getElementById('editModal');
        if (fallback) {
          const h = fallback.querySelector('.modal__header h3');
          if (h) h.textContent = '本当に投稿しますか';
          const postBtn = fallback.querySelector('#btnPostSubmit');
          const saveBtn = fallback.querySelector('#btnSaveEdit');
          const delBtn  = fallback.querySelector('#btnDeletePost');
          if (postBtn) postBtn.style.display = 'inline-block';
          if (saveBtn) saveBtn.style.display = 'none';
          if (delBtn)  delBtn.style.display  = 'none';
          fallback.classList.add('is-open');
        }
        return;
      }

      const file = filePick && filePick.files && filePick.files[0] ? filePick.files[0] : null;

      window.CommunityModal.openForCreate({
        text: inputText ? inputText.value.trim() : '',
        file,
        avatarSrc: avatarEl?.src || '',
        username: 'You'
      });
    });
  }

  // GC
  window.addEventListener('beforeunload', () => {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
  });
});

/* ===========================
 * 編集/作成 共通ポップアップ（Flask連携版）
 * =========================== */
(function(){
  const modal        = document.getElementById('editModal');
  if (!modal) return;

  const ta           = modal.querySelector('#editText');
  const fileInput    = modal.querySelector('#editFile');
  const btnPick      = modal.querySelector('#btnPickMedia');
  const btnRemove    = modal.querySelector('#btnRemoveMedia');
  const preview      = modal.querySelector('#mediaPreview');

  // 分離ボタン
  const btnSave      = modal.querySelector('#btnSaveEdit');     // 編集用
  const btnPost      = modal.querySelector('#btnPostSubmit');   // 新規用
  const btnDelete    = modal.querySelector('#btnDeletePost');
  const closeEls     = modal.querySelectorAll('[data-close="true"]');

  let activePost     = null;   // 編集対象。新規は null
  let lastFocus      = null;
  let objectUrl      = null;
  let replaceFile    = null;   // File | null
  let removeMedia    = false;
  let keepObjectUrl  = false;
  let createContext  = null;

  const POST_URL = '/community/upload_post'; // Flask 側のエンドポイント

  function getPostParts(post){
    const actions = post.querySelector('.actions');
    let textEl = actions ? actions.previousElementSibling : null;
    if (!textEl || textEl.tagName !== 'P') textEl = post.querySelector('p');
    let mediaEl = post.querySelector('.contents');
    return { textEl, mediaEl, actions };
  }

  /* ------- 表示切替 ------- */
  function showForEditMode(){
    modal.querySelector('.modal__header h3').textContent = '投稿を編集';
    if (btnSave)   btnSave.style.display   = 'inline-block';
    if (btnPost)   btnPost.style.display   = 'none';
    if (btnDelete) btnDelete.style.display = 'inline-block';

    if (btnSave)   btnSave.onclick   = handleSaveEdit;
    if (btnPost)   btnPost.onclick   = null;
    if (btnDelete) btnDelete.onclick = handleDeletePost;
  }

  function showForCreateMode(){
    modal.querySelector('.modal__header h3').textContent = '本当に投稿しますか';
    if (btnSave)   btnSave.style.display   = 'none';
    if (btnPost)   btnPost.style.display   = 'inline-block';
    if (btnDelete) btnDelete.style.display = 'none';

    if (btnSave)   btnSave.onclick   = null;
    if (btnPost)   btnPost.onclick   = handleCreatePostViaFlask;
    if (btnDelete) btnDelete.onclick = null;
  }

  /* ------- Open: 編集POP ------- */
  function openModalFor(post){
    // activePost    = post;
    // createContext = null;
    // lastFocus     = document.activeElement;
    // replaceFile   = null;
    // removeMedia   = false;
    // keepObjectUrl = false;
    if (objectUrl){ URL.revokeObjectURL(objectUrl); objectUrl = null; }

    const { textEl, mediaEl } = getPostParts(post);
    ta.value = textEl ? (textEl.textContent || '').trim() : '';

    renderPreview(mediaEl ? mediaEl.tagName.toLowerCase() : null, mediaEl ? mediaEl.getAttribute('src') : null);

    showForEditMode();

    modal.classList.add('is-open');
    setTimeout(()=>ta.focus(), 0);
    document.addEventListener('keydown', onKeydown);
  }

  /* ------- Open: 新規 ------- */
  function openModalForNew(draft){
    activePost    = null;
    createContext = {
      avatarSrc: draft?.avatarSrc || '',
      username:  draft?.username  || 'You'
    };
    lastFocus     = document.activeElement;
    replaceFile   = draft?.file || null;
    removeMedia   = false;
    keepObjectUrl = false;
    if (objectUrl){ URL.revokeObjectURL(objectUrl); objectUrl = null; }

    ta.value = (draft?.text || '').trim();

    if (replaceFile) {
      objectUrl = URL.createObjectURL(replaceFile);
    }

    renderPreview(null, null);
    showForCreateMode();

    modal.classList.add('is-open');
    setTimeout(()=>ta.focus(), 0);
    document.addEventListener('keydown', onKeydown);
  }

  // 外部API
  window.CommunityModal = {
    openForEdit:   openModalFor,
    openForCreate: openModalForNew
  };

  /* ------- Close ------- */
  function closeModal(){
    modal.classList.remove('is-open');
    document.removeEventListener('keydown', onKeydown);
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();

    activePost    = null;
    replaceFile   = null;
    removeMedia   = false;
    createContext = null;

    if (objectUrl && !keepObjectUrl){ URL.revokeObjectURL(objectUrl); }
    objectUrl     = null;
    keepObjectUrl = false;
    preview.innerHTML = '';
  }

  function onKeydown(e){
    if (e.key === 'Escape'){ e.preventDefault(); closeModal(); }
    if (e.key === 'Tab'){
      const f = modal.querySelectorAll('button,[href],input,textarea,select,[tabindex]:not([tabindex="-1"])');
      const a = Array.from(f).filter(el => !el.disabled);
      if (!a.length) return;
      const first = a[0], last = a[a.length-1];
      if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
  }

  /* ------- Preview ------- */
  function renderPreview(kind, src){
    preview.innerHTML = '';
    if (removeMedia){
      const p = document.createElement('div');
      p.textContent = '（メディアは削除されます）';
      preview.appendChild(p);
      return;
    }
    if (replaceFile && objectUrl){
      if (replaceFile.type.startsWith('image/')){
        const img = document.createElement('img'); img.src = objectUrl; preview.appendChild(img);
      }else if (replaceFile.type.startsWith('video/')){
        const v = document.createElement('video'); v.controls = true; v.src = objectUrl; preview.appendChild(v);
      }else{
        const p = document.createElement('div');
        p.textContent = '（このファイルはプレビューできません）';
        preview.appendChild(p);
      }
      return;
    }
    if (src && kind === 'img'){
      const img = document.createElement('img'); img.src = src; preview.appendChild(img);
    }else if (src && kind === 'video'){
      const v = document.createElement('video'); v.controls = true; v.src = src; preview.appendChild(v);
    }else{
      const p = document.createElement('div');
      p.textContent = '（メディアなし）';
      preview.appendChild(p);
    }
  }

  /* ------- Modal 内ファイル操作 ------- */
  if (btnPick) {
    btnPick.addEventListener('click', ()=> fileInput && fileInput.click());
  }
  if (fileInput) {
    fileInput.addEventListener('change', ()=>{
      removeMedia = false;
      const file = fileInput.files && fileInput.files[0];
      if (!file) {
        replaceFile = null;
        if (objectUrl){URL.revokeObjectURL(objectUrl); objectUrl=null;}
        renderPreview(null,null);
        return;
      }
      replaceFile = file;
      if (objectUrl){ URL.revokeObjectURL(objectUrl); }
      objectUrl = URL.createObjectURL(file);
      renderPreview(null, null);
    });
  }

  if (btnRemove) {
    btnRemove.addEventListener('click', ()=>{
      removeMedia = true;
      replaceFile = null;
      if (objectUrl){ URL.revokeObjectURL(objectUrl); objectUrl=null; }
      renderPreview(null, null);
    });
  }

  /* ==========================================================
   * Flaskへ送信（新規投稿）
   *   - endpoint: POST /community/upload_post
   *   - form fields:
   *       post_text: string
   *       upload_media: string (dataURL or "")
   *   - success: reload to reflect server-rendered list
   * ========================================================== */
  async function handleCreatePostViaFlask(){
    const textVal = (ta.value || '').trim();
    // dataURL or ""（モーダルで replaceFile を選んだ場合を優先）
    let dataUrl = '';
    if (!removeMedia && replaceFile) {
      try {
        dataUrl = await fileToDataURL(replaceFile);
      } catch (e) {
        console.error('Failed to read media file:', e);
        dataUrl = '';
      }
    }

    const params = new URLSearchParams();
    params.set('post_text', textVal);
    params.set('upload_media', dataUrl || ""); // Flask側："" のとき None 扱い

    const headers = { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' };
    const csrf = getCsrfToken();
    if (csrf) headers['X-CSRFToken'] = csrf;

    try {
      const res = await fetch('/community/upload_post', {
        method: 'POST',
        headers,
        body: params.toString(),
        credentials: 'same-origin'
      });
      if (!res.ok) {
        console.error('Upload failed:', res.status, await res.text());
        alert('投稿に失敗しました。時間をおいて再度お試しください。');
        return;
      }
      // サーバでレンダリングされた最新一覧に更新
      window.location.href = '/community/top';
    } catch (err) {
      console.error('Upload error:', err);
      alert('ネットワークエラーが発生しました。');
    } finally {
      closeModal();
    }
  }

  /* ------- 既存の編集はクライアント内だけ更新（バックエンド未提供のため） ------- */
  function handleDeletePost(){
    if (!activePost) return;
    const ok = window.confirm('この投稿を削除しますか？この操作は取り消せません。');
    if (!ok) return;
    activePost.remove();
    closeModal();
  }

  function handleSaveEdit(){
    const textVal = ta.value.trim();
    if (!activePost){ closeModal(); return; }

    const { textEl, mediaEl, actions } = getPostParts(activePost);

    if (textEl) textEl.textContent = textVal;
    else {
      const p = document.createElement('p');
      p.textContent = textVal;
      p.style.marginLeft = '49px';
      if (actions) activePost.insertBefore(p, actions);
      else activePost.appendChild(p);
    }

    if (removeMedia) {
      if (mediaEl) mediaEl.remove();
    } else if (replaceFile) {
      const isImg  = replaceFile.type.startsWith('image/');
      const isVid  = replaceFile.type.startsWith('video/');
      if (!isImg && !isVid) { closeModal(); return; }

      let target = mediaEl;
      if (!target){
        target = document.createElement(isImg ? 'img' : 'video');
        target.className = 'contents';
        target.style.marginLeft = '49px';
        const pAfter = getPostParts(activePost).textEl;
        if (pAfter) pAfter.insertAdjacentElement('afterend', target);
        else activePost.prepend(target);
      } else {
        const needNew = (isImg && target.tagName.toLowerCase() !== 'img') ||
                        (isVid && target.tagName.toLowerCase() !== 'video');
        if (needNew){
          const newEl = document.createElement(isImg ? 'img' : 'video');
          newEl.className = 'contents';
          newEl.style.marginLeft = '49px';
          target.replaceWith(newEl);
          target = newEl;
        }
      }
      // ここはプレビュー用に objectUrl を使うだけ（編集はローカル反映）
      if (!objectUrl) objectUrl = URL.createObjectURL(replaceFile);
      target.src = objectUrl || target.src;
      if (isVid) target.controls = true;
    }

    closeModal();
  }

  /* ------- フィード内「編集」から編集モード起動 ------- */
  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('.post .actions button');
    if (!btn) return;
    const post = btn.closest('.post');
    if (!post) return;
    openModalFor(post);
  });

  /* ------- 閉じる ------- */
  closeEls.forEach(el => el.addEventListener('click', closeModal));
  modal.addEventListener('click', (e)=>{ if (e.target.dataset && e.target.dataset.close === 'true') closeModal(); });

  /* ------- GC ------- */
  window.addEventListener('beforeunload', ()=>{
    if (objectUrl && !keepObjectUrl) URL.revokeObjectURL(objectUrl);
  });
})();

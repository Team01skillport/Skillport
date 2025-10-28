//  投稿フィード ----------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    const newPost = document.querySelector('.new-post');
    if (!newPost) return;
  
    const btnAdd     = newPost.querySelector('.add');
    const inputText  = newPost.querySelector('.textbox .text');
    const filePick   = newPost.querySelector('.filepick');
    const attachment = newPost.querySelector('.textbox .attachment');
    const textbox    = newPost.querySelector('.textbox');
  
    let objectUrl = null;
  
    // Click ＋ => open file picker
    btnAdd.addEventListener('click', (e) => {
      e.preventDefault();
      filePick.click();
    });
  
    // When a video is selected
    filePick.addEventListener('change', () => {
      const file = filePick.files && filePick.files[0];
      if (!file) return;
  
      // Revoke previous URL if any
      if (objectUrl) URL.revokeObjectURL(objectUrl);
      objectUrl = URL.createObjectURL(file);
  
      // Inject preview + ✖ button (no filename logic anymore)
      attachment.innerHTML = `
        <video controls src="${objectUrl}"></video>
        <button class="remove-btn" title="削除">✖</button>
      `;
      textbox.classList.add('has-attachment');
  
      // ✖ remove button logic
      attachment.querySelector('.remove-btn').addEventListener('click', () => {
        attachment.innerHTML = '';
        textbox.classList.remove('has-attachment');
        filePick.value = '';
        if (objectUrl) {
          URL.revokeObjectURL(objectUrl);
          objectUrl = null;
        }
      });
    });
  
    // No text-related deletion logic anymore
  
    window.addEventListener('beforeunload', () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    });
  });



  //編集popup ---------------------------------------------

  /* ============ 編集ポップアップ（テキスト＋画像/動画） ============ */
(function(){
  const modal        = document.getElementById('editModal');
  if (!modal) return;

  const ta           = modal.querySelector('#editText');
  const fileInput    = modal.querySelector('#editFile');
  const btnPick      = modal.querySelector('#btnPickMedia');
  const btnRemove    = modal.querySelector('#btnRemoveMedia');
  const preview      = modal.querySelector('#mediaPreview');
  const btnSave      = modal.querySelector('#btnSaveEdit');
  const closeEls     = modal.querySelectorAll('[data-close="true"]');

  let activePost     = null;
  let lastFocus      = null;
  let objectUrl      = null;
  let replaceFile    = null;   // File or null
  let removeMedia    = false;  // true if user chose to remove

  // Find elements inside a post (robust to your current HTML)
  function getPostParts(post){
    const actions = post.querySelector('.actions');
    // text paragraph = the <p> just before .actions, else first <p>
    let textEl = actions ? actions.previousElementSibling : null;
    if (!textEl || textEl.tagName !== 'P') textEl = post.querySelector('p');
    // media = <img class="contents"> or <video class="contents">
    let mediaEl = post.querySelector('.contents');
    return { textEl, mediaEl, actions };
  }

  function openModalFor(post){
    activePost = post;
    lastFocus  = document.activeElement;
    replaceFile = null;
    removeMedia = false;
    if (objectUrl){ URL.revokeObjectURL(objectUrl); objectUrl = null; }

    const { textEl, mediaEl } = getPostParts(post);
    ta.value = textEl ? (textEl.textContent || '').trim() : '';

    // render current media preview
    renderPreview(mediaEl ? mediaEl.tagName.toLowerCase() : null, mediaEl ? mediaEl.getAttribute('src') : null);

    modal.classList.add('is-open');
    setTimeout(()=>ta.focus(), 0);
    document.addEventListener('keydown', onKeydown);
  }

  function closeModal(){
    modal.classList.remove('is-open');
    document.removeEventListener('keydown', onKeydown);
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    activePost = null;
    replaceFile = null;
    removeMedia = false;
    if (objectUrl){ URL.revokeObjectURL(objectUrl); objectUrl = null; }
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

  // File select
  btnPick.addEventListener('click', ()=> fileInput.click());
  fileInput.addEventListener('change', ()=>{
    removeMedia = false; // selecting a new file cancels removal
    const file = fileInput.files && fileInput.files[0];
    if (!file) { replaceFile = null; if (objectUrl){URL.revokeObjectURL(objectUrl); objectUrl=null;} renderPreview(null,null); return; }
    replaceFile = file;
    if (objectUrl){ URL.revokeObjectURL(objectUrl); }
    objectUrl = URL.createObjectURL(file);
    renderPreview(null, null);
  });

  // Remove media
  btnRemove.addEventListener('click', ()=>{
    removeMedia = true;
    replaceFile = null;
    if (objectUrl){ URL.revokeObjectURL(objectUrl); objectUrl=null; }
    renderPreview(null, null);
  });

  // Save
  btnSave.addEventListener('click', ()=>{
    if (!activePost) return;
    const { textEl, mediaEl, actions } = getPostParts(activePost);

    // 1) update text
    if (textEl) textEl.textContent = ta.value.trim();
    else {
      // create a new <p> before .actions if none exists
      const p = document.createElement('p');
      p.textContent = ta.value.trim();
      p.style.marginLeft = '49px'; // keep your layout
      if (actions) activePost.insertBefore(p, actions);
      else activePost.appendChild(p);
    }

    // 2) update media
    if (removeMedia) {
      if (mediaEl) mediaEl.remove();
    } else if (replaceFile) {
      // create or replace .contents
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
        // if tag mismatch (img -> video or vice versa), replace element
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
      // assign src
      target.src = objectUrl || target.src;
      if (isVid) target.controls = true;
    }
    closeModal();
  });

  // Open (delegated): click any 「編集」 button inside .post .actions
  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('.post .actions button');
    if (!btn) return;
    const post = btn.closest('.post');
    if (!post) return;
    openModalFor(post);
  });

  // Close (overlay, ×, キャンセル)
  closeEls.forEach(el => el.addEventListener('click', closeModal));
  modal.addEventListener('click', (e)=>{ if (e.target.dataset.close === 'true') closeModal(); });

  // Cleanup on unload
  window.addEventListener('beforeunload', ()=>{ if (objectUrl) URL.revokeObjectURL(objectUrl); });
})();


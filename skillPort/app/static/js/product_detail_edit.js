// ===== 商品詳細編集ページ用スクリプト =====
document.addEventListener('DOMContentLoaded', () => {

  /* 文字数カウンター：商品名 */
  const titleInput = document.getElementById('titleInput');
  const titleCount = document.getElementById('titleCount');
  if (titleInput && titleCount) {
    const update = () => (titleCount.textContent = String(titleInput.value.length));
    titleInput.addEventListener('input', update);
    update();
  }

  /* 価格 → 手数料／利益の自動計算 */
  const priceInput  = document.getElementById('priceInput');
  const feeValue    = document.getElementById('feeValue');
  const profitValue = document.getElementById('profitValue');
  const feeRateLabel= document.getElementById('feeRateLabel');

  // 手数料率（％）※必要に応じて変更可
  const FEE_RATE = 10;
  if (feeRateLabel) feeRateLabel.textContent = `${FEE_RATE}%`;

  const calc = () => {
    const price = Number(priceInput?.value || 0);
    const fee   = Math.floor(price * FEE_RATE / 100);
    const profit= Math.max(0, price - fee);
    if (feeValue)    feeValue.textContent = fee.toLocaleString();
    if (profitValue) profitValue.textContent = profit.toLocaleString();
  };
  if (priceInput) {
    ['input','change','keyup'].forEach(ev => priceInput.addEventListener(ev, calc));
    calc();
  }

  /* 詳細：カテゴリ編集の開閉と保存 */
  const editCatBtn = document.getElementById('editCatBtn');
  const catEdit    = document.getElementById('catEdit');
  const catSave    = document.getElementById('catSave');
  const catText    = document.getElementById('catText');
  const catLv1     = document.getElementById('catLv1');
  const catLv2     = document.getElementById('catLv2');
  const catLv3     = document.getElementById('catLv3');

  editCatBtn?.addEventListener('click', () => {
    catEdit.hidden = !catEdit.hidden;
  });
  catSave?.addEventListener('click', () => {
    const lv1 = catLv1.value, lv2 = catLv2.value, lv3 = catLv3.value;
    catText.textContent = `${lv1} ＞ ${lv2} ＞ ${lv3}`;
    catEdit.hidden = true;
  });

  /* 詳細：商品の状態の保存 */
  const editCondBtn = document.getElementById('editCondBtn');
  const condEdit    = document.getElementById('condEdit');
  const condSave    = document.getElementById('condSave');
  const condSelect  = document.getElementById('condSelect');
  const condMore    = document.getElementById('condMore');
  const condText    = document.getElementById('condText');

  editCondBtn?.addEventListener('click', () => {
    condEdit.hidden = !condEdit.hidden;
  });
  condSave?.addEventListener('click', () => {
    const main = condSelect.value;
    const extra= condMore.value.trim();
    condText.textContent = extra ? `${main}・${extra}` : main;
    condEdit.hidden = true;
  });

  /* 画像追加（クリック／複数選択／ドラッグ＆ドロップ対応） */
  const imageGrid  = document.getElementById('imageGrid');
  const imageInput = document.getElementById('imageInput');
  const addBtns    = [document.getElementById('addImageBtn'), document.getElementById('addImageBtn2')];

  const MAX_IMAGES = 20;
  const currentCount = () => imageGrid.querySelectorAll('.pd-thumb img').length;

  // ファイル選択 → プレビュー追加
  const handleFiles = async (files) => {
    for (const file of files) {
      if (!file.type.startsWith('image/')) continue;
      if (currentCount() >= MAX_IMAGES) break;

      const url = URL.createObjectURL(file);
      const el  = document.createElement('div');
      el.className = 'pd-thumb';
      el.innerHTML = `<img src="${url}" alt="thumb">`;
      imageGrid.insertBefore(el, addBtns[0]); // 追加ボタンの前に挿入
    }
  };

  // クリックでファイル選択
  addBtns.forEach(btn => btn?.addEventListener('click', () => imageInput.click()));
  imageInput?.addEventListener('change', (e) => handleFiles(e.target.files));

  // D&D で追加
  ['dragenter','dragover'].forEach(evt => {
    imageGrid.addEventListener(evt, e => { e.preventDefault(); e.dataTransfer.dropEffect='copy'; }, false);
  });
  imageGrid.addEventListener('drop', e => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  });

  /* 操作ボタン（ダミー挙動） */
  document.getElementById('saveBtn')?.addEventListener('click', () => alert('変更内容を保存しました（ダミー）'));
  document.getElementById('pauseBtn')?.addEventListener('click', () => alert('この商品の出品を一時停止しました（ダミー）'));
  document.getElementById('deleteBtn')?.addEventListener('click', () => {
    if (confirm('本当に削除しますか？（ダミー）')) alert('削除しました（ダミー）');
  });
});
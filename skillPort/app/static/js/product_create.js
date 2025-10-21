// ===== 出品商品登録ページ用スクリプト =====
document.addEventListener('DOMContentLoaded', () => {

  /* 商品名の文字数カウンター */
  const titleInput = document.getElementById('titleInput');
  const titleCount = document.getElementById('titleCount');
  const titleError = document.getElementById('titleError');
  const updateTitleCount = () => (titleCount.textContent = String(titleInput.value.length));
  titleInput.addEventListener('input', () => {
    updateTitleCount();
    if (titleInput.value.trim()) titleError.hidden = true;
  });
  updateTitleCount();

  /* 価格 → 手数料／利益の自動計算 */
  const priceInput  = document.getElementById('priceInput');
  const priceError  = document.getElementById('priceError');
  const feeValue    = document.getElementById('feeValue');
  const profitValue = document.getElementById('profitValue');
  const feeRateLabel= document.getElementById('feeRateLabel');
  const FEE_RATE = 10; // 手数料率（%）
  feeRateLabel.textContent = `${FEE_RATE}%`;

  const recalc = () => {
    const price = Number(priceInput.value || 0);
    const fee   = Math.floor(price * FEE_RATE / 100);
    const profit= Math.max(0, price - fee);
    feeValue.textContent    = fee.toLocaleString();
    profitValue.textContent = profit.toLocaleString();
    if (price > 0) priceError.hidden = true;
  };
  ['input','change','keyup'].forEach(ev => priceInput.addEventListener(ev, recalc));
  recalc();

  /* カテゴリ／状態の入力確認 */
  const catError = document.getElementById('catError');
  const condError= document.getElementById('condError');
  const catLv1 = document.getElementById('catLv1');
  const catLv2 = document.getElementById('catLv2');
  const catLv3 = document.getElementById('catLv3');
  const condSelect = document.getElementById('condSelect');

  const categoryValid = () =>
    catLv1.value && catLv2.value && catLv3.value;
  const conditionValid = () => !!condSelect.value;

  [catLv1, catLv2, catLv3].forEach(el => el.addEventListener('change', () => catError.hidden = categoryValid()));
  condSelect.addEventListener('change', () => condError.hidden = conditionValid());

  /* 画像追加（クリック／複数／ドラッグ＆ドロップ） */
  const imageGrid  = document.getElementById('imageGrid');
  const imageInput = document.getElementById('imageInput');
  const addBtns    = [document.getElementById('addImageBtn'), document.getElementById('addImageBtn2')];

  const MAX_IMAGES = 20;
  const currentCount = () => imageGrid.querySelectorAll('.pc-thumb img').length;

  const handleFiles = (files) => {
    for (const file of files) {
      if (!file.type.startsWith('image/')) continue;
      if (currentCount() >= MAX_IMAGES) break;
      const url = URL.createObjectURL(file);
      const el  = document.createElement('div');
      el.className = 'pc-thumb';
      el.innerHTML = `<img src="${url}" alt="thumb">`;
      imageGrid.insertBefore(el, imageGrid.querySelector('.add-slot')); // 先頭スロットの前に差し込む
    }
  };

  addBtns.forEach(btn => btn.addEventListener('click', () => imageInput.click()));
  imageInput.addEventListener('change', (e) => handleFiles(e.target.files));

  ['dragenter','dragover'].forEach(evt => {
    imageGrid.addEventListener(evt, e => { e.preventDefault(); e.dataTransfer.dropEffect='copy'; }, false);
  });
  imageGrid.addEventListener('drop', e => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  });

  /* 操作ボタン（登録／下書き保存／クリア） */
  const createBtn = document.getElementById('createBtn');
  const draftBtn  = document.getElementById('draftBtn');
  const clearBtn  = document.getElementById('clearBtn');

  // 入力チェック（最小限）
  const validate = () => {
    let ok = true;
    if (!titleInput.value.trim()) { titleError.hidden = false; ok = false; }
    if (!(catLv1.value && catLv2.value && catLv3.value)) { catError.hidden = false; ok = false; }
    if (!condSelect.value) { condError.hidden = false; ok = false; }
    if (!priceInput.value || Number(priceInput.value) <= 0) { priceError.hidden = false; ok = false; }
    return ok;
  };

  createBtn.addEventListener('click', () => {
    if (!validate()) { window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
    alert('商品を登録しました（ダミー）');
  });

  draftBtn.addEventListener('click', () => {
    alert('下書きとして保存しました（ダミー）');
  });

  clearBtn.addEventListener('click', () => {
    if (!confirm('入力内容をクリアしますか？')) return;
    document.querySelectorAll('input[type="text"], input[type="number"]').forEach(i => i.value = '');
    document.querySelectorAll('select').forEach(s => s.value = '');
    document.getElementById('descInput').value = '';
    imageGrid.querySelectorAll('.pc-thumb img').forEach(img => img.parentElement.remove());
    // 表示更新
    titleCount.textContent = '0';
    feeValue.textContent = '0';
    profitValue.textContent = '0';
    [titleError, catError, condError, priceError].forEach(e => e.hidden = true);
  });
});
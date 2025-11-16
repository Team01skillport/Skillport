document.addEventListener('DOMContentLoaded', () => {

  // ==========================================================
  // 1. 变量定义与 DOM 元素获取
  // ==========================================================
  const select = document.getElementById('paymentSelect');
  const sumPayment = document.getElementById('sumPayment');
  const buyButton = document.getElementById('btnPurchase');

  const addressModal = document.getElementById('addressModal');
  const btnEditAddress = document.getElementById('btnEditAddress');
  const btnAddAddress = document.getElementById('btnAddAddress');
  const btnCancelAddress = document.getElementById('btnCancelAddress');
  const addressForm = document.getElementById('addressForm');
  const addressDisplay = document.getElementById('shippingAddressDisplay');

  const paymentModal = document.getElementById('paymentModal');
  const btnEditPayment = document.getElementById('btnEditPayment');
  const btnCancelPayment = document.getElementById('btnCancelPayment');
  const paymentForm = document.getElementById('paymentForm');
  
  // [已修改] 获取表单和切换器
  const creditForm = document.getElementById('creditCardForm');
  const bankForm = document.getElementById('bankAccountForm');
  const paymentTypeSelector = paymentModal.querySelector(".payment-type-selector");
  const labelCredit = document.getElementById('labelCredit');
  const labelBank = document.getElementById('labelBank');

  const btnOpenModalCredit = document.getElementById('btnOpenModalCredit');
  const btnOpenModalBank = document.getElementById('btnOpenModalBank');
  
  const cardNumInput = document.getElementById('card_num');
  const cardNameInput = document.getElementById('card_name');
  const cardExpInput = document.getElementById('card_expiration');
  const bankAccNumInput = document.getElementById('bank_account_num');


  // ==========================================================
  // 2. 支付总览显示同步
  // ==========================================================
  const syncPaymentDisplay = () => {
    if (!select || !sumPayment) return;
    const selectedOption = select.options[select.selectedIndex];

    if (selectedOption && selectedOption.value !== "") {
      sumPayment.textContent = selectedOption.textContent.split('(')[0].trim();
    } else if (document.getElementById('noPaymentOption')) {
      sumPayment.textContent = "支払い方法がありません";
    } else {
      sumPayment.textContent = "---";
    }
  };

  if (select && sumPayment) {
    select.addEventListener('change', syncPaymentDisplay);
    syncPaymentDisplay();
  }

  // ==========================================================
  // 3. 购买动作
  // ==========================================================
  buyButton?.addEventListener('click', async () => {
    buyButton.disabled = true;
    buyButton.textContent = '処理中...';

    if (select && (!select.value || document.getElementById('noPaymentOption'))) {
        alert('支払い方法を選択または登録してください。');
        buyButton.disabled = false;
        buyButton.textContent = '購入する';
        return;
    }

    const pathParts = window.location.pathname.split('/');
    const productIdIndex = pathParts.indexOf('product') + 1;
    const productId = (productIdIndex > 0) ? pathParts[productIdIndex] : null;

    if (!productId) {
        alert('エラー：商品IDが見つかりません。');
        buyButton.disabled = false;
        buyButton.textContent = '購入する';
        return;
    }

    try {
        const response = await fetch(`/market/product/${productId}/purchase`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
        });
        const data = await response.json();

        if (data.success) {
            alert('購入が完了しました。ありがとうございます！');
            window.location.href = data.redirect_url;
        } else {
            alert('購入に失敗しました： ' + data.error);
            buyButton.disabled = false;
            buyButton.textContent = '購入する';
        }
    } catch (error) {
        console.error('Purchase error:', error);
        alert('購入処理中にエラーが発生しました。');
        buyButton.disabled = false;
        buyButton.textContent = '購入する';
    }
  });

  // ==========================================================
  // 4. 配送地址模态框逻辑
  // ==========================================================
  const openAddressModal = (e) => {
    e.preventDefault();
    if (addressModal) addressModal.classList.add('active');
  };
  const closeAddressModal = (e) => {
    e.preventDefault();
    if (addressModal) addressModal.classList.remove('active');
  };

  btnEditAddress?.addEventListener('click', openAddressModal);
  btnAddAddress?.addEventListener('click', openAddressModal);
  btnCancelAddress?.addEventListener('click', closeAddressModal);

  addressForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const saveBtn = addressForm.querySelector('button[type="submit"]'); 
    saveBtn.disabled = true;

    const formData = new FormData(addressForm);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch('/market/checkout/update_address', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      const result = await response.json();

      if (result.success) {
        const updatedData = result.updated_data;
        const currentNameHTML = addressDisplay.innerHTML.split('<br>')[0]; 
        
        addressDisplay.innerHTML = `
          ${currentNameHTML.includes('〒') ? '' : currentNameHTML + '<br />'}
          〒${updatedData.zip_code}<br />
          ${updatedData.prefecture || ''} ${updatedData.address1 || ''}<br />
          ${updatedData.address2 || ''}
        `;
        
        const addAddressLink = document.getElementById('btnAddAddress');
        if (addAddressLink) {
            const strongElement = addAddressLink.closest('strong');
            if (strongElement) {
                strongElement.parentElement.innerHTML = addressDisplay.innerHTML; 
            }
        }
        closeAddressModal(e);
      } else {
        alert('住所の保存に失敗しました： ' + result.error);
      }
    } catch (error) {
      console.error('Address update error:', error);
      alert('住所の更新中にエラーが発生しました。');
    } finally {
        saveBtn.disabled = false;
    }
  });

  // ==========================================================
  // 5. [已重写] 支付方法模态框逻辑 (修复 Bug)
  // ==========================================================
  
  const switchPaymentForm = (type) => {
    const radio = document.querySelector(`input[name="payment_type"][value="${type}"]`);
    if (radio) radio.checked = true;

    const allCreditFields = creditForm ? creditForm.querySelectorAll('input, select') : [];
    const allBankFields = bankForm ? bankForm.querySelectorAll('input, select') : [];
    
    if (type === 'credit') {
      creditForm?.classList.add('active');
      bankForm?.classList.remove('active');
      labelCredit?.classList.add('active');
      labelBank?.classList.remove('active'); // [Bug 修复] 移除银行的 active
      
      allCreditFields.forEach(el => el.setAttribute('required', ''));
      allBankFields.forEach(el => el.removeAttribute('required')); 
      
    } else { 
      creditForm?.classList.remove('active');
      bankForm?.classList.add('active');
      labelCredit?.classList.remove('active'); // [Bug 修复] 移除信用卡的 active
      labelBank?.classList.add('active');
      
      allCreditFields.forEach(el => el.removeAttribute('required')); 
      allBankFields.forEach(el => el.setAttribute('required', ''));
    }
  };

  const openPaymentModal = (e) => {
    e.preventDefault();
    paymentModal?.classList.add('active');
  };

  btnEditPayment?.addEventListener('click', openPaymentModal);
  
  btnOpenModalCredit?.addEventListener('click', (e) => {
    switchPaymentForm('credit');
    openPaymentModal(e);
  });
  btnOpenModalBank?.addEventListener('click', (e) => {
    switchPaymentForm('bank');
    openPaymentModal(e);
  });
  
  // [新增] 监听切换器本身的点击事件
  paymentTypeSelector?.addEventListener("click", (event) => {
    const targetLabel = event.target.closest('.payment-type-option');
    if (targetLabel) {
      const radioInput = targetLabel.querySelector('input[type="radio"]');
      if (radioInput && !radioInput.checked) {
        switchPaymentForm(radioInput.value);
      }
    }
  });

  btnCancelPayment?.addEventListener('click', (e) => {
    e.preventDefault();
    paymentModal?.classList.remove('active');
    paymentForm.reset();
    switchPaymentForm('credit'); 
  });

  paymentForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const currentType = paymentForm.querySelector('input[name="payment_type"]:checked')?.value;
    if (currentType) {
        switchPaymentForm(currentType); 
    }
    
    if (!paymentForm.checkValidity()) {
        paymentForm.reportValidity(); 
        return;
    }
    
    const saveBtn = paymentForm.querySelector('button[type="submit"]'); 
    saveBtn.disabled = true;

    const formData = new FormData(paymentForm);
    let data = Object.fromEntries(formData.entries()); 

    const activeType = data.payment_type;
    let relevantData = { 'payment_type': activeType };

    let activeFormElements = [];
    if (activeType === 'credit' && creditForm) {
      activeFormElements = creditForm.querySelectorAll('input, select');
    } else if (activeType === 'bank' && bankForm) {
      activeFormElements = bankForm.querySelectorAll('input, select');
    }

    activeFormElements.forEach(el => {
      let value = data[el.name];
      if (typeof value === 'string') {
          if (el.name === 'card_num' || el.name === 'bank_account_num') {
              value = value.replace(/\s/g, '');
          }
          if (el.name === 'card_name') {
              value = value.toUpperCase();
          }
          if (el.name === 'card_expiration') {
              value = value.replace('/', ''); 
          }
      }
      if (value !== undefined) { 
          relevantData[el.name] = value;
      }
    });

    data = relevantData;

    try {
      const response = await fetch('/market/checkout/add_payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Server returned status ${response.status}`);
      }
      
      const result = await response.json();

      if (result.success) {
        const newOption = document.createElement('option');
        newOption.value = result.new_payment.value;
        newOption.textContent = result.new_payment.text;
        newOption.selected = true;

        if (select) {
          select.appendChild(newOption);
          const noPaymentOption = document.getElementById('noPaymentOption');
          if (noPaymentOption) {
            const selectWrap = noPaymentOption.closest('.block')?.querySelector('.select-wrap');
            if (selectWrap) selectWrap.style.display = 'block';
            document.querySelector('.payment-add-buttons')?.remove();
            const blockHead = noPaymentOption.closest('.block')?.querySelector('.block-head');
            const linkEdit = document.getElementById('btnEditPayment');
            if (blockHead && linkEdit) blockHead.appendChild(linkEdit);
            noPaymentOption.remove();
          }
        }
        
        paymentModal.classList.remove('active');
        paymentForm.reset(); 
        switchPaymentForm('credit');
        syncPaymentDisplay();

      } else {
        alert('保存に失敗しました： ' + result.error);
      }
    } catch (error) {
      console.error('Payment add error:', error);
      alert('支払い方法の追加中にエラーが発生しました: ' + error.message);
    } finally {
        saveBtn.disabled = false;
    }
  });


  // ==========================================================
  // 6. 输入专业化と検証
  // ==========================================================
  const cardNameInputHandler = (e) => { e.target.value = e.target.value.toUpperCase(); };
  
  cardNumInput?.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\s/g, ''); 
    let formatted = value.match(/.{1,4}/g)?.join(' ') || '';
    e.target.value = formatted;
  });

  cardExpInput?.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, ''); 
    if (value.length > 2) {
      value = value.substring(0, 2) + '/' + value.substring(2);
    }
    e.target.value = value.substring(0, 5);
  });
  
  cardNameInput?.addEventListener('input', cardNameInputHandler);

  bankAccNumInput?.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/\D/g, ''); 
  });
});
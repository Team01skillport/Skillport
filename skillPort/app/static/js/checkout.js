document.addEventListener('DOMContentLoaded', () => {

  // ==========================================================
  // 1. 变量定义与 DOM 元素获取 (Variables and DOM Elements)
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
  const creditForm = document.getElementById('creditCardForm');
  const bankForm = document.getElementById('bankAccountForm');
  const paymentRadios = document.querySelectorAll('input[name="payment_type"]');

  const btnOpenModalCredit = document.getElementById('btnOpenModalCredit');
  const btnOpenModalBank = document.getElementById('btnOpenModalBank');
  
  // 新增：专业化输入所需字段
  const cardNumInput = document.getElementById('card_num');
  const cardNameInput = document.getElementById('card_name');
  const cardExpInput = document.getElementById('card_expiration');
  const bankAccNumInput = document.getElementById('bank_account_num');


  // ==========================================================
  // 2. 支付总览显示同步 (Payment Summary Display)
  // ==========================================================
  const syncPaymentDisplay = () => {
    if (!select || !sumPayment) return;
    const selectedOption = select.options[select.selectedIndex];

    if (selectedOption && selectedOption.value !== "") {
      // 仅显示支付方式的名称部分
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
  // 3. 购买动作 (Purchase Action)
  // ==========================================================
  buyButton?.addEventListener('click', async () => {

    buyButton.disabled = true;
    buyButton.textContent = '処理中...';

    // 额外的安全检查: 确保已选择支付方式
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
  // 4. 配送地址模态框逻辑 (Address Modal)
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
    const saveBtn = addressForm.querySelector('.btn-save');
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
        addressDisplay.innerHTML = `
          ${updatedData.last_name || ''} ${updatedData.first_name || ''} 
          （${updatedData.last_name_katakana || ''} ${updatedData.first_name_katakana || ''}）<br />
          〒${updatedData.zip_code}<br />
          ${updatedData.prefecture || ''} ${updatedData.address1 || ''}<br />
          ${updatedData.address2 || ''}
        `;
        const currentName = addressDisplay.querySelector('strong') ? '' : addressDisplay.innerHTML.split('<br')[0];
        
        addressDisplay.innerHTML = `
          ${currentName}
          ${currentName ? '<br />' : ''}
          〒${updatedData.zip_code}<br />
          ${updatedData.prefecture || ''} ${updatedData.address1 || ''}<br />
          ${updatedData.address2 || ''}
        `;
        const addAddressLink = document.getElementById('btnAddAddress');
        // '住所が登録されていません' の警告を削除
        if (addAddressLink) {
            const strongElement = addAddressLink.closest('strong');
            if (strongElement) strongElement.parentElement.innerHTML = addressDisplay.innerHTML; 
            else addAddressLink.closest('span')?.remove();
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
  // 5. 支付方法模态框逻辑 (Payment Modal)
  // ==========================================================
  const switchPaymentForm = (type) => {
    const radio = document.querySelector(`input[name="payment_type"][value="${type}"]`);
    if (radio) radio.checked = true;

    // 获取所有输入字段
    const allCreditFields = creditForm ? creditForm.querySelectorAll('input, select') : [];
    const allBankFields = bankForm ? bankForm.querySelectorAll('input, select') : [];
    
    // 激活信用卡表单
    if (type === 'credit') {
      creditForm?.classList.add('active');
      bankForm?.classList.remove('active');
      
      // 启用信用卡的 required，禁用银行的 required
      allCreditFields.forEach(el => el.setAttribute('required', ''));
      allBankFields.forEach(el => el.removeAttribute('required')); // 【关键】移除隐藏字段的 required
      
    } else { // 激活银行表单
      creditForm?.classList.remove('active');
      bankForm?.classList.add('active');
      
      // 启用银行的 required，禁用信用卡的 required
      allCreditFields.forEach(el => el.removeAttribute('required')); // 【关键】移除隐藏字段的 required
      allBankFields.forEach(el => el.setAttribute('required', ''));
    }
  };

  paymentRadios.forEach(radio => {
    radio.addEventListener('change', () => switchPaymentForm(radio.value));
  });

  const openPaymentModal = (e) => {
    e.preventDefault();
    paymentModal?.classList.add('active');
  };

  btnEditPayment?.addEventListener('click', openPaymentModal);
  btnCancelPayment?.addEventListener('click', (e) => {
    e.preventDefault();
    paymentModal?.classList.remove('active');
  });

  btnOpenModalCredit?.addEventListener('click', (e) => {
    switchPaymentForm('credit');
    openPaymentModal(e);
  });
  btnOpenModalBank?.addEventListener('click', (e) => {
    switchPaymentForm('bank');
    openPaymentModal(e);
  });

  // --- 支付方法提交逻辑：包含数据过滤和清理 ---
  paymentForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // 确保在提交时设置了 active 表单的 required 属性
    const currentType = paymentForm.querySelector('input[name="payment_type"]:checked')?.value;
    if (currentType) {
        switchPaymentForm(currentType); 
    }
    
    // 浏览器会执行 HTML5 验证
    if (!paymentForm.checkValidity()) {
        console.warn("Form validation failed. Check if all required fields are filled.");
        return;
    }
    
    const saveBtn = paymentForm.querySelector('.btn-save');
    saveBtn.disabled = true;

    const formData = new FormData(paymentForm);
    let data = Object.fromEntries(formData.entries()); 

    const activeType = data.payment_type;
    let relevantData = { 'payment_type': activeType };

    // 确定当前活跃的表单元素集合
    let activeFormElements = [];
    if (activeType === 'credit' && creditForm) {
      activeFormElements = creditForm.querySelectorAll('input, select');
    } else if (activeType === 'bank' && bankForm) {
      activeFormElements = bankForm.querySelectorAll('input, select');
    }

    // [关键修复] 只保留活跃表单中的数据，并清理空格
    activeFormElements.forEach(el => {
      let value = data[el.name];
      if (typeof value === 'string') {
          // 清理信用卡号和银行账号中的所有空格
          if (el.name === 'card_num' || el.name === 'bank_account_num') {
              value = value.replace(/\s/g, '');
          }
          // 名义人必须转换为大写
          if (el.name === 'card_name') {
              value = value.toUpperCase();
          }
      }
      // 仅发送有效字段
      if (value !== undefined) { 
          relevantData[el.name] = value;
      }
    });

    data = relevantData; // 使用过滤后的数据

    try {
      const response = await fetch('/market/checkout/add_payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        // 捕获非 200 状态码的详细错误
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

          // 处理 "没有支付方式" 的初始状态切换
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
        paymentForm.reset(); // 【关键】重置表单内容
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
  // 6. 输入专业化と検証 (Input Professionalism and Validation)
  // ==========================================================
  
  // 6.1 Event Handlers
  const cardNameInputHandler = (e) => { e.target.value = e.target.value.toUpperCase(); };
  
  // 6.2 Initial Bindings (for fields that need immediate formatting)
  
  // a) 实时格式化卡号 (每 4 位添加空格)
  cardNumInput?.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\s/g, ''); 
    let formatted = value.match(/.{1,4}/g)?.join(' ') || '';
    e.target.value = formatted;
  });

  // b) 实时格式化有效期限 (自动添加 /)
  cardExpInput?.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, ''); 
    if (value.length > 2) {
      value = value.substring(0, 2) + '/' + value.substring(2);
    }
    // 限制长度为 MM/YY (5个字符)
    e.target.value = value.substring(0, 5);
  });
  
  // c) 实时将信用卡名义人转换为大写
  cardNameInput?.addEventListener('input', cardNameInputHandler);

  // d) 银行账户只允许数字输入 (安全优化)
  bankAccNumInput?.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/\D/g, ''); 
  });


  // ==========================================================
  // 7. 其他全局事件 (Misc Global Events)
  // ==========================================================
  document.addEventListener('click', (e) => {
    const dd = document.getElementById('nav-category');
    if (!dd) return;
    if (!e.target.closest('#nav-category, [data-dropdown-toggle]')) {
      dd.classList.remove('open');
    }
  });

});
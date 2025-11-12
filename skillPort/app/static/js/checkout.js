document.addEventListener('click', (e) => {
  const dd = document.getElementById('nav-category');
  if (!dd) return;
  if (dd.contains(e.target)) {
    dd.classList.toggle('open');
  } else {
    dd.classList.remove('open');
  }
});

document.addEventListener('DOMContentLoaded', () => {
  
  const select = document.getElementById('paymentSelect');
  const sumPayment = document.getElementById('sumPayment');

  const syncPaymentDisplay = () => {
    if (!select || !sumPayment) return;
    const selectedOption = select.options[select.selectedIndex];
    if (selectedOption && selectedOption.value !== "") {
      sumPayment.textContent = selectedOption.text.split(' ')[0];
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

  const buyButton = document.getElementById('btnPurchase');
  buyButton?.addEventListener('click', async () => {
    
    buyButton.disabled = true;
    buyButton.textContent = '処理中...';
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

  const addressModal = document.getElementById('addressModal');
  const btnEditAddress = document.getElementById('btnEditAddress');
  const btnAddAddress = document.getElementById('btnAddAddress');
  const btnCancelAddress = document.getElementById('btnCancelAddress');
  const addressForm = document.getElementById('addressForm');
  const addressDisplay = document.getElementById('shippingAddressDisplay');

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
        const newAddr = result.new_address;
        addressDisplay.innerHTML = `
          〒${newAddr.zip_code}<br />
          ${newAddr.prefecture} ${newAddr.address1}<br />
          ${newAddr.address2}
        `;
        if (addressDisplay.querySelector('strong')) {
            addressDisplay.querySelector('strong').remove();
            addressDisplay.querySelector('span.link-edit').remove();
        }
        closeAddressModal(e);
      } else {
        alert('住所の保存に失敗しました： ' + result.error);
      }
    } catch (error) {
      console.error('Address update error:', error);
      alert('住所の更新中にエラーが発生しました。');
    }
  });

  // --- 支払い方法モーダルの処理 ---
  const paymentModal = document.getElementById('paymentModal');
  const btnEditPayment = document.getElementById('btnEditPayment');
  const btnCancelPayment = document.getElementById('btnCancelPayment');
  const paymentForm = document.getElementById('paymentForm');
  const creditForm = document.getElementById('creditCardForm');
  const bankForm = document.getElementById('bankAccountForm');
  const paymentRadios = document.querySelectorAll('input[name="payment_type"]');
  
  // [修改] 抓取这两个新按钮
  const btnOpenModalCredit = document.getElementById('btnOpenModalCredit');
  const btnOpenModalBank = document.getElementById('btnOpenModalBank');

  const switchPaymentForm = (type) => {
    const radio = document.querySelector(`input[name="payment_type"][value="${type}"]`);
    if (radio) radio.checked = true;
    
    if (type === 'credit') {
      creditForm.classList.add('active');
      bankForm.classList.remove('active');
    } else {
      creditForm.classList.remove('active');
      bankForm.classList.add('active');
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

  // [修改] 为新按钮添加事件监听
  btnOpenModalCredit?.addEventListener('click', (e) => {
    switchPaymentForm('credit');
    openPaymentModal(e);
  });
  btnOpenModalBank?.addEventListener('click', (e) => {
    switchPaymentForm('bank');
    openPaymentModal(e);
  });

  paymentForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(paymentForm);
    const data = Object.fromEntries(formData.entries());
    try {
      const response = await fetch('/market/checkout/add_payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      
      if (result.success) {
        const newOption = document.createElement('option');
        newOption.value = result.new_payment.value;
        newOption.textContent = result.new_payment.text;
        newOption.selected = true;
        
        // 确保 select 存在
        if (select) {
          select.appendChild(newOption);
          
          const noPaymentOption = document.getElementById('noPaymentOption');
          if (noPaymentOption) {
            const parent = noPaymentOption.parentNode;
            
            // [修改] 替换掉 "没有支付方式" 的逻辑
            const selectWrap = parent.parentNode; // .select-wrap
            selectWrap.style.display = 'block'; // 显示下拉框
            
            // 删除 "添加" 按钮
            document.querySelector('.payment-add-buttons')?.remove();
            
            // 显示 "变更・追加" 按钮
            const blockHead = selectWrap.closest('.block').querySelector('.block-head');
            blockHead.appendChild(btnEditPayment); // 将按钮加回去
            
            noPaymentOption.remove();
          }
        }

        paymentModal.classList.remove('active');
        paymentForm.reset();
        syncPaymentDisplay(); 
        
      } else {
        alert('保存に失敗しました： ' + result.error);
      }
    } catch (error) {
      console.error('Payment add error:', error);
      alert('支払い方法の追加中にエラーが発生しました。');
    }
  });
});
document.addEventListener('DOMContentLoaded', () => {
    
    const sendButton = document.getElementById('sendMessageBtn');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const chatSection = document.querySelector('.transaction-chat'); // [已修改]
    
    // [已修改] 从 data-order-id 属性中安全地获取 ID
    const orderId = chatSection ? chatSection.dataset.orderId : null;
    
    if (!orderId) {
        console.error("注文IDが取得できませんでした。");
        if(sendButton) sendButton.disabled = true;
        return;
    }

    if (sendButton) {
        sendButton.addEventListener('click', () => {
            const messageText = messageInput.value.trim();
            if (messageText === "") {
                return; 
            }
            postMessage(orderId, messageText);
        });
    }

    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); 
                sendButton.click(); 
            }
        });
    }

    async function postMessage(orderId, messageText) {
        
        sendButton.disabled = true; 

        try {
            const response = await fetch('/market/transaction/post_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    order_id: orderId,
                    message_text: messageText
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                addMessageToChat(result.message.order_message_text, 'buyer');
                messageInput.value = ''; 
            } else {
                // [已修改] 显示后端返回的更具体的错误信息
                alert(result.error || 'メッセージの送信に失敗しました。');
            }

        } catch (error) {
            console.error('Fetch エラー:', error);
            alert('通信エラーが発生しました。'); // <-- 您看到的错误
        } finally {
            sendButton.disabled = false; 
        }
    }

    function addMessageToChat(text, role) {
        if (!chatMessages) return;
        
        const messageRow = document.createElement('div');
        messageRow.className = `message-row ${role}`; 
        
        const avatar = document.createElement('div');
        avatar.className = 'user-avatar';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const userName = document.createElement('p');
        userName.className = 'message-user-name';
        userName.textContent = (role === 'buyer') ? 'あなた' : '出品者';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = text;
        
        content.appendChild(userName);
        content.appendChild(bubble);
        messageRow.appendChild(avatar);
        messageRow.appendChild(content);
        
        chatMessages.appendChild(messageRow);
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    if(chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

});
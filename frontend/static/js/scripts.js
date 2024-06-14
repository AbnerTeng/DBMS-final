document.querySelectorAll('input[name="action"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
        if (this.value === 'remove_background') {
            document.getElementById('imageUpload').style.display = 'block';
            document.getElementById('urlInput').style.display = 'none';
            document.getElementById('eventSelect').style.display = 'none';
            document.getElementById('receiverUpload').style.display = 'none';
        } else if (this.value === 'generate_qrcode') {
            document.getElementById('imageUpload').style.display = 'none';
            document.getElementById('urlInput').style.display = 'block';
            document.getElementById('eventSelect').style.display = 'none';
            document.getElementById('receiverUpload').style.display = 'none';
        } else {
            document.getElementById('imageUpload').style.display = 'none';
            document.getElementById('urlInput').style.display = 'none';
            document.getElementById('eventSelect').style.display = 'block';
            document.getElementById('receiverUpload').style.display = 'block';
        }
    });
});

// 新增的 CRUD 操作代碼
document.addEventListener('DOMContentLoaded', () => {
    const mockData = [
        { id: '1', model: 'Roadster', quantity: 2, amount: 1000 },
        { id: '2', model: 'Mountain', quantity: 3, amount: 1500 }
    ];

    // 搜尋數據
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const query = document.getElementById('searchInput').value;
        const resultsDiv = document.getElementById('searchResults');
        resultsDiv.innerHTML = '';
        const results = mockData.filter(item => item.id.includes(query));
        results.forEach(item => {
            const resultItem = document.createElement('div');
            resultItem.textContent = `ID: ${item.id}, Model: ${item.model}, Quantity: ${item.quantity}, Amount: ${item.amount}`;
            resultsDiv.appendChild(resultItem);
        });
    });

    // 查找訂單ID
    document.getElementById('findOrderForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const orderId = document.getElementById('findOrderId').value;
        const order = mockData.find(item => item.id === orderId);

        if (order) {
            document.getElementById('orderDetails').style.display = 'block';
            document.getElementById('updateInputModel').value = order.model;
            document.getElementById('updateInputQuantity').value = order.quantity;
            document.getElementById('updateInputAmount').value = order.amount;
        } else {
            document.getElementById('orderDetails').style.display = 'none';
            console.error('Order not found');
        }
    });

    // 更新數據
    document.getElementById('updateForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const id = document.getElementById('findOrderId').value;
        const model = document.getElementById('updateInputModel').value;
        const quantity = document.getElementById('updateInputQuantity').value;
        const amount = document.getElementById('updateInputAmount').value;

        const orderIndex = mockData.findIndex(item => item.id === id);
        if (orderIndex > -1) {
            mockData[orderIndex] = { id, model, quantity, amount };
            console.log('Updated order:', mockData[orderIndex]);
        } else {
            console.error('Order not found');
        }
    });
});
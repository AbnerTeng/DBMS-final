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




//-----------------------------新增訂單-----------------------------
function addItems() {
    // 清除之前的輸入
    document.getElementById('itemInputs').innerHTML = '';

    // 請求用戶輸入需要添加的商品數量
    const numberOfItems = prompt('How many products do you want to add?');
    const container = document.getElementById('itemInputs');

    for (let i = 0; i < numberOfItems; i++) {
        const itemDiv = document.createElement('div');
        itemDiv.innerHTML = `
            <label for="product_id">Product ID:</label>
            <input type="text" name="product_id[]" required><br>
            <label for="quantity">Quantity:</label>
            <input type="number" name="quantity[]" required min="1"><br>
        `;
        container.appendChild(itemDiv);
    }
}

document.getElementById('orderForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const customerId = document.getElementById('customer_id').value;
    const discount = document.getElementById('discount').value;
    const productIds = document.querySelectorAll('input[name="product_id[]"]');
    const quantities = document.querySelectorAll('input[name="quantity[]"]');

    // 檢查每個數量是否為正數
    for (let quantity of quantities) {
        if (quantity.value <= 0) {
            alert('Quantity must be a positive number.');
            return;
        }
    }

    const items = Array.from(productIds).map((input, index) => ({
        product_id: input.value,
        quantity: quantities[index].value
    }));

    const orderDetails = {
        customer_id: customerId,
        discount: discount,
        items: items
    };

    // 驗證客戶 ID 是否存在
    fetch(`http://example.com/api/customers/${customerId}`)
        .then(response => {
            if (!response.ok) throw new Error('Customer not found');
            return response.json();
        })
        .then(data => {
            // 如果客戶存在，提交訂單
            submitOrder(orderDetails);
        })
        .catch(error => {
            // 如果客戶不存在，顯示新客戶信息表單
            document.getElementById('newCustomerForm').style.display = 'block';
        });
});

function submitOrder(orderDetails) {
    fetch('http://example.com/api/orders', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(orderDetails)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Order submitted successfully!');
            document.getElementById('orderForm').reset();
            document.getElementById('itemInputs').innerHTML = '';
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function submitNewCustomer() {
    const customerDetails = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        street: document.getElementById('street').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        zip_code: document.getElementById('zip_code').value
    };

    fetch('http://example.com/api/customers', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(customerDetails)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Customer created successfully!');
            // 隱藏新客戶信息表單
            document.getElementById('newCustomerForm').style.display = 'none';
            // 繼續提交訂單
            const customerId = data.customer_id;
            const discount = document.getElementById('discount').value;
            const productIds = document.querySelectorAll('input[name="product_id[]"]');
            const quantities = document.querySelectorAll('input[name="quantity[]"]');

            const items = Array.from(productIds).map((input, index) => ({
                product_id: input.value,
                quantity: quantities[index].value
            }));

            const orderDetails = {
                customer_id: customerId,
                discount: discount,
                items: items
            };

            submitOrder(orderDetails);
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

//-----------------------------刪除訂單-----------------------------
document.getElementById('deleteOrderForm').addEventListener('submit', function(event) {
    event.preventDefault(); // 防止表單的默認提交行為
    const orderId = document.getElementById('order_id').value;

    // 發送刪除請求的API
    fetch(`http://example.com/api/orders/${orderId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Order not found');
        return response.json();
    })
    .then(data => {
        alert('Order deleted successfully!');
        document.getElementById('deleteOrderForm').reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    });
});

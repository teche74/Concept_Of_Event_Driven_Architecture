function placeOrder(productName, event) {
    const button = event.target;

    const card = button.closest('.product-card');
    const quantityInput = card.querySelector('input[type="number"]');
    const priceSpan = card.querySelector('span');

    if (!quantityInput || !priceSpan) {
        alert("Missing input or price field.");
        return;
    }

    const quantity = parseInt(quantityInput.value);
    const price = parseInt(priceSpan.textContent);

    if (isNaN(quantity) || isNaN(price)) {
        alert("Invalid quantity or price.");
        return;
    }

    const payload = {
        product: productName,
        item_count: quantity,
        total_cost: quantity * price
    };

    fetch('/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(err => {
        alert("Failed to place order.");
        console.error(err);
    });
}

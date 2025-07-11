function placeOrder(productName) {
    let quantity = 1, price = 0; 
    
    if(productName === 'Protein Bar') {
        quantity = parseInt(document.getElementById('bar_quantity').value);
        price = parseInt(document.getElementById('bar_price').value);
    }
    else if(productName === 'Smoothie') {
        quantity = parseInt(document.getElementById('smooth_quantity').value);
        price = parseInt(document.getElementById('smooth_price').value);
    }
    else if(productName === 'Energy Balls') {
        quantity = parseInt(document.getElementById('balls_quantity').value);
        price = parseInt(document.getElementById('balls_price').value);
    }
    
    fetch('/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product: productName , item_count : quantity , total_cost : quantity * price })
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

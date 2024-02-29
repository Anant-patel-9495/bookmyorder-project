// Function to add an item to the cart
function addToCart(itemName, itemPrice, quantity) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];

    const existingItem = cart.find(item => item.name === itemName);

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({ name: itemName, price: itemPrice, quantity: quantity });
    }

    localStorage.setItem('cart', JSON.stringify(cart));

    // Calculate the total price based on quantity
    const totalPrice = (itemPrice * quantity).toFixed(2);

    // Update the total price displayed in the UI
    const totalPrices = document.querySelectorAll('.total-price');
    const itemIndex = cart.findIndex(item => item.name === itemName);
    totalPrices[itemIndex].textContent = `$${totalPrice}`;

    // Show an alert message
    alert(`Item "${itemName}" has been added to your cart.`);

    // You can customize the alert message style and appearance using CSS or a library like SweetAlert.
}

// Attach click event handlers to quantity buttons and "Add to Cart" buttons
document.addEventListener('DOMContentLoaded', function () {
    const quantityButtons = document.querySelectorAll('.quantity-button');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const input = button.parentElement.querySelector('.quantity-input');
            const currentValue = parseInt(input.value);

            if (button.classList.contains('minus')) {
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                }
            } else if (button.classList.contains('plus')) {
                input.value = currentValue + 1;
            }
        });
    });

    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const itemName = button.getAttribute('data-item-name');
            const itemPrice = parseFloat(button.getAttribute('data-item-price'));
            const quantity = parseInt(button.parentElement.querySelector('.quantity-input').value);
            addToCart(itemName, itemPrice, quantity);
        });
    });
});

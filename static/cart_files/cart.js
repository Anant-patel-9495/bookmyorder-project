// Function to retrieve the cart data from local storage
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

// Function to calculate the total price of an item
function calculateItemTotal(item) {
    return item.price * item.quantity;
}

// Function to calculate the total amount of the entire cart
function calculateTotalAmount(cart) {
    return cart.reduce((total, item) => total + calculateItemTotal(item), 0);
}

// Function to display cart items and calculate the total price
function displayCartItems() {
    const cartContent = document.getElementById('cart-content');
    const totalAmount = document.getElementById('total-amount');
    const cart = getCart();

    if (cart.length === 0) {
        cartContent.innerHTML = '<p>Your cart is empty.</p>';
        totalAmount.textContent = '0.00';
    } else {
        cartContent.innerHTML = '';
        let grandTotal = 0;

        cart.forEach((item, index) => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');

            // Check if the item has custom spice level and diet-conscious
            const spiceLevel = item.customSpiceLevel || item.spiceLevel;
            const dietConscious = item.customDietConscious !== undefined ? item.customDietConscious : item.dietConscious;

            cartItem.innerHTML = `
                <p class="cart-item-name">${item.name} x${item.quantity}</p>
                <p class="cart-item-spice">Spice Level: ${spiceLevel}</p>
                <p class="cart-item-diet">Diet Conscious: ${dietConscious ? 'Yes' : 'No'}</p>
                <p class="cart-item-quantity">Quantity: ${item.quantity}</p>
                <div class="quantity">
                    <button class="quantity-button minus" data-index="${index}">-</button>
                    <input class="quantity-input" type="number" value="${item.quantity}" min="1">
                    <button class="quantity-button plus" data-index="${index}">+</button>
                </div>
                <p class="total-price">₹${calculateItemTotal(item).toFixed(2)}</p>
                <button class="cart-item-remove" data-index="${index}">Remove</button>
            `;

            cartContent.appendChild(cartItem);

            grandTotal += calculateItemTotal(item);
        });

        totalAmount.textContent = grandTotal.toFixed(2);

        // Attach click event handlers to quantity buttons and "Remove" buttons
        const quantityButtons = document.querySelectorAll('.quantity-button');
        quantityButtons.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                const index = parseInt(button.getAttribute('data-index'));
                const input = button.parentElement.querySelector('.quantity-input');
                const currentValue = parseInt(input.value);

                if (button.classList.contains('minus')) {
                    if (currentValue > 1) {
                        input.value = currentValue - 1;
                        updateItemQuantity(index, currentValue - 1);
                    }
                } else if (button.classList.contains('plus')) {
                    input.value = currentValue + 1;
                    updateItemQuantity(index, currentValue + 1);
                }
            });
        });

        const removeButtons = document.querySelectorAll('.cart-item-remove');
        removeButtons.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                const index = parseInt(button.getAttribute('data-index'));
                removeFromCart(index);
            });
        });

        // Add event listener for the "Order Now" button
        const orderButton = document.getElementById('order-button');
        orderButton.addEventListener('click', placeOrder);
    }
}

// Function to update an item's quantity
function updateItemQuantity(index, quantity) {
    const cart = getCart();
    cart[index].quantity = quantity;
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCartItems();
}

// Function to remove an item from the cart
function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCartItems();
}

function placeOrder(event) {
    event.preventDefault(); // Prevent the default form submission

    // Fetch CSRF token from the hidden input field
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const cart = getCart();

    fetch('/user_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(cart),
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred while placing the order.');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Order placed successfully. Cook will start preparing your order.');
                // Clear the cart after placing the order
                localStorage.removeItem('cart');
                displayCartItems();
            }else {
                alert('Failed to place the order. Please try again later.');
            }
        })
        .catch(error => {
            console.error('Error placing the order:', error);
            alert('An error occurred while placing the order. Please try again later.');
        });
}

document.addEventListener('DOMContentLoaded', function () {
    displayCartItems();

    const orderForm = document.getElementById('order-form');
    orderForm.addEventListener('submit', placeOrder); // Attach to the form's submit event
});
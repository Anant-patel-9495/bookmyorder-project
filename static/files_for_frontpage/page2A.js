document.addEventListener('DOMContentLoaded', function () {
    const addToCartButton = document.getElementById('add-to-cart');

    addToCartButton.addEventListener('click', function () {
        const spiceLevelRadios = document.querySelectorAll('input[name="spice-level"]');
        let spiceLevel = '';

        spiceLevelRadios.forEach(radio => {
            if (radio.checked) {
                spiceLevel = radio.value;
            }
        });

        const dietConsciousCheckbox = document.getElementById('diet-conscious');
        const isDietConscious = dietConsciousCheckbox.checked;

        const quantityInput = document.getElementById('quantity');
        const quantity = parseInt(quantityInput.value);

        // Fetch item name and price from HTML attributes
        const itemName = addToCartButton.getAttribute('data-item-name');
        const itemPrice = parseFloat(addToCartButton.getAttribute('data-item-price'));

        const itemData = {
            name: itemName,
            spiceLevel: spiceLevel,
            dietConscious: isDietConscious,
            price: itemPrice,
            quantity: quantity,
        };

        // Add the item to the cart in local storage
        addToCart(itemData);
        
        // Show an alert message
        alert('Item added to the cart successfully!');
    });
    
    function addToCart(item) {
        const cart = getCart();
        cart.push(item);
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function getCart() {
        return JSON.parse(localStorage.getItem('cart')) || [];
    }
});
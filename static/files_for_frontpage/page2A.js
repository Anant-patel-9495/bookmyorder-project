document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('#add-to-cart');
  
    addToCartButtons.forEach(button => {
      button.addEventListener('click', function () {
        const menuItemDetail = button.closest('.menu-item-detail');
        const itemTitle = menuItemDetail.querySelector('.item-title').textContent;
        const itemPrice = parseFloat(button.getAttribute('data-item-price'));
  
        const spiceLevelRadios = menuItemDetail.querySelectorAll('input[name="spice-level"]');
        let spiceLevel = '';
        spiceLevelRadios.forEach(radio => {
          if (radio.checked) {
            spiceLevel = radio.value;
          }
        });
  
        const dietConsciousCheckbox = menuItemDetail.querySelector('#diet-conscious');
        const isDietConscious = dietConsciousCheckbox ? dietConsciousCheckbox.checked : false;
  
        const quantityInput = menuItemDetail.querySelector('#quantity');
        const quantity = parseInt(quantityInput ? quantityInput.value : 1);
  
        const itemData = {
          name: itemTitle,
          spiceLevel: spiceLevel,
          dietConscious: isDietConscious,
          price: itemPrice,
          quantity: quantity,
        };
  
        addToCart(itemData);
        alert(`Item "${itemTitle}" has been added to your cart.`);
      });
    });
  
    function addToCart(item) {
      const cart = getCart();
      const existingItem = cart.find(cartItem => cartItem.name === item.name);
      if (existingItem) {
        existingItem.quantity += item.quantity;
      } else {
        cart.push(item);
      }
      localStorage.setItem('cart', JSON.stringify(cart));
    }
  
    function getCart() {
      return JSON.parse(localStorage.getItem('cart')) || [];
    }
  });
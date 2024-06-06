
document.getElementById('user-details-form').addEventListener('submit', function (event) {
    event.preventDefault();

    // Get user details from the form
    const personName = document.getElementById('person-name').value;
    const email = document.getElementById('email').value;
    // Get more fields as needed

    // Redirect to cart page with user details as query parameters
    window.location.href = `{% url 'user_cart' %}?person_name=${encodeURIComponent(personName)}&email=${encodeURIComponent(email)}`;
});
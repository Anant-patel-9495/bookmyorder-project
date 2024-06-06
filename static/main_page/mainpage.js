// Function to handle form submission
function handleFormSubmission(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Generate a new customer ID
    const customerId = generateCustomerId();

    // Construct the URL for the cart page with the customer ID as a parameter
    const cartUrl = `http://127.0.0.1:8000/user_cart/?customer_id=${customerId}`;

    // Redirect the user to the cart page with the customer ID parameter
    window.location.href = cartUrl;
}

// Function to generate a new customer ID
function generateCustomerId() {
    // Generate a random UUID (you can use any method to generate a unique ID)
    // Here's a simple method to generate a UUID-like string
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Attach the handleFormSubmission function to the form's submit event
document.getElementById('customer-registration-form').addEventListener('submit', handleFormSubmission)
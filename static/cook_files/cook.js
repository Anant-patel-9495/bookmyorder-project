let startTime;
let timerInterval;

document.getElementById('personstart').addEventListener('click', function () {
    startTime = new Date();
    document.getElementById('timer').innerText = '0 seconds';
    timerInterval = setInterval(updateTimer, 1000);
});

document.getElementById('personsubmit').addEventListener('click', function () {
    clearInterval(timerInterval);
    alert('Your order is completed');
    window.location.href = "http://127.0.0.1:8000/user_cart/";
});

function updateTimer() {
    let currentTime = new Date();
    let elapsedTime = Math.floor((currentTime - startTime) / 1000);
    document.getElementById('timer').innerText = `${elapsedTime} seconds`;
}
document.addEventListener('DOMContentLoaded', function() {
    const quantityElems = document.querySelectorAll('#quantity');
    const incrementBtns = document.querySelectorAll('#increment');
    const decrementBtns = document.querySelectorAll('#decrement');

    incrementBtns.forEach((btn, index) => {
        btn.addEventListener('click', function () {
            let increment = Number(quantityElems[index].textContent);
            increment++;
            quantityElems[index].textContent = increment;
            updateQuantity(index, 'increment'); // Call the updateQuantity function here
        });
    });

    decrementBtns.forEach((btn, index) => {
        btn.addEventListener('click', function () {
            let decrement = Number(quantityElems[index].textContent);
            decrement = decrement <= 1 ? 1 : decrement - 1;
            quantityElems[index].textContent = decrement;
            updateQuantity(index, 'decrement'); // Call the updateQuantity function here
        });
    });

    function updateQuantity(index, action) {
    const Sellerdetail_ID = document.getElementById(`Sellerdetail_ID${index}`).value;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/update_quantity', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            // Handle response if needed
            console.log(xhr.responseText);
        }
    };
    const data = JSON.stringify({Sellerdetail_ID: Sellerdetail_ID, action: action});
    xhr.send(data);
}
});

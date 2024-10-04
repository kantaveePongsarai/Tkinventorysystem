document.addEventListener('DOMContentLoaded', () => {
    let listProductHTML = document.querySelector('.listProduct');
    let listCartHTML = document.querySelector('.listCart');
    let iconCart = document.querySelector('.icon-cart');
    let checkoutHTML = document.querySelector('.checkOut');
    let iconCartSpan = document.querySelector('.icon-cart span');
    let body = document.querySelector('body');
    let closeCart = document.querySelector('.close');
    let products = [];
    let cart = [];
    let maxQuantity = {};
    console.log(checkoutHTML);
    
    iconCart.addEventListener('click', () => {
        body.classList.toggle('showCart');
    });

    closeCart.addEventListener('click', () => {
        body.classList.toggle('showCart');
    });

    const addDataToHTML = () => {
        listProductHTML.innerHTML = '';

        if (products.length > 0) {
            products.forEach(product => {
                let newProduct = document.createElement('div');
                newProduct.dataset.id = product.Materials_ID;
                newProduct.dataset.quantity = product.Quantity;
                newProduct.classList.add('item');
                newProduct.innerHTML = `
                <img src="${product.materialsimg}" alt="${product.Materials_name}">
                <h2>${product.Materials_name}</h2>
                <h2>${product.Quantity} ตัว</h2>
                <button class="addCart">เพิ่มลงในตะกร้า</button><br>
                <a href="/editmaterial/${product.Materials_ID}">
                    <button class="primary">เเก้ไขข้อมูล</button>
                </a><br>
                <a href="/deletematerial/${product.Materials_ID}" onclick="return confirm('Are you sure you want to delete this item?');">
                    <button class="primary ghost">ลบข้อมูล</button>
                </a>
            `;
                maxQuantity[product.Materials_ID] = product.Quantity;
                listProductHTML.appendChild(newProduct);
            });
        }
    };

    listProductHTML.addEventListener('click', (event) => {
        let positionClick = event.target;
        if (positionClick.classList.contains('addCart')) {
            let id_product = positionClick.parentElement.dataset.id;
            addToCart(id_product);
        }
    });

    const addToCart = (materials_id) => {
        let positionThisProductInCart = cart.findIndex((value) => value.product_id == materials_id);
        if (cart.length <= 0) {
            cart = [{
                product_id: materials_id,
                quantity: 1
            }];
        } else if (positionThisProductInCart < 0) {
            cart.push({
                product_id: materials_id,
                quantity: 1
            });
        } else {
            if(cart[positionThisProductInCart].quantity < maxQuantity[materials_id]) {
                cart[positionThisProductInCart].quantity = cart[positionThisProductInCart].quantity + 1;
            } else {
                alert("bad");
            }
        }
        addCartToHTML();
        addCartToMemory();
    };

    const addCartToMemory = () => {
        localStorage.setItem('cart', JSON.stringify(cart));
    };

    const addCartToHTML = () => {
        listCartHTML.innerHTML = '';
        let totalQuantity = 0;
        if (cart.length > 0) {
            cart.forEach(item => {
                totalQuantity += item.quantity;
                let newItem = document.createElement('div');
                newItem.classList.add('item');
                newItem.dataset.id = item.product_id;

                let positionProduct = products.findIndex((value) => value.Materials_ID == item.product_id);
                let info = products[positionProduct];

                newItem.innerHTML = `
                    <div class="image">
                        <img src="${info.materialsimg}" alt="${info.Materials_name}">
                    </div>
                    <div class="name">${info.Materials_name}</div>
                    <div class="quantity">
                        <span class="plus">></span>
                        <span>${item.quantity}</span>
                        <span class="minus"><</span>
                    </div>`;
                listCartHTML.appendChild(newItem);
            });
        }
        iconCartSpan.innerText = totalQuantity;
    };

    listCartHTML.addEventListener('click', (event) => {
        let positionClick = event.target;
        if (positionClick.classList.contains('minus') || positionClick.classList.contains('plus')) {
            let materials_id = positionClick.parentElement.parentElement.dataset.id;
            let type = positionClick.classList.contains('plus') ? 'plus' : 'minus';
            changeQuantityCart(materials_id, type);
        }
    });

    const changeQuantityCart = (materials_id, type) => {
        let positionItemInCart = cart.findIndex((value) => value.product_id == materials_id);
        if (positionItemInCart >= 0) {
            switch (type) {
                case 'plus':
                    if(cart[positionItemInCart].quantity < maxQuantity[materials_id]) {
                        cart[positionItemInCart].quantity += 1;
                    } else {
                        alert("bad");
                    }
                    break;
                default:
                    if (cart[positionItemInCart].quantity > 1) {
                        cart[positionItemInCart].quantity -= 1;
                    } else {
                        cart.splice(positionItemInCart, 1);
                    }
                    break;
            }
        }
        addCartToHTML();
        addCartToMemory();
    };

    const initApp = () => {
        fetch(`/api/materials1`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            products = data;
            addDataToHTML();

            if (localStorage.getItem('cart')) {
                cart = JSON.parse(localStorage.getItem('cart'));
                addCartToHTML();
            }
        })
        .catch(error => console.error('Error fetching materials:', error));
    };
    checkoutHTML.addEventListener('click', (event) => {
        alert("Checkout initiated");
    
        fetch("/api/checkout", {  // Use the correct API endpoint
            method: "POST",
            body: JSON.stringify(cart),  // Send cart data
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert("Checkout successful: " + data.message);
            // Clear cart after successful checkout
            cart = [];
            addCartToHTML();
            addCartToMemory();
            // Redirect to detail page using the returned Req_Materials_ID
            if (data.req_materials_id) {
                window.location.href = `/detailrequisition/${data.req_materials_id}`;
            }
        })
        .catch(error => {
            console.error('Error during checkout:', error);
            alert("Error during checkout");
        });
    });

    initApp();
});


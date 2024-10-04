document.addEventListener("DOMContentLoaded", function() {
    // เลือกปุ่ม "Add to Cart" ทั้งหมด
    var addToCartButtons = document.querySelectorAll("button");

    // เพิ่มการฟังก์ชันสำหรับการคลิกที่ปุ่ม "Add to Cart" แต่ละปุ่ม
    addToCartButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            // หาข้อมูลที่เกี่ยวข้องกับสินค้าที่คลิกปุ่ม "Add to Cart"
            var card = button.closest(".card");
            var productName = card.querySelector("h1").textContent;
            var productPrice = card.querySelector(".price").textContent;
            
            // สร้าง HTML สำหรับสินค้าที่เพิ่มเข้าตะกร้า
            var cartItemHTML = `
                <div class="cart-item">
                    <span>${productName}</span>
                    <span>${productPrice}</span>
                </div>
            `;
            
            // เพิ่ม HTML ของสินค้าลงใน div ที่มี id เป็น "cartItem"
            var cartItemContainer = document.getElementById("cartItem");
            cartItemContainer.innerHTML = cartItemHTML;
            
            // อัพเดทยอดรวม
            updateTotal();
        });
    });

    // ฟังก์ชันสำหรับอัพเดทยอดรวม
    function updateTotal() {
        var totalPrice = 0;
        var cartItems = document.querySelectorAll(".cart-item");
        
        // หายอดรวมโดยวนลูปทุกรายการในตะกร้า
        cartItems.forEach(function(item) {
            var priceString = item.querySelector("span:nth-child(2)").textContent;
            var price = parseFloat(priceString.replace("$", ""));
            totalPrice += price;
        });
        
        // แสดงยอดรวมที่อัพเดทแล้ว
        var totalElement = document.getElementById("total");
        totalElement.textContent = "$ " + totalPrice.toFixed(2);
    }
});
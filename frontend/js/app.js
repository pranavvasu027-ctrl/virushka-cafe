// ==========================
// CART STORAGE
// ==========================

let cart = JSON.parse(localStorage.getItem("cart")) || [];


// ==========================
// ADD TO CART
// ==========================

function addToCart(name, price) {

    let existingItem = cart.find(item => item.name === name);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            name: name,
            price: price,
            quantity: 1
        });
    }

    localStorage.setItem("cart", JSON.stringify(cart));

    alert(name + " added to cart!");
}


// ==========================
// DISPLAY CART ITEMS
// ==========================

function displayCart() {

    const cartItems = document.getElementById("cart-items");

    const totalPrice = document.getElementById("total-price");

    if (!cartItems) return;

    cartItems.innerHTML = "";

    let total = 0;

    if (cart.length === 0) {

        cartItems.innerHTML = `
            <div style="text-align:center; padding: 60px 20px; color: #6b7280;">
                <p style="font-size:18px;">Your cart is empty.</p>
                <a href="menu.html" style="color:#ff5722; font-weight:600;">Browse Menu →</a>
            </div>
        `;

        totalPrice.innerText = 0;

        return;
    }

    cart.forEach((item, index) => {

        total += item.price * item.quantity;

        cartItems.innerHTML += `
            <div class="cart-item">

                <div>
                    <h3>${item.name}</h3>

                    <p>
                        ₹${item.price} × ${item.quantity}
                        =
                        ₹${item.price * item.quantity}
                    </p>
                </div>

                <div>
                    <button onclick="increaseQuantity(${index})">+</button>

                    <button onclick="decreaseQuantity(${index})">−</button>

                    <button onclick="removeItem(${index})">
                        Remove
                    </button>
                </div>

            </div>
        `;
    });

    totalPrice.innerText = total;
}


// ==========================
// INCREASE QUANTITY
// ==========================

function increaseQuantity(index) {

    cart[index].quantity++;

    updateCart();
}


// ==========================
// DECREASE QUANTITY
// ==========================

function decreaseQuantity(index) {

    if (cart[index].quantity > 1) {

        cart[index].quantity--;

    } else {

        cart.splice(index, 1);
    }

    updateCart();
}


// ==========================
// REMOVE ITEM
// ==========================

function removeItem(index) {

    cart.splice(index, 1);

    updateCart();
}


// ==========================
// UPDATE CART
// ==========================

function updateCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

    displayCart();
}


// ==========================
// LOAD CART
// ==========================

displayCart();


// ==========================
// PAYMENT TOTAL
// ==========================

function loadPaymentTotal() {

    const paymentTotal =
        document.getElementById(
            "payment-total"
        );

    if (!paymentTotal) return;

    let total = 0;

    cart.forEach(item => {

        total += item.price * item.quantity;
    });

    paymentTotal.innerText = total;
}

loadPaymentTotal();


// ==========================
// CONFIRM PAYMENT
// ==========================

async function confirmPayment() {

    const transactionId =
        document.getElementById(
            "transaction-id"
        ).value.trim();

    if (transactionId === "") {

        alert(
            "Please enter your Transaction ID"
        );

        return;
    }

    if (cart.length === 0) {

        alert(
            "Your cart is empty. Please add items first."
        );

        return;
    }

    let total = 0;

    cart.forEach(item => {

        total += item.price * item.quantity;
    });

    const orderData = {

        items: cart,

        totalAmount: total,

        transactionId: transactionId,

        paymentStatus: "Pending Verification"
    };

    try {

        const response = await fetch(
            `${API_URL}/place-order`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(orderData)
            }
        );

        const result = await response.json();

        if (!result.success) {

            alert(
                "Order failed: " + result.message
            );

            return;
        }

        localStorage.setItem(
            "latestOrderId",
            result.orderId
        );

        alert(
            "Order placed successfully!"
        );

        localStorage.removeItem("cart");

        cart = [];

        setTimeout(() => {

            window.location.href =
                "order-status.html";

        }, 1000);

    } catch (error) {

        console.error(error);

        alert(
            "Cannot connect to backend server."
        );
    }
}
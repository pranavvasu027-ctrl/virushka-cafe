// ==========================
// CART STORAGE
// ==========================

let cart = JSON.parse(localStorage.getItem("cart")) || [];

// ==========================
// ADD TO CART
// ==========================

function addToCart(name, price){

    // CHECK IF ITEM ALREADY EXISTS

    let existingItem = cart.find(item => item.name === name);

    if(existingItem){

        existingItem.quantity += 1;

    }else{

        cart.push({
            name: name,
            price: price,
            quantity: 1
        });

    }

    // SAVE TO LOCAL STORAGE

    localStorage.setItem("cart", JSON.stringify(cart));

    alert(name + " added to cart");
}

// ==========================
// DISPLAY CART ITEMS
// ==========================

function displayCart(){

    const cartItems = document.getElementById("cart-items");

    const totalPrice = document.getElementById("total-price");

    // STOP IF CART PAGE NOT OPEN

    if(!cartItems) return;

    cartItems.innerHTML = "";

    let total = 0;

    cart.forEach((item, index) => {

        total += item.price * item.quantity;

        cartItems.innerHTML += `
        
        <div class="cart-item">

            <div>

                <h3>${item.name}</h3>

                <p>₹${item.price} x ${item.quantity}</p>

            </div>

            <div>

                <button onclick="increaseQuantity(${index})">
                    +
                </button>

                <button onclick="decreaseQuantity(${index})">
                    -
                </button>

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

function increaseQuantity(index){

    cart[index].quantity++;

    updateCart();
}

// ==========================
// DECREASE QUANTITY
// ==========================

function decreaseQuantity(index){

    if(cart[index].quantity > 1){

        cart[index].quantity--;

    }else{

        cart.splice(index, 1);
    }

    updateCart();
}

// ==========================
// REMOVE ITEM
// ==========================

function removeItem(index){

    cart.splice(index, 1);

    updateCart();
}

// ==========================
// UPDATE CART
// ==========================

function updateCart(){

    localStorage.setItem("cart", JSON.stringify(cart));

    displayCart();
}

// ==========================
// LOAD CART
// ==========================

displayCart();

// ==========================
// PAYMENT TOTAL
// ==========================

function loadPaymentTotal(){

    const paymentTotal =
        document.getElementById("payment-total");

    if(!paymentTotal) return;

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

async function confirmPayment(){

    const transactionId =
        document.getElementById("transaction-id").value;

    const screenshot =
        document.getElementById("payment-screenshot").files[0];

    // VALIDATION

    if(transactionId === ""){

        alert("Please enter transaction ID");

        return;
    }

    if(!screenshot){

        alert("Please upload payment screenshot");

        return;
    }

    // TOTAL CALCULATION

    let total = 0;

    cart.forEach(item => {

        total += item.price * item.quantity;
    });

    // ORDER DATA

    const orderData = {

        items: cart,

        totalAmount: total,

        transactionId: transactionId,

        paymentStatus: "Pending Verification"
    };

    try{

        // SEND DATA TO FLASK BACKEND

        const response = await fetch(
            "http://127.0.0.1:5000/place-order",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(orderData)
            }
        );

        const result = await response.json();

        console.log(result);

        alert("Order placed successfully!");

        // CLEAR CART

        localStorage.removeItem("cart");

        // REDIRECT

        setTimeout(() => {

            window.location.href =
                "order-status.html";

        }, 1000);

    }catch(error){

        console.error(error);

        alert("Server connection failed");
    }
}
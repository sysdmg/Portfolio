// Initialize Stripe (will be set after fetching config)
let stripe;

// Sample products data (in a real app, this would come from a backend)
const products = [
    {
        id: 1,
        name: 'Classic T-Shirt',
        price: 29.99,
        image: 'https://via.placeholder.com/300'
    },
    {
        id: 2,
        name: 'Denim Jeans',
        price: 59.99,
        image: 'https://via.placeholder.com/300'
    },
    {
        id: 3,
        name: 'Casual Sneakers',
        price: 89.99,
        image: 'https://via.placeholder.com/300'
    }
];

// Shopping cart state
let cart = [];

// DOM Elements
const productsGrid = document.querySelector('.products-grid');
const cartSection = document.querySelector('.cart-section');
const cartItems = document.getElementById('cart-items');
const cartCount = document.getElementById('cart-count');
const cartSubtotal = document.getElementById('cart-subtotal');
const checkoutButton = document.getElementById('checkout-button');

// Initialize the store
async function initializeStore() {
    // Fetch Stripe publishable key from backend
    const response = await fetch('http://localhost:5000/config');
    const config = await response.json();
    stripe = Stripe(config.publishableKey);
    
    renderProducts();
    setupEventListeners();
}

// Render products to the grid
function renderProducts() {
    productsGrid.innerHTML = products.map(product => `
        <div class="product-card">
            <img src="${product.image}" alt="${product.name}" class="product-image">
            <div class="product-info">
                <h3 class="product-title">${product.name}</h3>
                <p class="product-price">$${product.price.toFixed(2)}</p>
                <button class="add-to-cart" data-id="${product.id}">Add to Cart</button>
            </div>
        </div>
    `).join('');
}

// Set up event listeners
function setupEventListeners() {
    // Add to cart buttons
    productsGrid.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-to-cart')) {
            const productId = parseInt(e.target.dataset.id);
            addToCart(productId);
        }
    });

    // Navigation
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = e.target.getAttribute('href').substring(1);
            toggleSection(section);
        });
    });

    // Checkout button
    checkoutButton.addEventListener('click', initiateCheckout);
}

// Add item to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const cartItem = cart.find(item => item.id === productId);

    if (cartItem) {
        cartItem.quantity++;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }

    updateCartUI();
}

// Update cart UI
function updateCartUI() {
    // Update cart count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;

    // Update cart items
    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <h3>${item.name}</h3>
                <p>$${item.price.toFixed(2)} × ${item.quantity}</p>
            </div>
            <div class="cart-item-total">
                $${(item.price * item.quantity).toFixed(2)}
            </div>
        </div>
    `).join('');

    // Update subtotal
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    cartSubtotal.textContent = `$${subtotal.toFixed(2)}`;
}

// Toggle sections (products/cart)
function toggleSection(section) {
    if (section === 'cart') {
        productsGrid.style.display = 'none';
        cartSection.classList.remove('hidden');
    } else {
        productsGrid.style.display = 'grid';
        cartSection.classList.add('hidden');
    }
}

// Initialize checkout process
async function initiateCheckout() {
    try {
        // In a real application, this would make a request to your backend
        // to create a Stripe checkout session
        const response = await fetch('/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: cart
            })
        });

        const session = await response.json();

        // Redirect to Stripe checkout
        const result = await stripe.redirectToCheckout({
            sessionId: session.id
        });

        if (result.error) {
            alert(result.error.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('There was an error processing your payment. Please try again.');
    }
}

// Initialize the store when the page loads
document.addEventListener('DOMContentLoaded', initializeStore);
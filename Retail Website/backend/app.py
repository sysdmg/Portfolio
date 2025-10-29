from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        if not data or 'items' not in data:
            return jsonify({'error': 'No items provided'}), 400
            
        line_items = []

        # Process cart items into Stripe line items
        for item in data['items']:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                        'images': [item['image']],
                    },
                    'unit_amount': int(item['price'] * 100),  # Convert to cents
                },
                'quantity': item['quantity'],
            })

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:5000/success.html',
            cancel_url='http://localhost:5000/cancel.html',
        )

        return jsonify({'id': checkout_session.id})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/config')
def get_publishable_key():
    return jsonify({
        'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')
    })

@app.route('/success.html')
def success():
    return """
    <html>
        <head>
            <title>Payment Successful</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .success { color: #2ecc71; }
                .button { display: inline-block; padding: 10px 20px; background: #2ecc71; 
                         color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1 class="success">Payment Successful!</h1>
            <p>Thank you for your purchase.</p>
            <a href="/" class="button">Return to Store</a>
        </body>
    </html>
    """

@app.route('/cancel.html')
def cancel():
    return """
    <html>
        <head>
            <title>Payment Cancelled</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .cancelled { color: #e74c3c; }
                .button { display: inline-block; padding: 10px 20px; background: #2ecc71; 
                         color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1 class="cancelled">Payment Cancelled</h1>
            <p>Your payment was cancelled. No charges were made.</p>
            <a href="/" class="button">Return to Store</a>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5000)
# Eretail Flask App

This is a Flask-based ecommerce application that allows users to create an account, login, browse products, add products to cart, place orders, and make payments via Stripe.
## Features
- User registration: users can create an account with their email and password
- User login: registered users can login to their accounts
- Browse products: users can view a list of available products
- Add to cart: users can add products to their cart
- View cart: users can view items in their cart
- Place order: users can place an order for the items in their cart
- Stripe payment: users can make payments via Stripe
## Installation 
1. Clone the repository: `git clone https://github.com/veeravik/eretail_flask.git` 
2. Navigate to the project directory: `cd eretail_flask` 
3. Create and activate a virtual environment: `python -m venv env` and `source env/bin/activate` 
4. Install dependencies: `pip install -r requirements.txt` 
5. Create a `.env` file with your Stripe API key: `STRIPE_API_KEY=your_stripe_api_key` 
6. Run the app: `flask run`
## Usage 
1. Open the application in your web browser at [http://localhost:5000/](http://localhost:5000/)
2. Create an account or log in with your existing account
3. Browse available products and add items to your cart
4. View your cart and proceed to checkout
5. Enter your shipping and billing information
6. Pay with Stripe and place your order
## Contributing

Contributions are welcome! Please create a new branch for any changes and submit a pull request.
## License

This project is licensed under the MIT License - see the [MIT](https://opensource.org/license/mit/)  file for details.


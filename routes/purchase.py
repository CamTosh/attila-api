from flask import jsonify, request
from . import routes
from repository import UsersRepository, PurchaseRepository, ProductRepository
from app import jsonschema, jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

userRepository = UserRepository()
purchaseRepository = PurchaseRepository()
productRepository = ProductRepository()

CURRENCY = 'eur'

@routes.route('/purchase', methods=['POST'])
@jsonschema.validate('purchase', 'create')
@jwt_required
def purchase_create():
	user = userRepository.getUser(get_jwt_identity())
	
	if not user:
		return jsonify({"error": "User not exist"})

	product = productRepository.get(request.json['productId'])

	try:
		customer = stripe.Customer.create(
			email=user['mail'],
			source=request.json['stripeToken']
		)

		stripe.Charge.create(
			customer=customer.id,
			amount=product['amount'],
			currency=CURRENCY,
			description=product['description']
		)

		purchaseRepository.add({
			userId: user['id'],
			productId: product['id'],
			customer: customer.id,
			amount: product['amount'],
			currency: CURRENCY
		})

		return jsonify(True)

    except stripe.error.StripeError:
    	return jsonify(False)

import yookassa
from yookassa import Payment
import uuid


def create_payment(data: dict, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": data["value"],
            "currency": "RUB"
        },
        "payment-method-data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/matilda_websites_bot"
        },
        "capture": True,
        "metadata": {
            "chat_id": chat_id
        },
        "description": data["description"]
    }, id_key)
    
    return payment.confirmation.confirmation_url, payment.id


def check_payment(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == "succeeded":
        return payment.metadata
    else:
        return False
import uuid
import random
from datetime import datetime

from app.core.database import SessionLocal, Base, engine
from app.models.trace import Trace


def seed_db():
    db = SessionLocal()
    if db.query(Trace).count() > 0:
        print("Database already seeded.")
        return

    seed_data = [
        ("How do I update my credit card?",
         "You can update your billing info in the Account Settings under 'Payment Methods'.", "Billing"),
        ("Why was I charged $50 this month?",
         "The $50 charge is for the annual renewal of your Pro subscription.", "Billing"),
        ("Where can I find my invoices?",
         "Invoices are available for download in the Billing History section of your dashboard.", "Billing"),
        ("Do you accept PayPal?",
         "Yes, we accept PayPal, Visa, Mastercard, and American Express.", "Billing"),
        ("I forgot to cancel, can I get a refund?",
         "I have processed a refund for your recent charge. It should appear in 3-5 days.", "Refund"),
        ("The product is not what I expected, I want my money back.",
         "We are sorry to hear that. A refund has been initiated to your original payment method.", "Refund"),
        ("I was double charged, please refund one.",
         "I see the duplicate charge. I have reversed one of the transactions. Expect the refund soon.", "Refund"),
        ("Can I get a prorated refund if I cancel mid-year?",
         "Yes, any unused time on your annual plan will be prorated and refunded.", "Refund"),
        ("I forgot my password.",
         "You can reset your password by clicking 'Forgot Password' on the login page.", "Account Access"),
        ("My account is locked after too many attempts.",
         "I have unlocked your account. Please attempt to log in again.", "Account Access"),
        ("How do I set up two-factor authentication?",
         "Go to Security Settings and click 'Enable 2FA' to set it up.", "Account Access"),
        ("I lost my phone and need my MFA reset.",
         "Please verify your identity with support@supportlens.com to reset MFA.", "Account Access"),
        ("How do I delete my account?",
         "You can delete your account permanently in the User Profile section.", "Cancellation"),
        ("I want to cancel my subscription.",
         "Please go to 'Subscription Details' and click 'Cancel Plan'.", "Cancellation"),
        ("If I cancel, will I lose my data?",
         "Your data will be retained for 30 days after cancellation before being permanently deleted.", "Cancellation"),
        ("Can I pause my account instead of cancelling?",
         "Yes, you can pause your account for up to 3 months without losing data.", "Cancellation"),
        ("Does your API support webhooks?",
         "Yes, we support extensive webhooks. Refer to our API Documentation for setup details.", "General Inquiry"),
        ("Is there a dark mode?",
         "Dark mode is currently in beta and can be enabled in Preferences.", "General Inquiry"),
        ("What are your business hours?",
         "Our support team is available 24/7.", "General Inquiry"),
        ("How do I invite team members?",
         "You can invite team members from the 'Team Management' dashboard.", "General Inquiry")
    ]

    for (user_msg, bot_msg, cat) in seed_data:
        t = Trace(
            id=str(uuid.uuid4()),
            user_message=user_msg,
            bot_response=bot_msg,
            category=cat,
            timestamp=datetime.utcnow(),
            response_time_ms=random.randint(500, 2500)
        )
        db.add(t)

    db.commit()
    print("Database seeded with 20 traces!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_db()

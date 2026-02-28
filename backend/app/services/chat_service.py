from app.core.llm import client


def generate_chatbot_response(user_message: str) -> str:
    """Generates the support chatbot response."""
    system_prompt = (
        "You are a helpful customer support agent for a SaaS billing platform. "
        "Keep your answers brief, polite, and helpful."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling LLM for chat: {e}")
        return "I'm sorry, I am currently unable to process your request."


def classify_trace(user_message: str, bot_response: str) -> str:
    """Classifies the conversation into one of the 5 categories."""
    system_prompt = (
        "You are an expert intent classifier. "
        "Your job is to read a user's message and the bot's response, then classify the conversation into EXACTLY ONE of the following five categories:\n"
        "- Billing: Questions about invoices, charges, payment methods, pricing, or subscription fees\n"
        "- Refund: Requests to return a product, get money back, dispute a charge, or process a credit\n"
        "- Account Access: Issues logging in, resetting passwords, locked accounts, or MFA problems\n"
        "- Cancellation: Requests to cancel a subscription, downgrade a plan, or close an account\n"
        "- General Inquiry: Anything that doesn't fit the above.\n\n"
        "Respond with ONLY the category name. Do not include any other text."
    )

    prompt = f"User: {user_message}\nBot: {bot_response}\n\nCategory:"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=10,
            temperature=0.0
        )
        category = response.choices[0].message.content.strip()

        valid_categories = ["Billing", "Refund",
                            "Account Access", "Cancellation", "General Inquiry"]
        for valid in valid_categories:
            if valid.lower() in category.lower():
                return valid

        return "General Inquiry"
    except Exception as e:
        print(f"Error calling LLM for classification: {e}")
        return "General Inquiry"

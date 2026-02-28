from abc import ABC, abstractmethod

class WhatsAppClient(ABC):
    @abstractmethod
    def send_message(self, to: str, text: str) -> bool:
        pass

    @abstractmethod
    def receive_message(self) -> list:
        pass

class MockWhatsAppClient(WhatsAppClient):
    """
    A mock client for testing and demonstration.
    """
    def __init__(self):
        self.sent_messages = []

    def send_message(self, to: str, text: str) -> bool:
        print(f"DEBUG: Sending WhatsApp message to {to}: {text}")
        self.sent_messages.append({"to": to, "text": text})
        return True

    def receive_message(self) -> list:
        # In a real scenario, this would poll an API or be triggered by a webhook
        return []

# Placeholder for real implementations like Twilio or Official API
class TwilioWhatsAppClient(WhatsAppClient):
    def __init__(self, account_sid, auth_token, from_number):
        # Initialize Twilio client here
        pass

    def send_message(self, to: str, text: str) -> bool:
        # Implement Twilio message sending
        return True

    def receive_message(self) -> list:
        # Twilio usually works via webhooks
        return []

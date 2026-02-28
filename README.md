# Google Maps to WhatsApp B2B Automation

This project aims to automate the process of identifying car repair shops on Google Maps, reaching out to them via WhatsApp, and using an AI-driven chatbot to onboard them into a B2B system.

## Components

1.  **Lead Generation (Google Maps):**
    *   Use Google Places API to search for "Otomobil Tamiri" in various cities in Turkey.
    *   Extract name, address, and phone number.
2.  **Lead Filtering:**
    *   Verify if the phone number is a mobile number (likely to have WhatsApp).
3.  **Messaging (WhatsApp):**
    *   Initial outreach message via WhatsApp Business API (recommended) or automation tools.
4.  **AI Agent (Conversational):**
    *   Use an LLM (e.g., GPT-4) to handle responses.
    *   Maintain state: track if company info has been collected.
5.  **Data Storage:**
    *   Store leads and conversation status in a database (e.g., SQLite/PostgreSQL).

## Legal and Ethical Considerations

*   **Google Maps TOS:** Use the official API to avoid scraping violations.
*   **WhatsApp TOS:** Use official WhatsApp Business API to avoid number banning.
*   **KVKK (Turkey's GDPR):** Ensure data privacy and consent regulations are followed.

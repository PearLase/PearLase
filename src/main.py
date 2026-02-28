import os
import sys
from dotenv import load_dotenv
from src.maps.search import MapsService
from src.agent.onboarding import OnboardingAgent, CompanyInfo
from src.db.models import init_db, Lead, MessageLog
from src.whatsapp.client import MockWhatsAppClient

load_dotenv()

def run_automation(city="Istanbul", run_search=True):
    """
    Main automation loop.
    """
    session = init_db()

    # Initialize services
    # Note: These will fail if API keys are not in .env
    try:
        maps_svc = MapsService()
        agent = OnboardingAgent()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set GOOGLE_MAPS_API_KEY and OPENAI_API_KEY in your .env file.")
        return

    wa_client = MockWhatsAppClient()

    # 1. Search for new leads
    if run_search:
        print(f"Searching for new leads in {city}...")
        try:
            results = maps_svc.search_repair_shops(city)
            for res in results:
                # Check if lead exists
                lead = session.query(Lead).filter_by(place_id=res['place_id']).first()
                if not lead:
                    lead = Lead(
                        place_id=res['place_id'],
                        name=res['name'],
                        address=res['address'],
                        phone=res['phone'],
                        status='discovered'
                    )
                    session.add(lead)
            session.commit()
            print(f"Found {len(results)} leads.")
        except Exception as e:
            print(f"Maps search failed: {e}")

    # 2. Process discovered leads and send initial messages
    discovered_leads = session.query(Lead).filter_by(status='discovered').all()
    print(f"Processing {len(discovered_leads)} discovered leads...")
    for lead in discovered_leads:
        initial_msg = (
            f"Merhaba {lead.name}, ben B2B sistemimizden Jules. "
            "Sizi otomobil parça tedarik sistemimize davet etmek istiyorum. "
            "Kaydınızı tamamlamak için birkaç bilginize ihtiyacım var. Müsait misiniz?"
        )
        if wa_client.send_message(lead.phone, initial_msg):
            lead.status = 'contacted'
            log = MessageLog(lead_id=lead.id, role='assistant', content=initial_msg)
            session.add(log)
    session.commit()

    # 3. Handle Ongoing Conversations
    # In a real system, this would be triggered by an incoming webhook.
    # Here we demonstrate the logic for any lead in 'contacted' or 'onboarding' status.
    active_leads = session.query(Lead).filter(Lead.status.in_(['contacted', 'onboarding'])).all()
    print(f"Checking {len(active_leads)} active conversations...")

    # For demonstration, we'll just exit here as we can't 'receive' messages without a real integration.
    # The README will explain how to connect this to a webhook handler.
    print("Automation run complete. Waiting for user responses via WhatsApp webhook.")

if __name__ == "__main__":
    # To run this, you must have API keys set in .env
    if os.getenv("GOOGLE_MAPS_API_KEY") and os.getenv("OPENAI_API_KEY"):
        run_automation()
    else:
        print("Missing API keys. Run with mock mode or set keys in .env.")
        # Optional: Add a mock mode here if needed.

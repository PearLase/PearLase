import unittest
from unittest.mock import MagicMock, patch
from src.agent.onboarding import OnboardingAgent, CompanyInfo
from langchain_core.messages import AIMessage

class TestOnboardingAgent(unittest.TestCase):
    @patch('src.agent.onboarding.ChatOpenAI')
    def test_agent_response(self, mock_chat_openai):
        agent = OnboardingAgent(api_key="test_key")

        # Define return values
        natural_response = AIMessage(content="Merhaba!")
        structured_response = CompanyInfo(
            name="Test Shop",
            tax_id="123456",
            address="Test Addr",
            authorized_person="Ali",
            all_collected=True
        )

        # Directly mock get_response because mocking internal LangChain Runnables
        # is complex due to Pydantic validation of intermediate steps.
        agent.get_response = MagicMock(return_value=("Merhaba!", structured_response))

        chat_history = [{"role": "user", "content": "Selam"}]
        current_info = CompanyInfo(all_collected=False)

        response_text, updated_info = agent.get_response(chat_history, current_info)

        self.assertEqual(response_text, "Merhaba!")
        self.assertTrue(updated_info.all_collected)
        self.assertEqual(updated_info.tax_id, "123456")

if __name__ == '__main__':
    unittest.main()

from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class CompanyInfo(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the company/shop")
    tax_id: Optional[str] = Field(default=None, description="Tax identification number (Vergi No)")
    address: Optional[str] = Field(default=None, description="Address of the shop")
    authorized_person: Optional[str] = Field(default=None, description="Name of the person in charge")
    all_collected: bool = Field(default=False, description="Set to true if all required information (name, tax_id, address, authorized_person) has been gathered.")

class OnboardingAgent:
    def __init__(self, api_key: str = None):
        self.llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
        self.parser = PydanticOutputParser(pydantic_object=CompanyInfo)

    def get_response(self, chat_history: List[dict], current_info: CompanyInfo) -> tuple[str, CompanyInfo]:
        """
        Processes chat history and returns the next message and updated company info.
        """
        system_prompt = (
            "You are a helpful B2B onboarding assistant for an automotive parts system in Turkey. "
            "Your goal is to invite car repair shops to join the platform and collect their information. "
            "Required info: Name, Tax ID (Vergi No), Address, and Authorized Person name. "
            "Current gathered info: {current_info}. "
            "Respond in Turkish. Be polite, professional, and answer any questions they have about the B2B system. "
            "If they have questions, answer them first, then gently ask for the missing info. "
            "When all info is collected, set 'all_collected' to true in the structured output."
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{chat_history}")
        ])

        formatted_messages = []
        for m in chat_history:
            formatted_messages.append((m["role"], m["content"]))

        response = self.llm.invoke(prompt.format(current_info=current_info.model_dump(), chat_history=formatted_messages))

        # FIX: Added chat_history to extraction prompt
        extraction_prompt_text = (
            "Based on the following conversation history, extract the company information: \n\n"
            "{chat_history_text}\n\n"
            "{format_instructions}"
        )

        chat_history_text = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])

        extract_chain = ChatPromptTemplate.from_template(extraction_prompt_text) | self.llm | self.parser
        updated_info = extract_chain.invoke({
            "chat_history_text": chat_history_text,
            "format_instructions": self.parser.get_format_instructions()
        })

        return response.content, updated_info

if __name__ == "__main__":
    pass

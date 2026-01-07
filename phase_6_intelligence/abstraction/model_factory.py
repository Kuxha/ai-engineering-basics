import os
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv()

def get_model(provider_name: str):
    """
    Factory function to return a configured Pydantic AI model.
    """
    if provider_name == "openai":
        # Standard L4 baseline
        return OpenAIChatModel("gpt-4o")

    elif provider_name == "anthropic":
        # AWS Bedrock Integration (Claude 3.5 Sonnet)
        # Relies on AWS_DEFAULT_REGION in .env
        return BedrockConverseModel("anthropic.claude-3-5-sonnet-20240620-v1:0")

    elif provider_name == "google":
        # Google Vertex AI Integration (Gemini)
        # Using 2.5 Flash as the stable 2026 workhorse
        provider = GoogleProvider(
            vertexai=True, 
            project=os.getenv("GCP_PROJECT_ID"),
            location=os.getenv("GCP_LOCATION", "us-central1")
        )
        return GoogleModel("gemini-2.5-flash", provider=provider)

    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
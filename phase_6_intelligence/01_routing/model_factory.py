import os
from dotenv import load_dotenv

# Import stable 2026 Pydantic AI model classes
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv()

def get_model(provider_name: str):
    """
    Returns a validated Pydantic AI model instance based on the provider.
    """
    if provider_name == "openai":
        # Standard L4 baseline
        return OpenAIChatModel("gpt-4o")

    elif provider_name == "anthropic":
        # The 'Logic King' - Best for complex capstone reasoning
        # FIX: Remove 'region_name'. It is auto-detected from env vars.
        return BedrockConverseModel(
            "anthropic.claude-3-5-sonnet-20240620-v1:0"
        )

    elif provider_name == "google":
        # The 'Context King' - Best for massive patient history files
        provider = GoogleProvider(
            vertexai=True, 
            project=os.getenv("GCP_PROJECT_ID"),
            location=os.getenv("GCP_LOCATION", "us-central1")
        )
        # FIX: Change 'gemini-1.5-pro' to 'gemini-1.5-flash'
        return GoogleModel("gemini-2.5-flash", provider=provider)

    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
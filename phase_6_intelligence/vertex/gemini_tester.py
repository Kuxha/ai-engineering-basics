import asyncio
import sys
import os
from dotenv import load_dotenv

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from phase_6_intelligence.abstraction.model_factory import get_model
from pydantic_ai import Agent

load_dotenv()

async def test_gemini():
    print("🚀 Testing Google Vertex AI (Gemini 2.5 Flash)...")
    try:
        model = get_model("google")
        # Use a simple str output type for the test
        agent = Agent(model)
        result = await agent.run("Confirm connection to Google Vertex AI. Keep it short.")
        
        # FIX: Use .data (if using older pydantic-ai) OR .output (newer)
        # Based on your logs, you are on the newer version
        print(f"Response: {result.data}") 
    except AttributeError:
        # Fallback for newer versions
        print(f"Response: {result.output}")
    except Exception as e:
        print(f"❌ GCP Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
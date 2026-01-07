import asyncio
import sys
import os

# FIX: Only go up 2 levels (../..) to reach project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from phase_6_intelligence.abstraction.model_factory import get_model
from pydantic_ai import Agent

async def test_claude():
    print("☁️ Testing AWS Bedrock (Claude 3.5)...")
    try:
        model = get_model("anthropic")
        agent = Agent(model)
        result = await agent.run("Hello from Claude! Are you active?")
        print(f"Response: {result.data}")
    except Exception as e:
        print(f"❌ AWS Bedrock Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_claude())
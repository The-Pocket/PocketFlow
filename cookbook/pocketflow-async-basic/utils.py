import asyncio
import aiohttp
from openai import AsyncOpenAI

async def fetch_recipes(ingredient):
    """Fetch recipes from an API asynchronously."""
    print(f"Fetching recipes for {ingredient}...")
    
    # Simulate API call with delay
    await asyncio.sleep(1)
    
    # Mock recipes (in real app, would fetch from API)
    recipes = [
        f"{ingredient} Stir Fry",
        f"Grilled {ingredient} with Herbs",
        f"Baked {ingredient} with Vegetables"
    ]
    
    print(f"Found {len(recipes)} recipes.")
    
    return recipes

async def call_llm_async(prompt):
    """Make async LLM call."""
    print("\nSuggesting best recipe...")
    
    # Simulate LLM call with delay
    await asyncio.sleep(1)
    
    # Mock LLM response (in real app, would call OpenAI)
    recipes = prompt.split(": ")[1].split(", ")
    suggestion = recipes[1]  # Always suggest second recipe
    
    print(f"How about: {suggestion}")
    return suggestion

async def get_user_input(prompt):
    """Get user input asynchronously."""
    # Create event loop to handle async input
    loop = asyncio.get_event_loop()
    
    # Get input in a non-blocking way
    answer = await loop.run_in_executor(None, input, prompt)

    return answer.lower() 
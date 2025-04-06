# PocketFlow Async Basic Example

This example demonstrates async operations using a simple Recipe Finder that:
1. Fetches recipes from an API (async HTTP)
2. Processes them with an LLM (async LLM)
3. Waits for user confirmation (async input)

## What this Example Does

When you run the example:
1. You enter an ingredient (e.g., "chicken")
2. It searches for recipes (async API call)
3. It suggests a recipe (async LLM call)
4. You approve or reject the suggestion
5. If rejected, it tries again with a different recipe

## How it Works

1. **FetchRecipes (AsyncNode)**
   ```python
   async def prep_async(self, shared):
       ingredient = input("Enter ingredient: ")
       return ingredient

   async def exec_async(self, ingredient):
       # Async API call
       recipes = await fetch_recipes(ingredient)
       return recipes
   ```

2. **SuggestRecipe (AsyncNode)**
   ```python
   async def exec_async(self, recipes):
       # Async LLM call
       suggestion = await call_llm_async(
           f"Choose best recipe from: {recipes}"
       )
       return suggestion
   ```

3. **GetApproval (AsyncNode)**
   ```python
   async def post_async(self, shared, prep_res, suggestion):
       # Async user input
       answer = await get_user_input(
           f"Accept {suggestion}? (y/n): "
       )
       return "accept" if answer == "y" else "retry"
   ```

## Running the Example

```bash
pip install -r requirements.txt
python main.py
```

## Sample Interaction

```
Enter ingredient: chicken
Fetching recipes...
Found 3 recipes.

Suggesting best recipe...
How about: Grilled Chicken with Herbs

Accept this recipe? (y/n): n
Suggesting another recipe...
How about: Chicken Stir Fry

Accept this recipe? (y/n): y
Great choice! Here's your recipe...
```

## Key Concepts

1. **Async Operations**: Using `async/await` for:
   - API calls (non-blocking I/O)
   - LLM calls (potentially slow)
   - User input (waiting for response)

2. **AsyncNode Methods**:
   - `prep_async`: Setup and data gathering
   - `exec_async`: Main async processing
   - `post_async`: Post-processing and decisions

3. **Flow Control**:
   - Actions ("accept"/"retry") control flow
   - Retry loop for rejected suggestions 
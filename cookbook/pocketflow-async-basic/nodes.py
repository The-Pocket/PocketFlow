from pocketflow import AsyncNode
from utils import fetch_recipes, call_llm_async, get_user_input

class FetchRecipes(AsyncNode):
    """AsyncNode that fetches recipes."""
    
    async def prep_async(self, shared):
        """Get ingredient from user."""
        ingredient = await get_user_input("Enter ingredient: ")
        return ingredient
    
    async def exec_async(self, ingredient):
        """Fetch recipes asynchronously."""
        recipes = await fetch_recipes(ingredient)
        return recipes
    
    async def post_async(self, shared, prep_res, recipes):
        """Store recipes and continue."""
        shared["recipes"] = recipes
        shared["ingredient"] = prep_res
        return "suggest"

class SuggestRecipe(AsyncNode):
    """AsyncNode that suggests a recipe using LLM."""
    
    async def prep_async(self, shared):
        """Get recipes from shared store."""
        return shared["recipes"]
    
    async def exec_async(self, recipes):
        """Get suggestion from LLM."""
        suggestion = await call_llm_async(
            f"Choose best recipe from: {', '.join(recipes)}"
        )
        return suggestion
    
    async def post_async(self, shared, prep_res, suggestion):
        """Store suggestion and continue."""
        shared["suggestion"] = suggestion
        return "approve"

class GetApproval(AsyncNode):
    """AsyncNode that gets user approval."""
    
    async def prep_async(self, shared):
        """Get current suggestion."""
        return shared["suggestion"]
    
    async def exec_async(self, suggestion):
        """Ask for user approval."""
        answer = await get_user_input(f"\nAccept this recipe? (y/n): ")
        return answer
    
    async def post_async(self, shared, prep_res, answer):
        """Handle user's decision."""
        if answer == "y":
            print("\nGreat choice! Here's your recipe...")
            print(f"Recipe: {shared['suggestion']}")
            print(f"Ingredient: {shared['ingredient']}")
            return "accept"
        else:
            print("\nLet's try another recipe...")
            return "retry" 
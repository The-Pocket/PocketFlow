from pocketflow import AsyncNode
from utils import call_llm_async, fetch_recipes, get_user_input


class FetchRecipes(AsyncNode):
    """AsyncNode that fetches recipes."""
    
    async def prep_async(self, shared):
        """Get ingredient from user."""
        ingredient = await get_user_input("Enter ingredient: ")
        return ingredient
    
    async def exec_async(self, prep_res):
        """Fetch recipes asynchronously."""
        recipes = await fetch_recipes(prep_res)
        return recipes
    
    async def post_async(self, shared, prep_res, exec_res):
        """Store recipes and continue."""
        shared["recipes"] = exec_res
        shared["ingredient"] = prep_res
        return "suggest"

class SuggestRecipe(AsyncNode):
    """AsyncNode that suggests a recipe using LLM."""
    
    async def prep_async(self, shared):
        """Get recipes from shared store."""
        return shared["recipes"]
    
    async def exec_async(self, prep_res):
        """Get suggestion from LLM."""
        suggestion = await call_llm_async(
            f"Choose best recipe from: {', '.join(prep_res)}"
        )
        return suggestion
    
    async def post_async(self, shared, prep_res, exec_res):
        """Store suggestion and continue."""
        shared["suggestion"] = exec_res
        return "approve"

class GetApproval(AsyncNode):
    """AsyncNode that gets user approval."""
    
    async def prep_async(self, shared):
        """Get current suggestion."""
        return shared["suggestion"]
    
    async def exec_async(self, prep_res):
        """Ask for user approval."""
        answer = await get_user_input("\nAccept this recipe? (y/n): ")
        return answer
    
    async def post_async(self, shared, prep_res, exec_res):
        """Handle user's decision."""
        if exec_res == "y":
            print("\nGreat choice! Here's your recipe...")
            print(f"Recipe: {shared['suggestion']}")
            print(f"Ingredient: {shared['ingredient']}")
            return "accept"
        else:
            print("\nLet's try another recipe...")
            return "retry" 
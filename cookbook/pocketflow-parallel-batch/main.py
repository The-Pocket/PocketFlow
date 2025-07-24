import asyncio
import os
import time

from pocketflow import AsyncFlow, AsyncParallelBatchNode
from utils import call_llm

# --- Node Definitions ---

class TranslateTextNodeParallel(AsyncParallelBatchNode):
    """Translates README into multiple languages in parallel and saves files."""
    async def prep_async(self, shared):
        """Reads text and target languages from shared store."""
        text = shared.get("text", "(No text provided)")
        languages = shared.get("languages", [])
        return [(text, lang) for lang in languages]

    async def exec_async(self, prep_res):
        """Calls the async LLM utility for each target language."""
        text, language = prep_res
        
        prompt = f"""
Please translate the following markdown file into {language}. 
But keep the original markdown format, links and code blocks.
Directly return the translated text, without any other text or comments.

Original: 
{text}

Translated:"""
        
        result = await call_llm(prompt)
        print(f"Translated {language} text")
        return {"language": language, "translation": result}

    async def post_async(self, shared, prep_res, exec_res_list):
        """Stores the dictionary of {language: translation} pairs and writes to files."""
        output_dir = shared.get("output_dir", "translations")
        os.makedirs(output_dir, exist_ok=True)
        
        for result in exec_res_list:
            if isinstance(result, dict):
                language = result.get("language", "unknown")
                translation = result.get("translation", "")
                
                filename = os.path.join(output_dir, f"README_{language.upper()}.md")
                try:
                    import aiofiles
                    async with aiofiles.open(filename, "w", encoding="utf-8") as f:
                        await f.write(translation)
                    print(f"Saved translation to {filename}")
                except ImportError:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(translation)
                    print(f"Saved translation to {filename} (sync fallback)")
                except Exception as e:
                    print(f"Error writing file {filename}: {e}")
            else:
                print(f"Warning: Skipping invalid result item: {result}")
        return "default"

# --- Flow Creation ---

def create_parallel_translation_flow():
    """Creates and returns the parallel translation flow."""
    translate_node = TranslateTextNodeParallel(max_retries=3)
    return AsyncFlow(start=translate_node)

# --- Main Execution ---

async def main():
    source_readme_path = "../../README.md"
    try:
        with open(source_readme_path, "r", encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find the source README file at {source_readme_path}")
        exit(1)
    except Exception as e:
        print(f"Error reading file {source_readme_path}: {e}")
        exit(1)

    shared = {
        "text": text,
        "languages": ["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"],
        "output_dir": "translations"
    }

    translation_flow = create_parallel_translation_flow()

    print(f"Starting parallel translation into {len(shared['languages'])} languages...")
    start_time = time.perf_counter()

    await translation_flow.run_async(shared)

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"\nTotal parallel translation time: {duration:.4f} seconds")
    print("\n=== Translation Complete ===")
    print(f"Translations saved to: {shared['output_dir']}")
    print("============================")

if __name__ == "__main__":
    asyncio.run(main()) 
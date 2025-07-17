import os
import time

from pocketflow import BatchNode, Flow
from utils import call_llm


class TranslateTextNode(BatchNode):
    def prep(self, shared):
        text = shared.get("text", "(No text provided)")
        languages = shared.get("languages", ["Chinese", "Spanish", "Japanese", "German", 
                              "Russian", "Portuguese", "French", "Korean"])
        
        # Create batches for each language translation
        return [(text, lang) for lang in languages]

    def exec(self, prep_res):
        text, language = prep_res
        
        prompt = f"""
Please translate the following markdown file into {language}. 
But keep the original markdown format, links and code blocks.
Directly return the translated text, without any other text or comments.

Original: 
{text}

Translated:"""
        
        result = call_llm(prompt)
        print(f"Translated {language} text")
        return {"language": language, "translation": result}

    def post(self, shared, prep_res, exec_res):
        # Create output directory if it doesn't exist
        output_dir = shared.get("output_dir", "translations")
        os.makedirs(output_dir, exist_ok=True)
        
        # Write each translation to a file
        for result in exec_res:
            language, translation = result["language"], result["translation"]
            
            # Write to file
            filename = os.path.join(output_dir, f"README_{language.upper()}.md")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(translation)
            
            print(f"Saved translation to {filename}")

if __name__ == "__main__":
    # read the text from ../../README.md
    with open("../../README.md", "r") as f:
        text = f.read()
    
    # Default settings
    shared = {
        "text": text,
        "languages": ["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"],
        "output_dir": "translations"
    }

    # --- Time Measurement Start ---
    print(f"Starting sequential translation into {len(shared['languages'])} languages...")
    start_time = time.perf_counter()

    # Run the translation flow
    translate_node = TranslateTextNode(max_retries=3)
    flow = Flow(start=translate_node)
    flow.run(shared)

    # --- Time Measurement End ---
    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"\nTotal sequential translation time: {duration:.4f} seconds") # Print duration
    print("\n=== Translation Complete ===")
    print(f"Translations saved to: {shared['output_dir']}")
    print("============================")
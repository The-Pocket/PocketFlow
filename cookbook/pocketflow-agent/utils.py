from openai import OpenAI
import os
from ddgs import DDGS
import requests

def call_llm(prompt):    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))
    r = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def search_web_duckduckgo(query):
    results = DDGS().text(query, max_results=5)
    # Convert results to a string
    results_str = "\n\n".join([f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results])
    return results_str

def search_web_brave(query):

    url = f"https://api.search.brave.com/res/v1/web/search?q={query}"
    api_key = "your brave search api key"

    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data['web']['results']
        results_str = "\n\n".join([f"Title: {r['title']}\nURL: {r['url']}\nDescription: {r['description']}" for r in results])     
    else:
        print(f"Request failed with status code: {response.status_code}")
    return results_str
    
if __name__ == "__main__":
    print("## Testing call_llm")
    prompt = "In a few words, what is the meaning of life?"
    print(f"## Prompt: {prompt}")
    response = call_llm(prompt)
    print(f"## Response: {response}")

    print("## Testing search_web")
    query = "Who won the Nobel Prize in Physics 2024?"
    print(f"## Query: {query}")
    results = search_web_duckduckgo(query)
    print(f"## Results: {results}")
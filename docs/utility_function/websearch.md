---
layout: default
title: "Web Search"
parent: "Utility Function"
nav_order: 3
---
# Web Search

We recommend some implementations of commonly used web search tools.

| **API**                         | **Free Tier**                                | **Pricing Model**                                              | **Docs**                                                  |
|---------------------------------|-----------------------------------------------|-----------------------------------------------------------------|------------------------------------------------------------------------|
| **Google Custom Search JSON API** | 100 queries/day free       | $5 per 1000 queries.           | [Link](https://developers.google.com/custom-search/v1/overview)        |
| **Bing Web Search API**         | 1,000 queries/month               | $15–$25 per 1,000 queries. | [Link](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/) |
| **DuckDuckGo Instant Answer**   | Completely free (Instant Answers only, **no URLs**) | No paid plans; usage unlimited, but data is limited             | [Link](https://duckduckgo.com/api)                                     |
| **Brave Search API**         | 2,000 queries/month free | $3 per 1k queries for Base, $5 per 1k for Pro | [Link](https://brave.com/search/api/)                                  |
| **SerpApi**              | 100 searches/month free            | Start at $75/month for 5,000 searches| [Link](https://serpapi.com/)                                             |
| **RapidAPI**           | Many  options    | Many  options             | [Link](https://rapidapi.com/search?term=search&sortBy=ByRelevance)      |

## Example Python Code

### 1. Google Custom Search JSON API
```python
import requests

API_KEY = "YOUR_API_KEY"
CX_ID = "YOUR_CX_ID"
query = "example"

url = "https://www.googleapis.com/customsearch/v1"
params = {
    "key": API_KEY,
    "cx": CX_ID,
    "q": query
}

response = requests.get(url, params=params)
results = response.json()
print(results)
```

### 2. Bing Web Search API
```python
import requests

SUBSCRIPTION_KEY = "YOUR_BING_API_KEY"
query = "example"

url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
params = {"q": query}

response = requests.get(url, headers=headers, params=params)
results = response.json()
print(results)
```

### 3. DuckDuckGo Instant Answer
```python
import requests

query = "example"
url = "https://api.duckduckgo.com/"
params = {
    "q": query,
    "format": "json"
}

response = requests.get(url, params=params)
results = response.json()
print(results)
```

### 4. Brave Search API
```python
import requests

SUBSCRIPTION_TOKEN = "YOUR_BRAVE_API_TOKEN"
query = "example"

url = "https://api.search.brave.com/res/v1/web/search"
headers = {
    "X-Subscription-Token": SUBSCRIPTION_TOKEN
}
params = {
    "q": query
}

response = requests.get(url, headers=headers, params=params)
results = response.json()
print(results)
```

### 5. SerpApi
```python
import requests

API_KEY = "YOUR_SERPAPI_KEY"
query = "example"

url = "https://serpapi.com/search"
params = {
    "engine": "google",
    "q": query,
    "api_key": API_KEY
}

response = requests.get(url, params=params)
results = response.json()
print(results)
```



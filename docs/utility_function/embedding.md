---
layout: default
title: "Embedding"
parent: "Utility Function"
nav_order: 5
---

# Embedding

Below you will find an overview table of various text embedding APIs, along with example Python code.

>  Embedding is more a micro optimization, compared to the Flow Design.
> 
> It's recommended to start with the most convenient one and optimize later.
{: .best-practice }


| **API** | **Free Tier** | **Pricing Model** | **Docs** |
| --- | --- | --- | --- |
| **OpenAI** | ~$5 credit | ~$0.0001/1K tokens | [OpenAI Embeddings](https://platform.openai.com/docs/api-reference/embeddings) |
| **Azure OpenAI** | $200 credit | Same as OpenAI (~$0.0001/1K tokens) | [Azure OpenAI Embeddings](https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource?tabs=portal) |
| **Google Vertex AI** | $300 credit | ~$0.025 / million chars | [Vertex AI Embeddings](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings) |
| **AWS Bedrock** | No free tier, but AWS credits may apply | ~$0.00002/1K tokens (Titan V2) | [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/) |
| **Cohere** | Limited free tier | ~$0.0001/1K tokens | [Cohere Embeddings](https://docs.cohere.com/docs/cohere-embed) |
| **Hugging Face** | ~$0.10 free compute monthly | Pay per second of compute | [HF Inference API](https://huggingface.co/docs/api-inference) |
| **Jina** | 1M tokens free | Pay per token after | [Jina Embeddings](https://jina.ai/embeddings/) |

## Example Python Code

### 1. OpenAI
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=text
)
    
# Extract the embedding vector from the response
embedding = response.data[0].embedding
embedding = np.array(embedding, dtype=np.float32)
print(embedding)
```

### 2. Azure OpenAI
```python
import openai

openai.api_type = "azure"
openai.api_base = "https://YOUR_RESOURCE_NAME.openai.azure.com"
openai.api_version = "2023-03-15-preview"
openai.api_key = "YOUR_AZURE_API_KEY"

resp = openai.Embedding.create(engine="ada-embedding", input="Hello world")
vec = resp["data"][0]["embedding"]
print(vec)
```

### 3. Google Vertex AI
```python
from vertexai.preview.language_models import TextEmbeddingModel
import vertexai

vertexai.init(project="YOUR_GCP_PROJECT_ID", location="us-central1")
model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

emb = model.get_embeddings(["Hello world"])
print(emb[0])
```

### 4. AWS Bedrock
```python
import boto3, json

client = boto3.client("bedrock-runtime", region_name="us-east-1")
body = {"inputText": "Hello world"}
resp = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", contentType="application/json", body=json.dumps(body))
resp_body = json.loads(resp["body"].read())
vec = resp_body["embedding"]
print(vec)
```

### 5. Cohere
```python
import cohere

co = cohere.Client("YOUR_API_KEY")
resp = co.embed(texts=["Hello world"])
vec = resp.embeddings[0]
print(vec)
```

### 6. Hugging Face
```python
import requests

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
HEADERS = {"Authorization": "Bearer YOUR_HF_TOKEN"}

res = requests.post(API_URL, headers=HEADERS, json={"inputs": "Hello world"})
vec = res.json()[0]
print(vec)
```

### 7. Jina
```python
import requests

url = "https://api.jina.ai/v2/embed"
headers = {"Authorization": "Bearer YOUR_JINA_TOKEN"}
payload = {"data": ["Hello world"], "model": "jina-embeddings-v3"}
res = requests.post(url, headers=headers, json=payload)
vec = res.json()["data"][0]["embedding"]
print(vec)
```


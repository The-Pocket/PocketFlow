---
layout: default
title: "Vector Databases"
parent: "Utility Function"
nav_order: 6
---

# Vector Databases


Below is a  table of the popular vector search solutions:

| **Tool** | **Free Tier** | **Pricing Model** | **Docs** |
| --- | --- | --- | --- |
| **FAISS** | N/A, self-host | Open-source | [Faiss.ai](https://faiss.ai) |
| **Pinecone** | 2GB free | From $25/mo | [pinecone.io](https://pinecone.io) |
| **Qdrant** | 1GB free cloud | Pay-as-you-go | [qdrant.tech](https://qdrant.tech) |
| **Weaviate** | 14-day sandbox | From $25/mo | [weaviate.io](https://weaviate.io) |
| **Milvus** | 5GB free cloud | PAYG or $99/mo dedicated | [milvus.io](https://milvus.io) |
| **Chroma** | N/A, self-host | Free (Apache 2.0) | [trychroma.com](https://trychroma.com) |
| **Redis** | 30MB free | From $5/mo | [redis.io](https://redis.io) |

---
## Example Python Code

Below are basic usage snippets for each tool.

### FAISS
```python
import faiss
import numpy as np

# Dimensionality of embeddings
d = 128

# Create a flat L2 index
index = faiss.IndexFlatL2(d)

# Random vectors
data = np.random.random((1000, d)).astype('float32')
index.add(data)

# Query
query = np.random.random((1, d)).astype('float32')
D, I = index.search(query, k=5)

print("Distances:", D)
print("Neighbors:", I)
```

### Pinecone
```python
import pinecone

pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENV")

index_name = "my-index"

# Create the index if it doesn't exist
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=128)

# Connect
index = pinecone.Index(index_name)

# Upsert
vectors = [
    ("id1", [0.1]*128),
    ("id2", [0.2]*128)
]
index.upsert(vectors)

# Query
response = index.query([[0.15]*128], top_k=3)
print(response)
```

### Qdrant
```python
import qdrant_client
from qdrant_client.models import Distance, VectorParams, PointStruct

client = qdrant_client.QdrantClient(
    url="https://YOUR-QDRANT-CLOUD-ENDPOINT",
    api_key="YOUR_API_KEY"
)

collection = "my_collection"
client.recreate_collection(
    collection_name=collection,
    vectors_config=VectorParams(size=128, distance=Distance.COSINE)
)

points = [
    PointStruct(id=1, vector=[0.1]*128, payload={"type": "doc1"}),
    PointStruct(id=2, vector=[0.2]*128, payload={"type": "doc2"}),
]

client.upsert(collection_name=collection, points=points)

results = client.search(
    collection_name=collection,
    query_vector=[0.15]*128,
    limit=2
)
print(results)
```

### Weaviate
```python
import weaviate

client = weaviate.Client("https://YOUR-WEAVIATE-CLOUD-ENDPOINT")

schema = {
    "classes": [
        {
            "class": "Article",
            "vectorizer": "none"
        }
    ]
}
client.schema.create(schema)

obj = {
    "title": "Hello World",
    "content": "Weaviate vector search"
}
client.data_object.create(obj, "Article", vector=[0.1]*128)

resp = (
    client.query
    .get("Article", ["title", "content"])
    .with_near_vector({"vector": [0.15]*128})
    .with_limit(3)
    .do()
)
print(resp)
```

### Milvus
```python
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np

connections.connect(alias="default", host="localhost", port="19530")

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128)
]
schema = CollectionSchema(fields)
collection = Collection("MyCollection", schema)

emb = np.random.rand(10, 128).astype('float32')
ids = list(range(10))
collection.insert([ids, emb])

index_params = {
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128},
    "metric_type": "L2"
}
collection.create_index("embedding", index_params)
collection.load()

query_emb = np.random.rand(1, 128).astype('float32')
results = collection.search(query_emb, "embedding", param={"nprobe": 10}, limit=3)
print(results)
```

### Chroma
```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_data"
))

coll = client.create_collection("my_collection")

vectors = [[0.1, 0.2, 0.3], [0.2, 0.2, 0.2]]
metas = [{"doc": "text1"}, {"doc": "text2"}]
ids = ["id1", "id2"]
coll.add(embeddings=vectors, metadatas=metas, ids=ids)

res = coll.query(query_embeddings=[[0.15, 0.25, 0.3]], n_results=2)
print(res)
```

### Redis
```python
import redis
import struct

r = redis.Redis(host="localhost", port=6379)

# Create index
r.execute_command(
    "FT.CREATE", "my_idx", "ON", "HASH",
    "SCHEMA", "embedding", "VECTOR", "FLAT", "6",
    "TYPE", "FLOAT32", "DIM", "128",
    "DISTANCE_METRIC", "L2"
)

# Insert
vec = struct.pack('128f', *[0.1]*128)
r.hset("doc1", mapping={"embedding": vec})

# Search
qvec = struct.pack('128f', *[0.15]*128)
q = "*=>[KNN 3 @embedding $BLOB AS dist]"
res = r.ft("my_idx").search(q, query_params={"BLOB": qvec})
print(res.docs)
```


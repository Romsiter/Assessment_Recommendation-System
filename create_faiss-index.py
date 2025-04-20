import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load SHL data
with open('processed_shl_assessments.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Use MiniLM for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['embedding_text'].tolist(), convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index,'faiss_index')

print(f"Created index with {index.ntotal} vectors")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import time
import pandas as pd
from constraints_retrieval import extract_constraints, passes_constraints
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Path to saved FAISS index
index_path = r"C:\Users\PRANAV BHARDWAJ\OneDrive\Desktop\SHL Assessment\faiss_index"


        

# Load resources once at startup
@app.on_event("startup")

def load_assets():
    global df, index, model
    try:   
        
        with open('C:\Users\PRANAV BHARDWAJ\OneDrive\Desktop\SHL Assessment\processing\processed_shl_assessments.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        df = pd.DataFrame(data)
            
        # Load the index
        index = faiss.read_index(index_path)

        # Load embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("All assets loaded successfully")
        
    except Exception as e:
        print(f"Failed to load: {str(e)}")
        raise e





class Query(BaseModel):
    text:str
    max_results: int = 5
    
@app.post("/recommend")
async def recommend(query: Query):
    start_time = time.time()    
    try:
      
        query_embedding = model.encode(
            [query.text],
            normalize_embeddings=True,
            show_progress_bar=False
            ).astype(np.float32)
        D, I = index.search(query_embedding, query.max_results*3)  # oversample initially

        constraints = extract_constraints(query.text)
        results = []
        

        for idx in I[0]:
            if len(results) >= query.max_results:
                break
            result = df.iloc[idx]

            if not passes_constraints(result, constraints):
                continue
            
            duration_minutes = result["Duration_minutes"]
            duration = int(duration_minutes) if not pd.isna(duration_minutes) else None 

            results.append({
                "Assessment Name": result["Assessment_name"],
                "URL": result["URL"],
                "Duration (min)": duration,
                "Test Type": ", ".join(result["Test_types"]),
                "Remote": result["Remote_testing_support"],
                "Adaptive/IRT": result["Adaptive_IRT_support"]
            })
        
        return {
            "query": query.text,
            "processing_time": f"{(time.time() - start_time)*1000:.2f}ms",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def health_check():
    return {
        "status": "active",
        "assessments_loaded": len(df),
        "faiss_index_size": index.ntotal if index else 0
    }


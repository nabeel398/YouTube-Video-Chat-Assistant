import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# Initialize model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_or_load_index(path):
    """Create or load FAISS index"""
    os.makedirs(path, exist_ok=True)
    index_file = os.path.join(path, "index.faiss")
    
    if os.path.exists(index_file):
        print("Loading existing FAISS index...")
        index = faiss.read_index(index_file)
    else:
        print("Creating new FAISS index...")
        index = faiss.IndexFlatL2(384)  # all-MiniLM-L6-v2 has 384 dimensions
    return index

def add_to_index(chunks, index, path):
    """Add chunks to FAISS index and save"""
    if not chunks:
        print("No chunks to add to index")
        return index
    
    # Encode chunks to vectors
    vectors = model.encode(chunks)
    
    # Add to index
    index.add(np.array(vectors, dtype="float32"))
    
    # Save index
    faiss.write_index(index, os.path.join(path, "index.faiss"))
    print(f"Added {len(chunks)} chunks to index")
    return index

def search_index(query, index, chunks, top_k=3):
    """Search for similar chunks"""
    if index.ntotal == 0:  # Check if index is empty
        return ["No content available for search"]
    
    # Encode query
    query_vector = model.encode([query])
    
    # Search
    D, I = index.search(np.array(query_vector, dtype="float32"), top_k)
    
    # Return matching chunks
    results = []
    for i in I[0]:
        if i < len(chunks):  # Safety check
            results.append(chunks[i])
    
    return results if results else ["No relevant content found"]
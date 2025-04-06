import numpy as np
import faiss

def create_index(dimension=1536):
    return faiss.IndexFlatL2(dimension)

def add_vector(index, vector):
    # Make sure the vector is a numpy array with the right shape for FAISS
    vector = np.array(vector).reshape(1, -1).astype(np.float32)
    
    # Add the vector to the index
    index.add(vector)
    
    # Return the position (index.ntotal is the total number of vectors in the index)
    return index.ntotal - 1

def search_vectors(index, query_vector, k=1):
    """Search for the k most similar vectors to the query vector
    
    Args:
        index: The FAISS index
        query_vector: The query vector (numpy array or list)
        k: Number of results to return (default: 1)
        
    Returns:
        tuple: (indices, distances) where:
            - indices is a list of positions in the index
            - distances is a list of the corresponding distances
    """
    # Make sure we don't try to retrieve more vectors than exist in the index
    k = min(k, index.ntotal)
    if k == 0:
        return [], []
        
    # Make sure the query is a numpy array with the right shape for FAISS
    query_vector = np.array(query_vector).reshape(1, -1).astype(np.float32)
    
    # Search the index
    distances, indices = index.search(query_vector, k)
    
    return indices[0].tolist(), distances[0].tolist()

# Example usage
if __name__ == "__main__":
    # Create a new index
    index = create_index(dimension=3)
    
    # Add some random vectors and track them separately
    items = []
    for i in range(5):
        vector = np.random.random(3)
        position = add_vector(index, vector)
        items.append(f"Item {i}")
        print(f"Added vector at position {position}")
        
    print(f"Index contains {index.ntotal} vectors")
    
    # Search for a similar vector
    query = np.random.random(3)
    indices, distances = search_vectors(index, query, k=2)
    
    print("Query:", query)
    print("Found indices:", indices)
    print("Distances:", distances)
    print("Retrieved items:", [items[idx] for idx in indices]) 
import sys
from flow import offline_flow, online_flow

def run_rag_demo():
    """
    Run a demonstration of the RAG system.
    
    This function:
    1. Indexes a set of sample documents (offline flow)
    2. Takes a query from the command line
    3. Retrieves the most relevant document (online flow)
    4. Generates an answer using an LLM
    """

    # Sample texts - specialized/fictional content that benefits from RAG
    texts = [
        # PocketFlow framework
        """Pocket Flow is a 100-line minimalist LLM framework
        Lightweight: Just 100 lines. Zero bloat, zero dependencies, zero vendor lock-in.
        Expressive: Everything you love—(Multi-)Agents, Workflow, RAG, and more.
        Agentic Coding: Let AI Agents (e.g., Cursor AI) build Agents—10x productivity boost!
        To install, pip install pocketflow or just copy the source code (only 100 lines).""",
        
        # Fictional medical device
        """NeurAlign M7 is a revolutionary non-invasive neural alignment device.
        Targeted magnetic resonance technology increases neuroplasticity in specific brain regions.
        Clinical trials showed 72% improvement in PTSD treatment outcomes.
        Developed by Cortex Medical in 2024 as an adjunct to standard cognitive therapy.
        Portable design allows for in-home use with remote practitioner monitoring.""",
        
        # Made-up historical event
        """The Velvet Revolution of Caldonia (1967-1968) ended Generalissimo Verak's 40-year rule.
        Led by poet Eliza Markovian through underground literary societies.
        Culminated in the Great Silence Protest with 300,000 silent protesters.
        First democratic elections held in March 1968 with 94% voter turnout.
        Became a model for non-violent political transitions in neighboring regions.""",
        
        # Fictional technology 
        """Q-Mesh is QuantumLeap Technologies' instantaneous data synchronization protocol.
        Utilizes directed acyclic graph consensus for 500,000 transactions per second.
        Consumes 95% less energy than traditional blockchain systems.
        Adopted by three central banks for secure financial data transfer.
        Released in February 2024 after five years of development in stealth mode.""",
        
        # Made-up scientific research
        """Harlow Institute's Mycelium Strain HI-271 removes 99.7% of PFAS from contaminated soil.
        Engineered fungi create symbiotic relationships with native soil bacteria.
        Breaks down "forever chemicals" into non-toxic compounds within 60 days.
        Field tests successfully remediated previously permanently contaminated industrial sites.
        Deployment costs 80% less than traditional chemical extraction methods."""
    ]
    
    print("=" * 50)
    print("PocketFlow RAG Document Retrieval")
    print("=" * 50)
    
    # Default query about the fictional technology
    default_query = "How to install PocketFlow?"
    
    # Get query from command line if provided with --
    query = default_query
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            query = arg[2:]
            break
    
    # Single shared store for both flows
    shared = {
        "texts": texts,
        "embeddings": None,
        "index": None,
        "query": query,
        "query_embedding": None,
        "retrieved_document": None,
        "generated_answer": None
    }
    
    # Initialize and run the offline flow (document indexing)
    offline_flow.run(shared)
    
    # Run the online flow to retrieve the most relevant document and generate an answer
    online_flow.run(shared)


if __name__ == "__main__":
    run_rag_demo()
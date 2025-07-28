#!/usr/bin/env python3
"""
Async example demonstrating PocketFlow tracing with Langfuse.

This example shows how to use the @trace_flow decorator with AsyncFlow
and AsyncNode to trace asynchronous workflows.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path to import pocketflow and tracing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tracing import trace_flow

from pocketflow import AsyncFlow, AsyncNode


class AsyncDataFetchNode(AsyncNode):
    """An async node that simulates fetching data."""

    async def prep_async(self, shared):
        """Extract the query from shared data."""
        query = shared.get("query", "default")
        return query

    async def exec_async(self, prep_res):
        """Simulate async data fetching."""
        print(f"🔍 Fetching data for query: {prep_res}")

        # Simulate async operation
        await asyncio.sleep(1)

        # Return mock data
        data = {
            "query": prep_res,
            "results": [f"Result {i} for {prep_res}" for i in range(3)],
            "timestamp": "2024-01-01T00:00:00Z",
        }
        return data

    async def post_async(self, shared, prep_res, exec_res):
        """Store the fetched data."""
        shared["fetched_data"] = exec_res
        return "process"


class AsyncDataProcessNode(AsyncNode):
    """An async node that processes the fetched data."""

    async def prep_async(self, shared):
        """Get the fetched data."""
        return shared.get("fetched_data", {})

    async def exec_async(self, prep_res):
        """Process the data asynchronously."""
        print("⚙️ Processing fetched data...")

        # Simulate async processing
        await asyncio.sleep(0.5)

        # Process the results
        processed_results = []
        for result in prep_res.get("results", []):
            processed_results.append(f"PROCESSED: {result}")

        return {
            "original_query": prep_res.get("query"),
            "processed_results": processed_results,
            "result_count": len(processed_results),
        }

    async def post_async(self, shared, prep_res, exec_res):
        """Store the processed data."""
        shared["processed_data"] = exec_res
        return "default"


@trace_flow(flow_name="AsyncDataProcessingFlow")
class AsyncDataProcessingFlow(AsyncFlow):
    """An async flow that fetches and processes data."""

    def __init__(self):
        # Create async nodes
        fetch_node = AsyncDataFetchNode()
        process_node = AsyncDataProcessNode()

        # Connect nodes
        fetch_node - "process" >> process_node

        # Initialize async flow
        super().__init__(start=fetch_node)


async def main():
    """Run the async tracing example."""
    print("🚀 Starting PocketFlow Async Tracing Example")
    print("=" * 50)

    # Create the async flow
    flow = AsyncDataProcessingFlow()

    # Prepare shared data
    shared = {"query": "machine learning tutorials"}

    print(f"📥 Input: {shared}")

    # Run the async flow (this will be automatically traced)
    try:
        result = await flow.run_async(shared)
        print(f"📤 Output: {shared}")
        print(f"🎯 Result: {result}")
        print("✅ Async flow completed successfully!")

        # Print the processed data
        if "processed_data" in shared:
            processed = shared["processed_data"]
            print(
                f"🎉 Processed {processed['result_count']} results for query: {processed['original_query']}"
            )
            for result in processed["processed_results"]:
                print(f"   - {result}")

    except Exception as e:
        print(f"❌ Async flow failed with error: {e}")
        raise

    print("\n📊 Check your Langfuse dashboard to see the async trace!")
    langfuse_host = os.getenv("LANGFUSE_HOST", "your-langfuse-host")
    print(f"   Dashboard URL: {langfuse_host}")


if __name__ == "__main__":
    asyncio.run(main())

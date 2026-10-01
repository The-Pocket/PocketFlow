import asyncio
import sys

from pocketflow import AsyncFlow, AsyncNode, AsyncParallelBatchNode

from utils import BudgetReached, call_llm


class SummarizeEach(AsyncParallelBatchNode):
    """Summarizes every document at once. All calls share the run's budget."""

    async def prep_async(self, shared):
        return [(shared, name, text) for name, text in shared["documents"].items()]

    async def exec_async(self, item):
        shared, name, text = item
        summary = await call_llm(f"Summarize in one sentence:\n\n{text}", shared["run_id"], shared["budget_usd"])
        return name, summary

    async def exec_fallback_async(self, item, exc):
        # A refused call is not retried and costs nothing.
        if isinstance(exc, BudgetReached):
            return item[1], None
        raise exc

    async def post_async(self, shared, prep_res, exec_res_list):
        shared["summaries"] = dict(exec_res_list)


class Combine(AsyncNode):
    async def prep_async(self, shared):
        return shared

    async def exec_async(self, shared):
        done = [s for s in shared["summaries"].values() if s]
        if not done:
            return "No summaries: the run's budget was used up before any call fit."
        return await call_llm("Combine into one paragraph:\n\n" + "\n".join(done), shared["run_id"], shared["budget_usd"])

    async def exec_fallback_async(self, shared, exc):
        if isinstance(exc, BudgetReached):
            return "Not combined: the run's budget was used up."
        raise exc

    async def post_async(self, shared, prep_res, exec_res):
        shared["report"] = exec_res


def create_flow():
    summarize = SummarizeEach(max_retries=1)
    summarize >> Combine(max_retries=1)
    return AsyncFlow(start=summarize)


DOCUMENTS = {
    "refunds": "Refunds are processed within 5 business days after the returned item is inspected.",
    "shipping": "Orders over $100 ship free. Express shipping is available for an extra fee.",
    "warranty": "All devices carry a two-year warranty covering manufacturing defects.",
    "support": "Support is available by chat from 8am to 8pm, Monday to Saturday.",
}


async def run(run_id: str, budget_usd: str):
    shared = {"documents": DOCUMENTS, "run_id": run_id, "budget_usd": budget_usd}
    await create_flow().run_async(shared)
    skipped = [n for n, s in shared["summaries"].items() if s is None]
    print(f"\n=== {run_id} (budget ${budget_usd}) ===")
    print(f"summarized: {len(DOCUMENTS) - len(skipped)}/{len(DOCUMENTS)}  skipped by budget: {skipped}")
    print(shared["report"])


async def main():
    budget = sys.argv[1] if len(sys.argv) > 1 else "0.05"
    await run("summary-job-1", budget)
    await run("summary-job-2", "0.0002")  # deliberately tight: only some calls fit


if __name__ == "__main__":
    asyncio.run(main())

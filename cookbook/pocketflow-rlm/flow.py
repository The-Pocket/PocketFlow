"""Flow assembly for the RLM cookbook."""

from pocketflow import Flow

from nodes import EndNode, PrepareContextNode, ReduceOrFinishNode, SummarizeChunksNode


def create_rlm_flow():
    """Create a recursive map-compress-answer flow."""

    prepare = PrepareContextNode()
    summarize = SummarizeChunksNode()
    reduce_or_finish = ReduceOrFinishNode()
    end = EndNode()

    prepare >> summarize >> reduce_or_finish
    reduce_or_finish - "recurse" >> summarize
    reduce_or_finish - "finish" >> end

    return Flow(start=prepare)

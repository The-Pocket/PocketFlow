from __future__ import annotations

import asyncio
import copy
import time
import warnings
from typing import Any, override


class BaseNode:
    def __init__(self) -> None:
        self.params: dict[str, Any] = {}
        self.successors: dict[str, "BaseNode"] = {}

    def set_params(self, params: dict[str, Any]) -> None:
        self.params = params

    def next(self, node: "BaseNode", action: str = "default") -> "BaseNode":
        if action in self.successors:
            warnings.warn(message=f"Overwriting successor for action '{action}'")
        self.successors[action] = node
        return node

    def prep(self, shared_storage: Any) -> Any:
        pass

    def exec(self, prep_result: Any) -> Any:
        pass

    def post(self, shared_storage: Any, prep_result: Any, exec_result: Any) -> Any:
        pass

    def _exec(self, prep_result: Any) -> Any:
        return self.exec(prep_result=prep_result)

    def _run(self, shared_storage: Any) -> Any:
        p = self.prep(shared_storage=shared_storage)
        e = self._exec(prep_result=p)
        return self.post(shared_storage=shared_storage, prep_result=p, exec_result=e)

    def run(self, shared_storage: Any) -> Any:
        if self.successors:
            warnings.warn(message="Node won't run successors. Use Flow.")
        return self._run(shared_storage=shared_storage)

    def __rshift__(self, other: "BaseNode") -> "BaseNode":
        return self.next(node=other)

    def __sub__(self, action: str) -> _ConditionalTransition:
        if isinstance(action, str):
            return _ConditionalTransition(src=self, action=action)
        raise TypeError("Action must be a string")


class _ConditionalTransition:
    def __init__(self, src: BaseNode, action: str) -> None:
        self.src, self.action = src, action

    def __rshift__(self, tgt: BaseNode) -> BaseNode:
        return self.src.next(node=tgt, action=self.action)


class Node(BaseNode):
    def __init__(self, max_retries: int = 1, wait: int = 0) -> None:
        super().__init__()
        self.max_retries, self.wait = max_retries, wait
        self.cur_retry: int = 0

    def exec_fallback(self, prep_result: Any, exc: Exception) -> Any:
        raise exc

    def _exec(self, prep_result: Any) -> Any:
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_result=prep_result)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_result=prep_result, exc=e)
                if self.wait > 0:
                    time.sleep(self.wait)
        return None # Should be unreachable


class BatchNode(Node):
    def _exec(self, prep_result: list[Any] | None) -> list[Any]:
        return [super(BatchNode, self)._exec(prep_result=i) for i in (prep_result or [])]


class Flow(BaseNode):
    def __init__(self, start: BaseNode | None = None) -> None:
        super().__init__()
        self.start_node = start

    def start(self, start: BaseNode) -> BaseNode:
        self.start_node = start
        return start

    def get_next_node(self, curr: BaseNode, action: str | None) -> BaseNode | None:
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors:
            warnings.warn(message=f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def _orch(self, shared_storage: Any, params: dict[str, Any] | None = None) -> str | None:
        curr, p, last_action = (
            copy.copy(self.start_node),
            (params or {**self.params}),
            None,
        )
        while curr:
            curr.set_params(params=p)
            last_action = curr._run(shared_storage=shared_storage)
            curr = copy.copy(self.get_next_node(curr=curr, action=last_action))
        return last_action

    def _run(self, shared_storage: Any) -> Any:
        p = self.prep(shared_storage=shared_storage)
        o = self._orch(shared_storage=shared_storage)
        return self.post(shared_storage=shared_storage, prep_result=p, exec_result=o)

    def post(self, shared_storage: Any, prep_result: Any, exec_result: Any) -> Any:
        return exec_result


class BatchFlow(Flow):
    def _run(self, shared_storage: Any) -> Any:
        pr = self.prep(shared_storage=shared_storage) or []
        for bp in pr:
            self._orch(shared_storage=shared_storage, params={**self.params, **bp})
        return self.post(shared_storage=shared_storage, prep_result=pr, exec_result=None)


class AsyncNode(Node):
    async def prep_async(self, shared_storage: Any) -> Any:
        pass

    async def exec_async(self, prep_result: Any) -> Any:
        pass

    async def exec_fallback_async(self, prep_result: Any, exc: Exception) -> Any:
        raise exc

    async def post_async(self, shared_storage: Any, prep_result: Any, exec_result: Any) -> Any:
        pass

    async def _exec(self, prep_result: Any) -> Any:
        for i in range(self.max_retries):
            try:
                return await self.exec_async(prep_result=prep_result)
            except Exception as e:
                if i == self.max_retries - 1:
                    return await self.exec_fallback_async(prep_result=prep_result, exc=e)
                if self.wait > 0:
                    await asyncio.sleep(delay=self.wait)
        return None # Should be unreachable

    async def run_async(self, shared_storage: Any) -> Any:
        if self.successors:
            warnings.warn(message="Node won't run successors. Use AsyncFlow.")
        return await self._run_async(shared_storage=shared_storage)

    async def _run_async(self, shared_storage: Any) -> Any:
        p = await self.prep_async(shared_storage=shared_storage)
        e = await self._exec(prep_result=p)
        return await self.post_async(shared_storage=shared_storage, prep_result=p, exec_result=e)

    def _run(self, shared_storage: Any) -> Any:
        raise RuntimeError("Use run_async.")


class AsyncBatchNode(AsyncNode, BatchNode):
    @override
    async def _exec(self, prep_result: list[Any] | None) -> list[Any]:
        return [await super(AsyncBatchNode, self)._exec(prep_result=i) for i in prep_result or []]

class AsyncParallelBatchNode(AsyncNode, BatchNode):
    @override
    async def _exec(self, prep_result: list[Any] | None) -> list[Any]:
        return await asyncio.gather(
            *(super(AsyncParallelBatchNode, self)._exec(prep_result=i) for i in prep_result or [])
        )


class AsyncFlow(Flow, AsyncNode):
    async def _orch_async(
        self, shared_storage: Any, params: dict[str, Any] | None = None
    ) -> str | None:
        curr, p, last_action = (
            copy.copy(x=self.start_node),
            (params or {**self.params}),
            None,
        )
        while curr:
            curr.set_params(params=p)
            last_action = (
                await curr._run_async(shared_storage=shared_storage)
                if isinstance(curr, AsyncNode)
                else curr._run(shared_storage=shared_storage)
            )
            curr = copy.copy(self.get_next_node(curr=curr, action=last_action))
        return last_action

    async def _run_async(self, shared_storage: Any) -> Any:
        p = await self.prep_async(shared_storage=shared_storage)
        o = await self._orch_async(shared_storage=shared_storage)
        return await self.post_async(shared_storage=shared_storage, prep_result=p, exec_result=o)

    async def post_async(self, shared_storage: Any, prep_result: Any, exec_result: Any) -> Any:
        return exec_result


class AsyncBatchFlow(AsyncFlow, BatchFlow):
    async def _run_async(self, shared_storage: Any) -> Any:
        pr = await self.prep_async(shared_storage=shared_storage) or []
        for bp in pr:
            await self._orch_async(shared_storage=shared_storage, params={**self.params, **bp})
        return await self.post_async(shared_storage=shared_storage, prep_result=pr, exec_result=None)


class AsyncParallelBatchFlow(AsyncFlow, BatchFlow):
    async def _run_async(self, shared_storage: Any) -> Any:
        pr = await self.prep_async(shared_storage=shared_storage) or []
        await asyncio.gather(
            *(self._orch_async(shared_storage=shared_storage, params={**self.params, **bp}) for bp in pr)
        )
        return await self.post_async(shared_storage=shared_storage, prep_result=pr, exec_result=None)
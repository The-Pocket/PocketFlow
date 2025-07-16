from __future__ import annotations

import asyncio
import copy
import time
import warnings
from typing import Any


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

    def prep(self, shared: Any) -> Any:
        pass

    def exec(self, prep_res: Any) -> Any:
        pass

    def post(self, shared: Any, prep_res: Any, exec_res: Any) -> Any:
        pass

    def _exec(self, prep_res: Any) -> Any:
        return self.exec(prep_res=prep_res)

    def _run(self, shared: Any) -> Any:
        p = self.prep(shared=shared)
        e = self._exec(prep_res=p)
        return self.post(shared=shared, prep_res=p, exec_res=e)

    def run(self, shared: Any) -> Any:
        if self.successors:
            warnings.warn(message="Node won't run successors. Use Flow.")
        return self._run(shared=shared)

    def __rshift__(self, other: BaseNode) -> BaseNode:
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

    def exec_fallback(self, prep_res: Any, exc: Exception) -> Any:
        raise exc

    def _exec(self, prep_res: Any) -> Any:
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res, e)
                if self.wait > 0:
                    time.sleep(self.wait)
        return None # Should be unreachable


class BatchNode(Node):
    def _exec(self, items: list[Any] | None) -> list[Any]:
        return [super(BatchNode, self)._exec(prep_res=i) for i in (items or [])]


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

    def _orch(self, shared: Any, params: dict[str, Any] | None = None) -> str | None:
        curr, p, last_action = (
            copy.copy(self.start_node),
            (params or {**self.params}),
            None,
        )
        while curr:
            curr.set_params(params=p)
            last_action = curr._run(shared=shared)
            curr = copy.copy(self.get_next_node(curr=curr, action=last_action))
        return last_action

    def _run(self, shared: Any) -> Any:
        p = self.prep(shared=shared)
        o = self._orch(shared=shared)
        return self.post(shared=shared, prep_res=p, exec_res=o)

    def post(self, shared: Any, prep_res: Any, exec_res: Any) -> Any:
        return exec_res


class BatchFlow(Flow):
    def _run(self, shared: Any) -> Any:
        pr = self.prep(shared=shared) or []
        for bp in pr:
            self._orch(shared=shared, params={**self.params, **bp})
        return self.post(shared=shared, prep_res=pr, exec_res=None)


class AsyncNode(Node):
    async def prep_async(self, shared: Any) -> Any:
        pass

    async def exec_async(self, prep_res: Any) -> Any:
        pass

    async def exec_fallback_async(self, prep_res: Any, exc: Exception) -> Any:
        raise exc

    async def post_async(self, shared: Any, prep_res: Any, exec_res: Any) -> Any:
        pass

    async def _exec(self, prep_res: Any) -> Any:
        for i in range(self.max_retries):
            try:
                return await self.exec_async(prep_res)
            except Exception as e:
                if i == self.max_retries - 1:
                    return await self.exec_fallback_async(prep_res=prep_res, exc=e)
                if self.wait > 0:
                    await asyncio.sleep(delay=self.wait)
        return None # Should be unreachable

    async def run_async(self, shared: Any) -> Any:
        if self.successors:
            warnings.warn(message="Node won't run successors. Use AsyncFlow.")
        return await self._run_async(shared=shared)

    async def _run_async(self, shared: Any) -> Any:
        p = await self.prep_async(shared=shared)
        e = await self._exec(prep_res=p)
        return await self.post_async(shared=shared, prep_res=p, exec_res=e)

    def _run(self, shared: Any) -> Any:
        raise RuntimeError("Use run_async.")


class AsyncBatchNode(AsyncNode, BatchNode):
    async def _exec(self, items: list[Any]) -> list[Any]:
        return [await super(AsyncBatchNode, self)._exec(prep_res=i) for i in items]


class AsyncParallelBatchNode(AsyncNode, BatchNode):
    async def _exec(self, items: list[Any]) -> list[Any]:
        return await asyncio.gather(
            *(super(AsyncParallelBatchNode, self)._exec(prep_res=i) for i in items)
        )


class AsyncFlow(Flow, AsyncNode):
    async def _orch_async(
        self, shared: Any, params: dict[str, Any] | None = None
    ) -> str | None:
        curr, p, last_action = (
            copy.copy(x=self.start_node),
            (params or {**self.params}),
            None,
        )
        while curr:
            curr.set_params(params=p)
            last_action = (
                await curr._run_async(shared=shared)
                if isinstance(curr, AsyncNode)
                else curr._run(shared=shared)
            )
            curr = copy.copy(self.get_next_node(curr=curr, action=last_action))
        return last_action

    async def _run_async(self, shared: Any) -> Any:
        p = await self.prep_async(shared=shared)
        o = await self._orch_async(shared=shared)
        return await self.post_async(shared=shared, prep_res=p, exec_res=o)

    async def post_async(self, shared: Any, prep_res: Any, exec_res: Any) -> Any:
        return exec_res


class AsyncBatchFlow(AsyncFlow, BatchFlow):
    async def _run_async(self, shared: Any) -> Any:
        pr = await self.prep_async(shared=shared) or []
        for bp in pr:
            await self._orch_async(shared=shared, params={**self.params, **bp})
        return await self.post_async(shared=shared, prep_res=pr, exec_res=None)


class AsyncParallelBatchFlow(AsyncFlow, BatchFlow):
    async def _run_async(self, shared: Any) -> Any:
        pr = await self.prep_async(shared=shared) or []
        await asyncio.gather(
            *(self._orch_async(shared=shared, params={**self.params, **bp}) for bp in pr)
        )
        return await self.post_async(shared=shared, prep_res=pr, exec_res=None)
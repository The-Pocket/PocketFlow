from __future__ import annotations

import asyncio
import copy
import time
import warnings
from typing import Any

type ParamValue = str | int | float | bool | None | list[Any] | dict[str, Any]


class BaseNode:
    """The base class for all nodes and flows in PocketFlow."""

    def __init__(self) -> None:
        """Initializes a `BaseNode` object."""
        self.params: dict[str, Any] = {}
        self.successors: dict[str, "BaseNode"] = {}

    def set_params(self, params: dict[str, ParamValue]) -> None:
        """Sets the parameters of the node.

        Args:
            params (dict[str, ParamValue]): The parameters to set.
        """
        self.params = params

    def next(self, node: "BaseNode", action: str = "default") -> "BaseNode":
        """Sets the next node in the flow.

        Args:
            node (BaseNode): The next node in the flow.
            action (str, optional): The action that triggers the transition to
                the next node. Defaults to "default".

        Returns:
            BaseNode: The next node in the flow.
        """
        if action in self.successors:
            warnings.warn(message=f"Overwriting successor for action '{action}'")
        self.successors[action] = node
        return node

    def prep(self, shared: dict[str, Any]) -> Any | None:
        """The pre-processing logic of the node.

        This method is called before the node is executed.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any | None: The result of the pre-processing logic.
        """
        pass

    def exec(self, prep_res: Any) -> Any | None:
        """The execution logic of the node.

        This method is called after the `prep` method.

        Args:
            prep_res (Any): The result of the `prep` method.

        Returns:
            Any | None: The result of the execution logic.
        """
        pass

    def post(
        self, shared: dict[str, Any], prep_res: Any, exec_res: Any
    ) -> Any | None:
        """The post-processing logic of the node.

        This method is called after the node is executed.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.
            prep_res (Any): The result of the `prep` method.
            exec_res (Any): The result of the `exec` method.

        Returns:
            Any | None: The result of the post-processing logic.
        """
        pass

    def _exec(self, prep_res: Any) -> Any:
        """The execution wrapper for the node.

        This method wraps the `exec` method.

        Args:
            prep_res (Any): The result of the `prep` method.

        Returns:
            Any: The result of the `exec` method.
        """
        return self.exec(prep_res=prep_res)

    def _run(self, shared: dict[str, Any]) -> Any:
        """The execution wrapper for the node.

        This method wraps the `prep`, `_exec`, and `post` methods.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post` method.
        """
        p = self.prep(shared=shared)
        e = self._exec(prep_res=p)
        return self.post(shared=shared, prep_res=p, exec_res=e)

    def run(self, shared: dict[str, Any]) -> Any:
        """Runs the node.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post` method.
        """
        if self.successors:
            warnings.warn(message="Node won't run successors. Use Flow.")
        return self._run(shared=shared)

    def __rshift__(self, other: "BaseNode") -> "BaseNode":
        """Sets the next node in the flow.

        This method is an alias for the `next` method.

        Args:
            other (BaseNode): The next node in the flow.

        Returns:
            BaseNode: The next node in the flow.
        """
        return self.next(node=other)

    def __sub__(self, action: str) -> _ConditionalTransition:
        """Creates a conditional transition.

        Args:
            action (str): The action that triggers the transition.

        Raises:
            TypeError: If the action is not a string.

        Returns:
            _ConditionalTransition: The conditional transition.
        """
        if isinstance(action, str):
            return _ConditionalTransition(src=self, action=action)
        raise TypeError("Action must be a string")


class _ConditionalTransition:
    """A conditional transition between two nodes."""

    def __init__(self, src: BaseNode, action: str) -> None:
        """Initializes a `_ConditionalTransition` object.

        Args:
            src (BaseNode): The source node.
            action (str): The action that triggers the transition.
        """
        self.src, self.action = src, action

    def __rshift__(self, tgt: BaseNode) -> BaseNode:
        """Sets the target node of the transition.

        Args:
            tgt (BaseNode): The target node.

        Returns:
            BaseNode: The source node.
        """
        return self.src.next(node=tgt, action=self.action)


class Node(BaseNode):
    """A `Node` object is an atomic, executable unit of a `Flow`.

    It is characterized by the following:
    - A single entry point and a single exit point.
    - The ability to be retried on failure.
    - A fallback mechanism for when all retries are exhausted.
    """

    def __init__(self, max_retries: int = 1, wait: int = 0) -> None:
        """Initializes a `Node` object.

        Args:
            max_retries (int, optional): The maximum number of times to retry the
                node on failure. Defaults to 1.
            wait (int, optional): The number of seconds to wait between retries.
                Defaults to 0.
        """
        super().__init__()
        self.max_retries, self.wait = max_retries, wait
        self.cur_retry: int = 0

    def exec_fallback(self, prep_res: Any, exc: Exception) -> Any:
        """The fallback mechanism for the node.

        This method is called when the node has been retried `max_retries` times
        and has failed every time.

        Args:
            prep_res (Any): The result of the `prep` method.
            exc (Exception): The exception that was raised.

        Raises:
            exc: The exception that was raised.
        """
        raise exc

    def _exec(self, prep_res: Any) -> Any:
        """The execution wrapper for the node.

        This method wraps the `exec` method with retry and fallback logic.

        Args:
            prep_res (Any): The result of the `prep` method.

        Returns:
            Any: The result of the `exec` method or the `exec_fallback` method.
        """
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res=prep_res)
            except Exception as e:
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res=prep_res, exc=e)
                if self.wait > 0:
                    time.sleep(self.wait)
        return None  # Should be unreachable


class BatchNode(Node):
    """A `BatchNode` object is a `Node` that processes a batch of items.

    It is a `Node` that takes a list of items as input and returns a list of
    results.
    """

    def _exec(self, prep_res: list[Any] | None) -> list[Any]:
        """The execution wrapper for the batch node.

        This method wraps the `_exec` method of the parent class to process a
        batch of items.

        Args:
            prep_res (list[Any] | None): The result of the `prep` method.

        Returns:
            list[Any]: The list of results.
        """
        return [
            super(BatchNode, self)._exec(prep_res=i) for i in (prep_res or [])
        ]


class Flow(BaseNode):
    """A `Flow` object orchestrates a graph of `Node` objects.

    It is a state machine that transitions between nodes based on the `action`
    returned by each node's `post` method.
    """

    def __init__(self, start: BaseNode | None = None) -> None:
        """Initializes a `Flow` object.

        Args:
            start (BaseNode | None, optional): The start node of the flow.
                Defaults to None.
        """
        super().__init__()
        self.start_node = start

    def start(self, start: BaseNode) -> BaseNode:
        """Sets the start node of the flow.

        Args:
            start (BaseNode): The start node of the flow.

        Returns:
            BaseNode: The start node of the flow.
        """
        self.start_node = start
        return start

    def get_next_node(self, curr: BaseNode, action: str | None) -> BaseNode | None:
        """Gets the next node in the flow.

        Args:
            curr (BaseNode): The current node.
            action (str | None): The action returned by the current node.

        Returns:
            BaseNode | None: The next node in the flow, or `None` if the flow
                has ended.
        """
        nxt = curr.successors.get(action or "default")
        if not nxt and curr.successors:
            warnings.warn(
                message=f"Flow ends: '{action}' not found in {list(curr.successors)}"
            )
        return nxt

    def _orch(
        self,
        shared: dict[str, Any],
        params: dict[str, ParamValue] | None = None,
    ) -> str | None:
        """The orchestration logic of the flow.

        This method executes the nodes in the flow in the order they are
        connected.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.
            params (dict[str, ParamValue] | None, optional): The parameters to
                pass to the nodes. Defaults to None.

        Returns:
            str | None: The last action returned by a node in the flow.
        """
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

    def _run(self, shared: dict[str, Any]) -> Any:
        """The execution wrapper for the flow.

        This method wraps the `_orch` method with `prep` and `post` methods.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post` method.
        """
        p = self.prep(shared=shared)
        o = self._orch(shared=shared)
        return self.post(shared=shared, prep_res=p, exec_res=o)

    def post(
        self, shared: dict[str, Any], prep_res: Any, exec_res: Any
    ) -> Any:
        """The post-processing logic of the flow.

        This method is called after the flow has finished executing.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.
            prep_res (Any): The result of the `prep` method.
            exec_res (Any): The result of the `_orch` method.

        Returns:
            Any: The result of the `_orch` method.
        """
        return exec_res


class BatchFlow(Flow):
    """A `BatchFlow` object is a `Flow` that runs in batch mode.

    It is a `Flow` that runs the same orchestration logic for a list of
    different inputs.
    """

    def _run(self, shared: dict[str, Any]) -> Any:
        """The execution wrapper for the batch flow.

        This method wraps the `_orch` method with `prep` and `post` methods.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post` method.
        """
        pr = self.prep(shared=shared) or []
        for bp in pr:
            self._orch(shared=shared, params={**self.params, **bp})
        return self.post(
            shared=shared, prep_res=pr, exec_res=None
        )


class AsyncNode(Node):
    """An `AsyncNode` object is a `Node` that runs asynchronously.

    It is a `Node` that can be used in an `AsyncFlow`.
    """

    async def prep_async(self, shared: dict[str, Any]) -> Any:
        """The async pre-processing logic of the node.

        This method is called before the node is executed.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the pre-processing logic.
        """
        pass

    async def exec_async(self, prep_res: Any) -> Any:
        """The async execution logic of the node.

        This method is called after the `prep_async` method.

        Args:
            prep_res (Any): The result of the `prep_async` method.

        Returns:
            Any: The result of the execution logic.
        """
        pass

    async def exec_fallback_async(self, prep_res: Any, exc: Exception) -> Any:
        """The async fallback mechanism for the node.

        This method is called when the node has been retried `max_retries` times
        and has failed every time.

        Args:
            prep_res (Any): The result of the `prep_async` method.
            exc (Exception): The exception that was raised.

        Raises:
            exc: The exception that was raised.
        """
        raise exc

    async def post_async(
        self, shared: dict[str, Any], prep_res: Any, exec_res: Any
    ) -> Any:
        """The async post-processing logic of the node.

        This method is called after the node is executed.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.
            prep_res (Any): The result of the `prep_async` method.
            exec_res (Any): The result of the `exec_async` method.

        Returns:
            Any: The result of the post-processing logic.
        """
        pass

    async def _exec(self, prep_res: Any) -> Any:
        """The async execution wrapper for the node.

        This method wraps the `exec_async` method with retry and fallback logic.

        Args:
            prep_res (Any): The result of the `prep_async` method.

        Returns:
            Any: The result of the `exec_async` method or the
                `exec_fallback_async` method.
        """
        for i in range(self.max_retries):
            try:
                return await self.exec_async(prep_res=prep_res)
            except Exception as e:
                if i == self.max_retries - 1:
                    return await self.exec_fallback_async(
                        prep_res=prep_res, exc=e
                    )
                if self.wait > 0:
                    await asyncio.sleep(delay=self.wait)
        return None  # Should be unreachable

    async def run_async(self, shared: dict[str, Any]) -> Any:
        """Runs the node asynchronously.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post_async` method.
        """
        if self.successors:
            warnings.warn(message="Node won't run successors. Use AsyncFlow.")
        return await self._run_async(shared=shared)

    async def _run_async(self, shared: dict[str, Any]) -> Any:
        """The async execution wrapper for the node.

        This method wraps the `prep_async`, `_exec`, and `post_async` methods.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post_async` method.
        """
        p = await self.prep_async(shared=shared)
        e = await self._exec(prep_res=p)
        return await self.post_async(
            shared=shared, prep_res=p, exec_res=e
        )

    def _run(self, shared: dict[str, Any]) -> Any:
        """Raises a `RuntimeError` because this is an async node.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Raises:
            RuntimeError: Always.
        """
        raise RuntimeError("Use run_async.")


class AsyncBatchNode(AsyncNode, BatchNode):
    """An `AsyncBatchNode` object is a `Node` that processes a batch of items
    asynchronously.

    It is a `Node` that takes a list of items as input and returns a list of
    results.
    """

    async def _exec(self, prep_res: list[Any] | None) -> list[Any]:  # type: ignore[override]
        """The async execution wrapper for the batch node.

        This method wraps the `_exec` method of the parent class to process a
        batch of items.

        Args:
            prep_res (list[Any] | None): The result of the `prep` method.

        Returns:
            list[Any]: The list of results.
        """
        return [
            await super(AsyncBatchNode, self)._exec(prep_res=i)
            for i in prep_res or []
        ]


class AsyncParallelBatchNode(AsyncNode, BatchNode):
    """An `AsyncParallelBatchNode` object is a `Node` that processes a batch of
    items asynchronously and in parallel.

    It is a `Node` that takes a list of items as input and returns a list of
    results.
    """

    async def _exec(self, prep_res: list[Any] | None) -> list[Any]:  # type: ignore[override]
        """The async execution wrapper for the parallel batch node.

        This method wraps the `_exec` method of the parent class to process a
        batch of items in parallel.

        Args:
            prep_res (list[Any] | None): The result of the `prep` method.

        Returns:
            list[Any]: The list of results.
        """
        return await asyncio.gather(
            *(
                super(AsyncParallelBatchNode, self)._exec(prep_res=i)
                for i in prep_res or []
            )
        )


# CoroutuneType[Any, Any, list[Any] | None]


class AsyncFlow(Flow, AsyncNode):
    """An `AsyncFlow` object is a `Flow` that runs asynchronously.

    It is a `Flow` that can contain both `Node` and `AsyncNode` objects.
    """

    async def _orch_async(
        self, shared: dict[str, Any], params: dict[str, Any] | None = None
    ) -> str | None:
        """The async orchestration logic of the flow.

        This method executes the nodes in the flow in the order they are
        connected.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.
            params (dict[str, Any] | None, optional): The parameters to pass to
                the nodes. Defaults to None.

        Returns:
            str | None: The last action returned by a node in the flow.
        """
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

    async def _run_async(self, shared: dict[str, Any]) -> Any:
        """The async execution wrapper for the flow.

        This method wraps the `_orch_async` method with `prep_async` and
        `post_async` methods.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post_async` method.
        """
        p = await self.prep_async(shared=shared)
        o = await self._orch_async(shared=shared)
        return await self.post_async(
            shared=shared, prep_res=p, exec_res=o
        )

    async def post_async(
        self, shared: dict[str, Any], prep_res: Any, exec_res: Any
    ) -> Any:
        """The async post-processing logic of the flow.

        This method is called after the flow has finished executing.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.
            prep_res (Any): The result of the `prep_async` method.
            exec_res (Any): The result of the `_orch_async` method.

        Returns:
            Any: The result of the `_orch_async` method.
        """
        return exec_res


class AsyncBatchFlow(AsyncFlow, BatchFlow):
    """An `AsyncBatchFlow` object is a `Flow` that runs in batch mode
    asynchronously.

    It is a `Flow` that runs the same orchestration logic for a list of
    different inputs.
    """


async def _run_async(self, shared: dict[str, Any]) -> Any:
    """The async execution wrapper for the batch flow.

    This method wraps the `_orch_async` method with `prep_async` and
    `post_async` methods.

    Args:
        shared (dict[str, Any]): The shared storage of the flow.

    Returns:
        Any: The result of the `post_async` method.
    """
    pr = await self.prep_async(shared=shared) or []
    for bp in pr:
        await self._orch_async(
            shared=shared, params={**self.params, **bp}
        )
    return await self.post_async(
        shared=shared, prep_res=pr, exec_res=None
    )


class AsyncParallelBatchFlow(AsyncFlow, BatchFlow):
    """An `AsyncParallelBatchFlow` object is a `Flow` that runs in batch mode
    asynchronously and in parallel.

    It is a `Flow` that runs the same orchestration logic for a list of
    different inputs.
    """

    async def _run_async(self, shared: dict[str, Any]) -> Any:
        """The async execution wrapper for the parallel batch flow.

        This method wraps the `_orch_async` method with `prep_async` and
        `post_async` methods.

        Args:
            shared (dict[str, Any]): The shared storage of the flow.

        Returns:
            Any: The result of the `post_async` method.
        """
        pr = await self.prep_async(shared=shared) or []
        await asyncio.gather(
            *(
                self._orch_async(
                    shared=shared, params={**self.params, **bp}
                )
                for bp in pr
            )
        )
        return await self.post_async(
            shared=shared, prep_res=pr, exec_res=None
        )

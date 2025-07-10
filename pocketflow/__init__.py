import asyncio, warnings, copy, time

class BaseNode:
    def __init__(self, node_id=None): self.params,self.successors,self.node_id={},{},node_id
    def set_params(self,params): self.params=params
    def next(self,node,action="default"):
        if action in self.successors: warnings.warn(f"Overwriting successor for action '{action}'")
        self.successors[action]=node; return node
    def prep(self,shared): pass
    def exec(self,prep_res): pass
    def post(self,shared,prep_res,exec_res): pass
    def _exec(self,prep_res): return self.exec(prep_res)
    def _run(self,shared): p=self.prep(shared); e=self._exec(p); return self.post(shared,p,e)
    def run(self,shared): 
        if self.successors: warnings.warn("Node won't run successors. Use Flow.")  
        return self._run(shared)
    def __rshift__(self,other): return self.next(other)
    def __sub__(self,action):
        if isinstance(action,str): return _ConditionalTransition(self,action)
        raise TypeError("Action must be a string")

class _ConditionalTransition:
    def __init__(self,src,action): self.src,self.action=src,action
    def __rshift__(self,tgt): return self.src.next(tgt,self.action)

class Node(BaseNode):
    def __init__(self,max_retries=1,wait=0,node_id=None): super().__init__(node_id=node_id); self.max_retries,self.wait=max_retries,wait
    def exec_fallback(self,prep_res,exc): raise exc
    def _exec(self,prep_res):
        for self.cur_retry in range(self.max_retries):
            try: return self.exec(prep_res)
            except Exception as e:
                if self.cur_retry==self.max_retries-1: return self.exec_fallback(prep_res,e)
                if self.wait>0: time.sleep(self.wait)

class BatchNode(Node):
    def _exec(self,items): return [super(BatchNode,self)._exec(i) for i in (items or [])]

class Flow(BaseNode):
    def __init__(self,start=None, node_id=None): super().__init__(node_id=node_id); self.start_node=start; self.nodes={}

    def start(self,start): self.start_node=start; return start

    def _discover_nodes(self):
        q, visited = ([self.start_node] if self.start_node else []), set()
        while q:
            curr = q.pop(0)
            if curr in visited: continue
            visited.add(curr)
            if getattr(curr, 'node_id', None):
                if curr.node_id in self.nodes: warnings.warn(f"Duplicate node_id '{curr.node_id}' found.")
                self.nodes[curr.node_id] = curr
            if isinstance(curr, Flow) and curr.start_node: q.append(curr.start_node)
            q.extend([succ for succ in curr.successors.values() if succ])
        return self

    def get_next_node(self,curr,action):
        nxt=curr.successors.get(action or "default")
        if not nxt and curr.successors: warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt

    def _orch(self,shared,params=None, resume_info=None):
        curr, p, last_action = None, (params or {**self.params}), None
        if resume_info:
            if not self.nodes: self._discover_nodes()
            resume_node = self.nodes.get(resume_info.get("node_id"))
            if not resume_node: raise ValueError(f"Resume node_id '{resume_info.get('node_id')}' not found.")
            curr = self.get_next_node(resume_node, resume_info.get("last_action"))
        else:
            curr=copy.copy(self.start_node)

        while curr: curr.set_params(p); last_action=curr._run(shared); curr=copy.copy(self.get_next_node(curr,last_action))
        return last_action

    def _run(self,shared): p=self.prep(shared); o=self._orch(shared, resume_info=getattr(self,'_resume_info',None)); return self.post(shared,p,o)

    def resume(self, shared, resume_info):
        self._resume_info = resume_info
        try: return self._run(shared)
        finally: del self._resume_info

    def post(self,shared,prep_res,exec_res): return exec_res

class BatchFlow(Flow):
    def _run(self,shared):
        pr=self.prep(shared) or []
        for bp in pr: self._orch(shared,{**self.params,**bp})
        return self.post(shared,pr,None)

class AsyncNode(Node):
    async def prep_async(self,shared): pass
    async def exec_async(self,prep_res): pass
    async def exec_fallback_async(self,prep_res,exc): raise exc
    async def post_async(self,shared,prep_res,exec_res): pass
    async def _exec(self,prep_res): 
        for i in range(self.max_retries):
            try: return await self.exec_async(prep_res)
            except Exception as e:
                if i==self.max_retries-1: return await self.exec_fallback_async(prep_res,e)
                if self.wait>0: await asyncio.sleep(self.wait)
    async def run_async(self,shared): 
        if self.successors: warnings.warn("Node won't run successors. Use AsyncFlow.")  
        return await self._run_async(shared)
    async def _run_async(self,shared): p=await self.prep_async(shared); e=await self._exec(p); return await self.post_async(shared,p,e)
    def _run(self,shared): raise RuntimeError("Use run_async.")

class AsyncBatchNode(AsyncNode,BatchNode):
    async def _exec(self,items): return [await super(AsyncBatchNode,self)._exec(i) for i in items]

class AsyncParallelBatchNode(AsyncNode,BatchNode):
    async def _exec(self,items): return await asyncio.gather(*(super(AsyncParallelBatchNode,self)._exec(i) for i in items))

class AsyncFlow(Flow,AsyncNode):
    async def _orch_async(self,shared,params=None, resume_info=None):
        curr,p,last_action = None,(params or {**self.params}),None
        if resume_info:
            if not self.nodes: self._discover_nodes()
            resume_node = self.nodes.get(resume_info.get("node_id"))
            if not resume_node: raise ValueError(f"Resume node_id '{resume_info.get('node_id')}' not found.")
            curr = self.get_next_node(resume_node, resume_info.get("last_action"))
        else:
            curr = copy.copy(self.start_node)

        while curr: curr.set_params(p); last_action=await curr._run_async(shared) if isinstance(curr,AsyncNode) else curr._run(shared); curr=copy.copy(self.get_next_node(curr,last_action))
        return last_action
        
    async def _run_async(self,shared): p=await self.prep_async(shared); o=await self._orch_async(shared, resume_info=getattr(self,'_resume_info',None)); return await self.post_async(shared,p,o)

    async def resume_async(self, shared, resume_info):
        self._resume_info = resume_info
        try: return await self._run_async(shared)
        finally: del self._resume_info

    async def post_async(self,shared,prep_res,exec_res): return exec_res

class AsyncBatchFlow(AsyncFlow,BatchFlow):
    async def _run_async(self,shared):
        pr=await self.prep_async(shared) or []
        for bp in pr: await self._orch_async(shared,{**self.params,**bp})
        return await self.post_async(shared,pr,None)

class AsyncParallelBatchFlow(AsyncFlow,BatchFlow):
    async def _run_async(self,shared): 
        pr=await self.prep_async(shared) or []
        await asyncio.gather(*(self._orch_async(shared,{**self.params,**bp}) for bp in pr))
        return await self.post_async(shared,pr,None)
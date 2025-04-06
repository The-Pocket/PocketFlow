import time
import threading
from pocketflow import Node, Flow
from utils import fake_stream_llm, stream_llm

class StreamNode(Node):
    def prep(self, shared):
        # Create interrupt event
        interrupt_event = threading.Event()

        # Start a thread to listen for user interrupt
        def wait_for_interrupt():
            input("Press ENTER at any time to interrupt streaming...\n")
            interrupt_event.set()
        listener_thread = threading.Thread(target=wait_for_interrupt)
        listener_thread.start()
        
        # Get prompt from shared store
        prompt = shared["prompt"]
        # Get chunks from LLM function
        chunks = fake_stream_llm(prompt)
        return chunks, interrupt_event, listener_thread

    def exec(self, prep_res):
        chunks, interrupt_event, listener_thread = prep_res
        for chunk in chunks:
            if interrupt_event.is_set():
                print("User interrupted streaming.")
                break
            
            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                print(chunk_content, end="", flush=True)
                time.sleep(0.1)  # simulate latency
        return interrupt_event, listener_thread

    def post(self, shared, prep_res, exec_res):
        interrupt_event, listener_thread = exec_res
        # Join the interrupt listener so it doesn't linger
        interrupt_event.set()
        listener_thread.join()
        return "default"

# Usage:
node = StreamNode()
flow = Flow(start=node)

shared = {"prompt": "What's the meaning of life?"}
flow.run(shared)

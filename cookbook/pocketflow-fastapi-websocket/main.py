import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from flow import create_streaming_chat_flow

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_chat_interface():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Initialize conversation history for this connection
    shared_storage = {
        "websocket": websocket,
        "conversation_history": []
    }
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Update only the current message, keep conversation history
            shared_storage["user_message"] = message.get("content", "")
            
            flow = create_streaming_chat_flow()
            await flow.run_async(shared_storage)
            
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
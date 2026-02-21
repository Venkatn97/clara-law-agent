import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from dotenv import load_dotenv
from agent.agent import chat
from agent.memory import create_initial_state

load_dotenv()

app = FastAPI()

sessions = {}

@app.get("/")
def health_check():
    return {"status": "Clara is running"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()

    if "messages" in body:
        messages = body.get("messages", [])
        user_messages = [m for m in messages if m.get("role") == "user"]
        message = user_messages[-1].get("content", "") if user_messages else ""
        session_id = body.get("call", {}).get("id", "default")
    else:
        session_id = body.get("session_id", "default")
        message = body.get("message", "")

    if session_id not in sessions:
        sessions[session_id] = create_initial_state(session_id=session_id)

    state = sessions[session_id]
    response, updated_state = chat(message, state)
    sessions[session_id] = updated_state

    return JSONResponse({
        "id": "chatcmpl-clara",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response
            },
            "finish_reason": "stop"
        }]
    })

@app.post("/vapi")
async def vapi_endpoint(request: Request):
    body = await request.json()

    message_type = body.get("message", {}).get("type", "")

    if message_type == "assistant-request":
        return JSONResponse({
            "assistant": {
                "firstMessage": "Thank you for calling Morrison and Associates. This is Clara speaking. How can I help you today?",
                "model": {
                    "provider": "custom-llm",
                    "url": f"{os.getenv('NGROK_URL', '')}/chat"
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
                }
            }
        })

    if message_type == "end-of-call-report":
        print(f"Call ended. Summary: {body.get('message', {}).get('summary', '')}")

    return JSONResponse({"status": "ok"})

@app.post("/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()

    messages = body.get("messages", [])
    user_messages = [m for m in messages if m.get("role") == "user"]
    message = user_messages[-1].get("content", "") if user_messages else ""
    session_id = body.get("call", {}).get("id", "default")

    if session_id not in sessions:
        sessions[session_id] = create_initial_state(session_id=session_id)

    state = sessions[session_id]
    response, updated_state = chat(message, state)
    sessions[session_id] = updated_state

    async def generate():
        words = response.split(" ")
        for i, word in enumerate(words):
            chunk = {
                "id": "chatcmpl-clara",
                "object": "chat.completion.chunk",
                "choices": [{
                    "index": 0,
                    "delta": {
                        "content": word + (" " if i < len(words) - 1 else "")
                    },
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0)

        final = {
            "id": "chatcmpl-clara",
            "object": "chat.completion.chunk",
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(final)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
import os
import ngrok
import uvicorn
import threading
from dotenv import load_dotenv

load_dotenv()

def start_server():
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    listener = ngrok.forward(8000, authtoken=os.getenv("NGROK_AUTH_TOKEN"))
    ngrok_url = listener.url()
    
    print(f"\n Clara API is live at: {ngrok_url}")
    print(f" Health check: {ngrok_url}/")
    print(f" Chat endpoint: {ngrok_url}/chat")
    print(f" Vapi endpoint: {ngrok_url}/vapi")
    print(f"\n Add this to your .env:")
    print(f" NGROK_URL={ngrok_url}\n")
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    input("Press Enter to stop the server...\n")
    
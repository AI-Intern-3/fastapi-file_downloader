from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import requests
from dotenv import load_dotenv

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Load environment variables from .env file
load_dotenv()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/configure", response_class=HTMLResponse)
async def configure(
    request: Request,
    account_id: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...)
):
    try:
        # Save credentials in environment variables
        with open(".env", "w") as env_file:
            env_file.write(f"ACCOUNT_ID={account_id}\n")
            env_file.write(f"CLIENT_ID={client_id}\n")
            env_file.write(f"CLIENT_SECRET={client_secret}\n")
        
        # Load them back to ensure they are stored
        load_dotenv()

        # Fetch recordings after configuration
        recordings = fetch_recordings()

        return templates.TemplateResponse("success.html", {"request": request, "recordings": recordings})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def fetch_recordings():
    url = f"https://api.zoom.us/v2/accounts/{os.getenv('ACCOUNT_ID')}/recordings"
    headers = {
        "Authorization": f"Bearer {generate_zoom_jwt()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json().get('meetings', [])

def generate_zoom_jwt():
    # Replace with your logic to generate a JWT token using client_id and client_secret
    return "your_jwt_token"

@app.get("/download/{recording_id}")
async def download_recording(recording_id: str):
    # Implement the logic to download a specific recording by its ID
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

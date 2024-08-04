from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="app/templates/")

# Zoom API Credentials (Replace with yours)
ZOOM_API_KEY = "YOUR_ZOOM_API_KEY"
ZOOM_API_SECRET = "YOUR_ZOOM_API_SECRET"
ZOOM_API_BASE_URL = "https://api.zoom.us/v2"

# Function to get an access token using JWT (replace with your implementation)
def get_access_token():
    # Implement logic to obtain an access token using JWT
    # Refer to Zoom API documentation for details on creating a JWT app:
    # https://marketplace.zoom.us/docs/guides/jwt/tutorial
    # This function should return a valid access token as a string
    pass


# Function to download a file
def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return filename


# Function to retrieve a list of recordings for a meeting
def get_recordings(meeting_id, access_token):
    url = f"{ZOOM_API_BASE_URL}/meetings/{meeting_id}/recordings"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        recordings = data.get("recordings", [])
        return recordings
    else:
        raise Exception(f"Error fetching recordings: {response.text}")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download_file(link: str = Form(...)):
    try:
        # Logic for handling non-Zoom download links can be added here
        if not link.startswith("https://zoom.us/rec"):
            raise Exception("Currently only Zoom recording download links are supported")
        # ... (extract meeting ID from link)

        # Retrieve access token (replace with your get_access_token function)
        access_token = get_access_token()

        # Fetch recordings using meeting ID and access token
        recordings = get_recordings(meeting_id, access_token)

        # Find the recording matching the link (if provided)
        download_url = None
        for recording in recordings:
            if recording["recording_file"] == link.split("/")[-1]:
                download_url = recording["download_url"]
                break

        if download_url:
            filename = download_url.split("/")[-1]
            return FileResponse(download_file(download_url, filename), media_type='video/mp4', filename=filename)
        else:
            raise Exception("Recording not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/save_config")
async def save_config(api_key: str = Form(...), api_secret: str = Form(...)):
    global ZOOM_API_KEY, ZOOM_API_SECRET
    ZOOM_API_KEY = api_key
    ZOOM_API_SECRET = api_secret
    # Implement logic to store configuration securely (e.g., database)
    return {"message": "Configuration saved successfully"}


@app.get("/recordings")
async def get_recordings(request: Request):
    # Retrieve access token (replace with your get_access_token function)
    access_token = get_access_token()

    # Fetch all recordings (change based on your needs)
    recordings = get_recordings("YOUR_MEETING_ID", access_token)  # Replace with actual meeting ID

    # Render template with recordings data (adjust template as needed)
    return templates.TemplateResponse("recordings.html", {"data": recordings})


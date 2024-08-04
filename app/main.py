import requests
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.get_template("index.html").render({"request": request})

@app.post("/download")
async def download_file(link: str = Form(...)):
    try:
        response = requests.get(link, stream=True)
        response.raise_for_status()

        filename = link.split('/')[-1]  # Extract filename from URL
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return FileResponse(filename, media_type='application/octet-stream', filename=filename)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

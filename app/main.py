from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import aiohttp
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download/")
async def download_file(request: Request, link: str = Form(...)):
    filename = link.split("/")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            content = await response.read()
            with open(filename, "wb") as file:
                file.write(content)
    
    return FileResponse(path=filename, filename=filename, media_type='application/octet-stream')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

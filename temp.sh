#!/bin/bash

# Create the project directory
mkdir fastapi-file-downloader
cd fastapi-file-downloader

# Create app directory and subdirectories
mkdir -p app/templates
mkdir app/static

# Create the main FastAPI application file
cat <<EOL > app/main.py
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
EOL

# Create the HTML template
cat <<EOL > app/templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Downloader</title>
</head>
<body>
    <h1>File Downloader</h1>
    <form action="/download/" method="post">
        <label for="link">Enter the file link:</label><br><br>
        <input type="text" id="link" name="link" style="width: 300px;"><br><br>
        <input type="submit" value="Download">
    </form>
</body>
</html>
EOL

# Create the Dockerfile
cat <<EOL > Dockerfile
# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

# Create requirements.txt
cat <<EOL > requirements.txt
fastapi
uvicorn
aiohttp
jinja2
EOL

# Create a .gitignore file
cat <<EOL > .gitignore
__pycache__/
*.pyc
.env
*.sqlite3
*.db
EOL

# Create an empty README.md
touch README.md

# Done
echo "Project structure created successfully!"

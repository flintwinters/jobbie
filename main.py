from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "data.csv"

@app.get("/api/csv")
async def get_csv():
    if not os.path.exists(CSV_FILE):
        return Response(status_code=404, content="CSV file not found.")
    with open(CSV_FILE, "r") as f:
        content = f.read()
    return Response(content=content, media_type="text/csv")

@app.post("/api/csv")
async def save_csv(request: Request):
    data = await request.body()
    with open(CSV_FILE, "wb") as f:
        f.write(data)
    return {"message": "CSV file saved successfully."}

@app.get("/api/link-preview")
async def link_preview(url: str):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('title').text if soup.find('title') else ''
        
        favicon_url = ''
        favicon_link = soup.find("link", rel="shortcut icon")
        if not favicon_link:
            favicon_link = soup.find("link", rel="icon")

        if favicon_link:
            favicon_url = favicon_link.get('href', '')
            if not urllib.parse.urlparse(favicon_url).scheme:
                favicon_url = urllib.parse.urljoin(url, favicon_url)
        
        if not favicon_url:
            # Check for default favicon.ico
            default_favicon_url = urllib.parse.urljoin(url, '/favicon.ico')
            try:
                # Use stream=True to avoid downloading the whole file if it's large
                # and just check headers
                fav_res = requests.head(default_favicon_url, timeout=2)
                if fav_res.status_code == 200 and 'image' in fav_res.headers.get('Content-Type', ''):
                     favicon_url = default_favicon_url
            except requests.RequestException:
                pass # Ignore if /favicon.ico doesn't exist

        proxied_favicon_url = f"/api/favicon?url={urllib.parse.quote(favicon_url)}" if favicon_url else ""
        return JSONResponse({"title": title, "favicon": proxied_favicon_url})
    except requests.RequestException:
        return JSONResponse({"title": "", "favicon": ""}, status_code=400)

@app.get("/api/favicon")
async def favicon_proxy(url: str):
    try:
        response = requests.get(url, timeout=5, stream=True)
        response.raise_for_status()
        
        # Check content type if possible, default to common image types
        content_type = response.headers.get('Content-Type', 'image/x-icon')
        
        return Response(content=response.content, media_type=content_type)
    except requests.RequestException:
        return Response(status_code=404)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
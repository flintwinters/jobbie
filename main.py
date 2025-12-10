from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import requests
from bs4 import BeautifulSoup
import urllib.parse
import favicon

app = FastAPI()

PORT = 28889

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "data.csv"

@app.get("/")
async def serve_index():
    return FileResponse('index.html')

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
        # Use a standard user-agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, timeout=5, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title').text if soup.find('title') else ''
        
        favicon_url = ''
        icons = favicon.get(url)
        if icons:
            # Choose the first icon found
            favicon_url = icons[0].url

        proxied_favicon_url = f"/api/favicon?url={urllib.parse.quote(favicon_url)}" if favicon_url else ""
        return JSONResponse({"title": title, "favicon": proxied_favicon_url})
    except Exception as e:
        print(f"Error getting link preview for {url}: {e}")
        return JSONResponse({"title": "", "favicon": ""}, status_code=400)

@app.get("/api/favicon")
async def favicon_proxy(url: str):
    print(f"Proxying favicon from: {url}")
    try:
        response = requests.get(url, timeout=5, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', 'image/x-icon')
        print(f"Favicon content type: {content_type}")
        
        return Response(content=response.content, media_type=content_type)
    except requests.RequestException as e:
        print(f"Error fetching favicon: {e}")
        return Response(status_code=404)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)

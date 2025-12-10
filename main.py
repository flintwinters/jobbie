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
        icon_links = soup.find_all("link", rel=lambda rel: rel and 'icon' in rel)
        
        if icon_links:
            # Prioritize certain icon types
            for rel_type in ["apple-touch-icon", "shortcut icon", "icon"]:
                for link in icon_links:
                    if rel_type in link.get('rel', []):
                        favicon_url = link.get('href', '')
                        if not urllib.parse.urlparse(favicon_url).scheme:
                            favicon_url = urllib.parse.urljoin(url, favicon_url)
                        break
                if favicon_url:
                    break
        
        if not favicon_url:
            # Check for default favicon.ico
            default_favicon_url = urllib.parse.urljoin(url, '/favicon.ico')
            try:
                fav_res = requests.head(default_favicon_url, timeout=2)
                if fav_res.status_code == 200 and 'image' in fav_res.headers.get('Content-Type', ''):
                     favicon_url = default_favicon_url
            except requests.RequestException:
                pass

        proxied_favicon_url = f"/api/favicon?url={urllib.parse.quote(favicon_url)}" if favicon_url else ""
        return JSONResponse({"title": title, "favicon": proxied_favicon_url})
    except requests.RequestException:
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
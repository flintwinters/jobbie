from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
import os
import uvicorn

app = FastAPI()

CSV_FILE = "data.csv"

@app.get("/api/csv")
async def get_csv():
    if not os.path.exists(CSV_FILE):
        return Response(status_code=404, content="CSV file not found.")
    return FileResponse(CSV_FILE, media_type="text/csv")

@app.post("/api/csv")
async def save_csv(request: Request):
    data = await request.body()
    with open(CSV_FILE, "wb") as f:
        f.write(data)
    return {"message": "CSV file saved successfully."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

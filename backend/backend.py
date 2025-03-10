from fastapi import FastAPI, UploadFile, File, HTTPException, Form 
from pydantic import BaseModel
from typing import List
from pathlib import Path
import uvicorn
import shutil
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List
import shutil
from datetime import datetime 
from data_analysis_agent import DataAnalysisAgent
from data_schema_agent import DataSchemaAgent

from image_analysis import analyze_image

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define folder to store uploaded images
UPLOAD_FOLDER = Path("uploaded_images")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Serve static files (uploaded images)
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

analysis_agent = DataAnalysisAgent()
schema_agent = DataSchemaAgent()

@app.post("/upload-folder/")
def upload_folder(folder_name: str = Form(...), folder: List[UploadFile] = File(...)):
    """
    Uploads a folder of images and stores them in a public directory.
    """
    try:
        folder_path = UPLOAD_FOLDER
        print(folder)
        for file in folder:
            file_path = folder_path / file.filename
            print("file_path:", file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # real_format = imghdr.what(file_path)
            # print(f"Detected format: {real_format}")

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        # run data analysis agent 
        timestamp = datetime.now()
        analysis_agent.run_agent(folder_path, folder, datetime.now())
        schema_agent.run_agent()
        time_after = datetime.now()
        print("Time taken to run agent: ", time_after - timestamp)
        return {
            "message": "Folder uploaded successfully",
            "folder_url": f"http://localhost:8000/uploads/{folder_name}"
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading folder: {str(e)}")

@app.get("/list-images/")
def list_images(folder_name: str):
    """
    Returns a list of image URLs from the uploaded folder.
    """
    folder_path = UPLOAD_FOLDER / folder_name
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="Invalid folder name")

    image_urls = [
        f"http://localhost:8000/uploads/{folder_name}/{file.name}"
        for file in folder_path.iterdir() if file.is_file()
    ]

    return {"images": image_urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

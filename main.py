from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import Response
from typing import List
import uuid
from datetime import datetime, timezone
from config import supabase
from models import AudioFile, AudioFileCreate
from storage import (
    upload_audio_file,
    list_audio_files,
    get_audio_file,
    download_audio_file,
    delete_audio_file,
    AUDIO_BUCKET
)
import os

app = FastAPI(
    title="Supabase Audio File Storage API",
    description="A simple API for CRUD operations on audio files using Supabase Storage",
    version="1.0.0"
)

# Allowed audio file types
ALLOWED_CONTENT_TYPES = [
    "audio/mpeg",     # MP3
    "audio/wav",      # WAV
    "audio/x-wav",    # WAV (alternative)
    "audio/flac",     # FLAC
    "audio/aac",      # AAC
    "audio/ogg",      # OGG
    "audio/mp4",      # M4A
]

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "OK", "message": "Supabase Audio File Storage API is running"}

# Upload an audio file
@app.post("/upload", response_model=AudioFile)
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    
    # Check if filename exists
    if file.filename is None:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Upload to Supabase Storage
        upload_result = upload_audio_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        # Create metadata record in database
        metadata = {
            "id": upload_result["id"],
            "filename": upload_result["filename"],
            "content_type": upload_result["content_type"],
            "size": len(file_content),
            "upload_timestamp": datetime.now(timezone.utc).isoformat(),
            "storage_path": upload_result["storage_path"]
        }
        
        # Insert metadata into Supabase database
        result = supabase.table("audio_files").insert(metadata).execute()
        
        # Return the created file metadata
        return AudioFile(**metadata)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

# List all audio files
@app.get("/files", response_model=List[AudioFile])
async def list_files():
    try:
        # Get files from Supabase database
        response = supabase.table("audio_files").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

# Get a specific audio file info
@app.get("/files/{file_id}", response_model=AudioFile)
async def get_file(file_id: str):
    try:
        # Get file from Supabase database
        response = supabase.table("audio_files").select("*").eq("id", file_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="File not found")
        
        return AudioFile(**response.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file: {str(e)}")

# Download an audio file
@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    try:
        # Get file info from database
        response = supabase.table("audio_files").select("storage_path, filename, content_type").eq("id", file_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_info = response.data[0]
        storage_path = file_info["storage_path"]
        
        # Download file from Supabase Storage
        file_content = download_audio_file(storage_path)
        
        # Return file as response
        return Response(
            content=file_content,
            media_type=file_info["content_type"],
            headers={
                "Content-Disposition": f'attachment; filename="{file_info["filename"]}"'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

# Delete an audio file
@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    try:
        # Get file info from database
        response = supabase.table("audio_files").select("storage_path").eq("id", file_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="File not found")
        
        storage_path = response.data[0]["storage_path"]
        
        # Delete file from Supabase Storage
        delete_audio_file(storage_path)
        
        # Delete metadata from Supabase database
        supabase.table("audio_files").delete().eq("id", file_id).execute()
        
        return {"message": "File deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

# Create the audio_files table if it doesn't exist
def create_audio_files_table():
    try:
        # Try to select from the table to see if it exists
        supabase.table("audio_files").select("*").limit(1).execute()
        print("Audio files table exists")
    except Exception as e:
        # Table doesn't exist, inform user to create it manually
        print(f"Audio files table not found: {e}")
        print("Please create the table manually in your Supabase dashboard with the following structure:")
        print("""
        Table: audio_files
        Columns:
        - id (TEXT) - Primary Key
        - filename (TEXT)
        - content_type (TEXT)
        - size (INTEGER)
        - upload_timestamp (TIMESTAMP)
        - storage_path (TEXT)
        """)
        
# Initialize the table when the app starts
create_audio_files_table()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

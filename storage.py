import os
from typing import List, Optional
try:
    from supabase import Client
except ImportError:
    Client = None
from config import supabase, AUDIO_BUCKET
from models import AudioFile
import uuid
from datetime import datetime

# Ensure the audio files bucket exists
def create_audio_bucket():
    try:
        # Check if bucket already exists
        buckets = supabase.storage.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]
        
        if AUDIO_BUCKET not in bucket_names:
            # Try to create the bucket
            try:
                supabase.storage.create_bucket(AUDIO_BUCKET)
                print(f"Created bucket: {AUDIO_BUCKET}")
            except Exception as create_error:
                print(f"Error creating bucket: {create_error}")
                print("Please create the bucket manually in your Supabase dashboard:")
                print(f"1. Go to your Supabase project dashboard")
                print(f"2. Navigate to Storage")
                print(f"3. Click 'New bucket'")
                print(f"4. Name it '{AUDIO_BUCKET}'")
                print(f"5. Set it as public if you want public access to files")
        else:
            print(f"Bucket {AUDIO_BUCKET} already exists")
    except Exception as e:
        print(f"Error checking buckets: {e}")
        print("Please ensure your bucket exists in your Supabase dashboard:")
        print(f"Bucket name: {AUDIO_BUCKET}")

# Upload an audio file to Supabase Storage
def upload_audio_file(file_content: bytes, filename: str, content_type: str) -> dict:
    try:
        # Generate a unique file ID
        file_id = str(uuid.uuid4())
        
        # Create the storage path
        storage_path = f"{file_id}_{filename}"
        
        # Upload the file to Supabase Storage
        response = supabase.storage.from_(AUDIO_BUCKET).upload(
            path=storage_path,
            file=file_content,
            file_options={"content-type": content_type}
        )
        
        return {
            "id": file_id,
            "storage_path": storage_path,
            "filename": filename,
            "content_type": content_type
        }
    except Exception as e:
        raise Exception(f"Error uploading file: {str(e)}")

# Get list of all audio files
def list_audio_files() -> List[dict]:
    try:
        # List all files in the bucket
        response = supabase.storage.from_(AUDIO_BUCKET).list()
        return response
    except Exception as e:
        raise Exception(f"Error listing files: {str(e)}")

# Get a specific audio file
def get_audio_file(file_path: str) -> dict:
    try:
        # Get file info
        response = supabase.storage.from_(AUDIO_BUCKET).get_public_url(file_path)
        return {"public_url": response}
    except Exception as e:
        raise Exception(f"Error getting file: {str(e)}")

# Download an audio file
def download_audio_file(file_path: str) -> bytes:
    try:
        # Download the file
        response = supabase.storage.from_(AUDIO_BUCKET).download(file_path)
        return response
    except Exception as e:
        raise Exception(f"Error downloading file: {str(e)}")

# Delete an audio file
def delete_audio_file(file_path: str) -> bool:
    try:
        # Delete the file from storage
        supabase.storage.from_(AUDIO_BUCKET).remove([file_path])
        return True
    except Exception as e:
        raise Exception(f"Error deleting file: {str(e)}")

# Initialize the bucket when this module is imported
create_audio_bucket()

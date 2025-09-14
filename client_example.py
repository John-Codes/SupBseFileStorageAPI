import requests
import os
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8001"

def upload_audio_file(file_path):
    """Upload an audio file to the API"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        return response.json()

def list_audio_files():
    """List all uploaded audio files"""
    response = requests.get(f"{API_BASE_URL}/files")
    return response.json()

def get_file_info(file_id):
    """Get information about a specific file"""
    response = requests.get(f"{API_BASE_URL}/files/{file_id}")
    return response.json()

def download_audio_file(file_id, save_path):
    """Download an audio file"""
    response = requests.get(f"{API_BASE_URL}/files/{file_id}/download")
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return {"message": f"File downloaded successfully to {save_path}"}
    else:
        return {"error": "File not found"}

def delete_audio_file(file_id):
    """Delete an audio file"""
    response = requests.delete(f"{API_BASE_URL}/files/{file_id}")
    return response.json()

def health_check():
    """Check if the API is running"""
    response = requests.get(API_BASE_URL)
    return response.json()

# Example usage
if __name__ == "__main__":
    print("Supabase Audio File Storage API Client Example")
    print("=" * 50)
    
    # Check if API is running
    try:
        health = health_check()
        print(f"API Status: {health}")
    except requests.exceptions.ConnectionError:
        print("Error: API is not running. Please start the API server first.")
        exit(1)
    
    # List files (initial)
    print("\nInitial file list:")
    files = list_audio_files()
    print(f"Found {len(files)} files")
    
    # If you have an audio file to upload, uncomment the following lines:
    # file_path = "path/to/your/audio/file.mp3"  # Update this path
    # if os.path.exists(file_path):
    #     print(f"\nUploading {file_path}...")
    #     upload_result = upload_audio_file(file_path)
    #     print(f"Upload result: {upload_result}")
    #     
    #     # List files after upload
    #     print("\nFile list after upload:")
    #     files = list_audio_files()
    #     for file in files:
    #         print(f"- {file['filename']} ({file['id']})")
    #         
    #     # Get info about the uploaded file
    #     file_id = upload_result['id']
    #     print(f"\nGetting info for file {file_id}:")
    #     file_info = get_file_info(file_id)
    #     print(f"File info: {file_info}")
    #     
    #     # Download the file
    #     download_path = f"downloaded_{upload_result['filename']}"
    #     print(f"\nDownloading file to {download_path}...")
    #     download_result = download_audio_file(file_id, download_path)
    #     print(f"Download result: {download_result}")
    #     
    #     # Delete the file
    #     print(f"\nDeleting file {file_id}...")
    #     delete_result = delete_audio_file(file_id)
    #     print(f"Delete result: {delete_result}")
    # else:
    #     print(f"\nFile {file_path} not found. Skipping upload example.")
    # 
    # # Final file list
    # print("\nFinal file list:")
    # files = list_audio_files()
    # print(f"Found {len(files)} files")

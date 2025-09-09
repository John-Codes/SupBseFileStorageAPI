import pytest
import requests
import time
import os
import json
from typing import Dict, Any

# Base URL for the API
BASE_URL = "http://localhost:8001"

# Test audio file content (simple WAV header for testing)
TEST_WAV_CONTENT = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'

# Test MP3 file content (minimal MP3 header for testing)
TEST_MP3_CONTENT = b'\xff\xfb\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

class TestAPIEndpoints:
    uploaded_file_id = None
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        assert "Supabase Audio File Storage API is running" in data["message"]
    
    def test_upload_wav_file(self):
        """Test uploading a WAV file"""
        files = {
            'file': ('test_audio.wav', TEST_WAV_CONTENT, 'audio/wav')
        }
        response = requests.post(f"{BASE_URL}/upload", files=files)
        
        # Provide a more informative error message if the upload fails
        assert response.status_code == 200, (
            f"Expected status code 200, but got {response.status_code}. "
            f"Response: {response.text}. "
            f"This might be due to incomplete Supabase setup. "
            f"Please check that you have created the 'audio-files' storage bucket "
            f"and the 'audio_files' database table as described in the detailed_setup_guide.md"
        )
        
        data = response.json()
        
        # Store the file ID for later tests
        TestAPIEndpoints.uploaded_file_id = data["id"]
        
        # Check that all expected fields are present
        assert "id" in data
        assert "filename" in data
        assert data["filename"] == "test_audio.wav"
        assert "content_type" in data
        assert data["content_type"] == "audio/wav"
        assert "size" in data
        assert data["size"] == len(TEST_WAV_CONTENT)
        assert "upload_timestamp" in data
        assert "storage_path" in data
    
    def test_upload_mp3_file(self):
        """Test uploading an MP3 file"""
        files = {
            'file': ('test_audio.mp3', TEST_MP3_CONTENT, 'audio/mpeg')
        }
        response = requests.post(f"{BASE_URL}/upload", files=files)
        
        # Provide a more informative error message if the upload fails
        assert response.status_code == 200, (
            f"Expected status code 200, but got {response.status_code}. "
            f"Response: {response.text}. "
            f"This might be due to incomplete Supabase setup. "
            f"Please check that you have created the 'audio-files' storage bucket "
            f"and the 'audio_files' database table as described in the detailed_setup_guide.md"
        )
        
        data = response.json()
        
        # Check that all expected fields are present
        assert "id" in data
        assert "filename" in data
        assert data["filename"] == "test_audio.mp3"
        assert "content_type" in data
        assert data["content_type"] == "audio/mpeg"
        assert "size" in data
        assert data["size"] == len(TEST_MP3_CONTENT)
        assert "upload_timestamp" in data
        assert "storage_path" in data
    
    def test_upload_invalid_file_type(self):
        """Test uploading an invalid file type"""
        # Create a simple text file content
        text_content = b"This is a text file, not an audio file"
        
        files = {
            'file': ('test_file.txt', text_content, 'text/plain')
        }
        response = requests.post(f"{BASE_URL}/upload", files=files)
        assert response.status_code == 400
        data = response.json()
        assert "Invalid file type" in data["detail"]
    
    def test_list_files(self):
        """Test listing all files"""
        response = requests.get(f"{BASE_URL}/files")
        assert response.status_code == 200
        data = response.json()
        
        # Should have at least the files we uploaded
        assert isinstance(data, list)
        assert len(data) >= 2  # At least our two test files
        
        # Check that our uploaded file is in the list
        if TestAPIEndpoints.uploaded_file_id:
            file_ids = [file["id"] for file in data]
            assert TestAPIEndpoints.uploaded_file_id in file_ids
    
    def test_get_file_info(self):
        """Test getting information about a specific file"""
        if not TestAPIEndpoints.uploaded_file_id:
            pytest.skip("No file uploaded yet")
        
        response = requests.get(f"{BASE_URL}/files/{TestAPIEndpoints.uploaded_file_id}")
        assert response.status_code == 200
        data = response.json()
        
        # Check that all expected fields are present
        assert data["id"] == TestAPIEndpoints.uploaded_file_id
        assert "filename" in data
        assert "content_type" in data
        assert "size" in data
        assert "upload_timestamp" in data
        assert "storage_path" in data
    
    def test_get_nonexistent_file(self):
        """Test getting information about a nonexistent file"""
        fake_id = "nonexistent-file-id-12345"
        response = requests.get(f"{BASE_URL}/files/{fake_id}")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "File not found"
    
    def test_download_file(self):
        """Test downloading a file"""
        if not TestAPIEndpoints.uploaded_file_id:
            pytest.skip("No file uploaded yet")
        
        response = requests.get(f"{BASE_URL}/files/{TestAPIEndpoints.uploaded_file_id}/download")
        assert response.status_code == 200
        # Check that the content type matches what we uploaded
        assert response.headers["content-type"] in ["audio/wav", "audio/mpeg"]
        # Check that we got some content back
        assert len(response.content) > 0
    
    def test_download_nonexistent_file(self):
        """Test downloading a nonexistent file"""
        fake_id = "nonexistent-file-id-12345"
        response = requests.get(f"{BASE_URL}/files/{fake_id}/download")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "File not found"
    
    def test_delete_file(self):
        """Test deleting a file"""
        if not TestAPIEndpoints.uploaded_file_id:
            pytest.skip("No file uploaded yet")
        
        # First, verify the file exists
        response = requests.get(f"{BASE_URL}/files/{TestAPIEndpoints.uploaded_file_id}")
        assert response.status_code == 200
        
        # Delete the file
        response = requests.delete(f"{BASE_URL}/files/{TestAPIEndpoints.uploaded_file_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "File deleted successfully"
        
        # Verify the file is gone
        response = requests.get(f"{BASE_URL}/files/{TestAPIEndpoints.uploaded_file_id}")
        assert response.status_code == 404
    
    def test_delete_nonexistent_file(self):
        """Test deleting a nonexistent file"""
        fake_id = "nonexistent-file-id-12345"
        response = requests.delete(f"{BASE_URL}/files/{fake_id}")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "File not found"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

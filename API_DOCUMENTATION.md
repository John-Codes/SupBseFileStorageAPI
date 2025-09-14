# Supabase Audio File Storage API Documentation

## Overview

The Supabase Audio File Storage API is a FastAPI-based service that provides CRUD operations for audio files using Supabase Storage and Database. It supports uploading, listing, retrieving, downloading, and deleting audio files with proper metadata management.

## Features

- Upload audio files with automatic metadata storage
- List all uploaded audio files
- Retrieve specific file information
- Download audio files
- Delete audio files with metadata cleanup
- Support for multiple audio formats (MP3, WAV, FLAC, AAC, OGG, M4A)
- Automatic UUID generation for file identification
- Secure storage using Supabase

## API Endpoints

### Health Check
**GET /**

Returns the health status of the API.

**Response:**
```json
{
  "status": "OK",
  "message": "Supabase Audio File Storage API is running"
}
```

### Upload Audio File
**POST /upload**

Uploads an audio file to Supabase Storage and creates metadata in the database.

**Request:**
- Form data with file parameter

**Supported File Types:**
- audio/mpeg (MP3)
- audio/wav (WAV)
- audio/x-wav (WAV)
- audio/flac (FLAC)
- audio/aac (AAC)
- audio/ogg (OGG)
- audio/mp4 (M4A)

**Response:**
```json
{
  "filename": "example.mp3",
  "content_type": "audio/mpeg",
  "size": 123456,
  "id": "980392bb-1997-4cca-a9ae-50a99debf3b3",
  "upload_timestamp": "2023-10-15T12:00:00.000000+00:00",
  "storage_path": "980392bb-1997-4cca-a9ae-50a99debf3b3_example.mp3"
}
```

### List All Audio Files
**GET /files**

Retrieves a list of all uploaded audio files with their metadata.

**Response:**
```json
[
  {
    "filename": "example.mp3",
    "content_type": "audio/mpeg",
    "size": 123456,
    "id": "980392bb-1997-4cca-a9ae-50a99debf3b3",
    "upload_timestamp": "2023-10-15T12:00:00.000000+00:00",
    "storage_path": "980392bb-1997-4cca-a9ae-50a99debf3b3_example.mp3"
  }
]
```

### Get File Information
**GET /files/{file_id}**

Retrieves metadata for a specific audio file.

**Parameters:**
- file_id (path): The UUID of the file

**Response:**
```json
{
  "filename": "example.mp3",
  "content_type": "audio/mpeg",
  "size": 123456,
  "id": "980392bb-1997-4cca-a9ae-50a99debf3b3",
  "upload_timestamp": "2023-10-15T12:00:00.000000+00:00",
  "storage_path": "980392bb-1997-4cca-a9ae-50a99debf3b3_example.mp3"
}
```

### Download Audio File
**GET /files/{file_id}/download**

Downloads the actual audio file content.

**Parameters:**
- file_id (path): The UUID of the file

**Response:**
- Binary file content with appropriate Content-Type and Content-Disposition headers

### Delete Audio File
**DELETE /files/{file_id}**

Deletes an audio file from both storage and metadata database.

**Parameters:**
- file_id (path): The UUID of the file

**Response:**
```json
{
  "message": "File deleted successfully"
}
```

## Setup Instructions

1. **Supabase Configuration:**
   - Create a Supabase project
   - Get your project URL and service role key
   - Create an `.env` file with:
     ```
     SUPABASE_URL=your_supabase_project_url
     SUPABASE_KEY=your_supabase_service_role_key
     ```

2. **Database Setup:**
   - Create an `audio_files` table in your Supabase database with the following columns:
     - id (TEXT, Primary Key)
     - filename (TEXT)
     - content_type (TEXT)
     - size (INTEGER)
     - upload_timestamp (TIMESTAMP)
     - storage_path (TEXT)

3. **Storage Setup:**
   - Create an `audio-files` storage bucket in your Supabase project

4. **Dependencies Installation:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Running the API:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8001`

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── config.py               # Supabase client configuration
├── models.py               # Pydantic models for data validation
├── storage.py              # Supabase storage operations
├── setup_supabase.py       # Supabase setup verification script
├── test_endpoints.py       # API endpoint tests
├── requirements.txt        # Python dependencies
├── setup_guide.py          # Interactive setup guide
├── detailed_setup_guide.md # Detailed setup instructions
├── README.md              # Project overview and usage
└── .env                   # Environment variables (not included in repo)
```

## Testing

Run the test suite to verify all endpoints work correctly:

```bash
python -m pytest test_endpoints.py -v
```

## Error Handling

The API provides appropriate HTTP status codes and error messages:
- 400 Bad Request: Invalid file type or missing filename
- 404 Not Found: File not found
- 500 Internal Server Error: Server-side errors during file operations

## Security Considerations

- The API uses Supabase service role key for administrative operations
- File type validation prevents malicious file uploads
- UUID-based file identification prevents path traversal attacks
- All timestamps are stored in UTC format

## Supported Audio Formats

| Format | MIME Type        | File Extension |
|--------|------------------|----------------|
| MP3    | audio/mpeg       | .mp3           |
| WAV    | audio/wav        | .wav           |
| FLAC   | audio/flac       | .flac          |
| AAC    | audio/aac        | .aac           |
| OGG    | audio/ogg        | .ogg           |
| M4A    | audio/mp4        | .m4a           |

## Usage Examples

### Upload a File (curl)
```bash
curl -X POST "http://localhost:8001/upload" -F "file=@example.mp3"
```

### List Files (curl)
```bash
curl -X GET "http://localhost:8001/files"
```

### Download a File (curl)
```bash
curl -X GET "http://localhost:8001/files/{file_id}/download" -o downloaded_file.mp3
```

### Delete a File (curl)
```bash
curl -X DELETE "http://localhost:8001/files/{file_id}"

# Supabase Audio File Storage API

A simple API for CRUD operations on audio files using Supabase Storage and Python FastAPI.

## Prerequisites

Before running this API, you MUST complete the following setup steps in your Supabase dashboard:

1. **Create the database table:**
   - Go to your Supabase project dashboard
   - Navigate to Table Editor
   - Click 'New Table'
   - Name it 'audio_files'
   - Add the following columns:
     - id (Text, Primary Key)
     - filename (Text)
     - content_type (Text)
     - size (Integer)
     - upload_timestamp (Timestamp)
     - storage_path (Text)
   - Click 'Save'

2. **Create the storage bucket:**
   - Go to your Supabase project dashboard
   - Navigate to Storage
   - Click 'New bucket'
   - Name it 'audio-files'
   - Set it as public if you want public access to files
   - Click 'Save'

3. **Set up Row Level Security (RLS):**
   - Go to your Supabase project dashboard
   - Navigate to Table Editor
   - Click on the 'audio_files' table
   - Click on 'RLS policies'
   - Create policies for SELECT, INSERT, UPDATE, and DELETE operations as needed for your use case

## Features

- Upload audio files (MP3, WAV, FLAC, AAC, OGG, M4A)
- List all uploaded audio files
- Get information about a specific audio file
- Download audio files
- Delete audio files

## Requirements

- Python 3.8+
- Supabase account

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up your Supabase credentials in a `.env` file:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

## Usage

1. Start the server:
   ```
   python main.py
   ```

2. The API will be available at `http://localhost:8001`

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload an audio file
- `GET /files` - List all audio files
- `GET /files/{file_id}` - Get information about a specific audio file
- `GET /files/{file_id}/download` - Download an audio file
- `DELETE /files/{file_id}` - Delete an audio file

## Testing

To run the tests:
```
pytest test_endpoints.py -v
```

## Note

Due to compatibility issues with the Supabase Python client, some features may not work as expected. The API will still run and provide basic functionality, but file operations may fail. Make sure to properly configure your Supabase project with the required table and storage bucket as described in the installation steps.

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
- Docker (for containerized deployment)

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. For development and testing, install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

3. Set up your Supabase credentials in a `.env` file:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

## Usage

### Option 1: Direct Python execution
1. Start the server:
   ```
   python main.py
   ```

2. The API will be available at `http://localhost:8001`

### Option 2: Docker (Recommended for production)
1. Build and run with Docker:
   ```
   docker build -t supabase-audio-api .
   docker run -p 8001:8001 --env-file .env supabase-audio-api
   ```

### Option 3: Docker Compose (Recommended for development)
1. Create a `.env` file with your Supabase credentials (see `env.example`)
2. Start the services:
   ```
   docker-compose up --build
   ```

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload an audio file
- `GET /files` - List all audio files
- `GET /files/{file_id}` - Get information about a specific audio file
- `GET /files/{file_id}/download` - Download an audio file
- `DELETE /files/{file_id}` - Delete an audio file

## Testing

### Option 1: Run tests against a running server
To run the tests, you must first start the API server:

1. Start the API server:
   ```
   python main.py
   ```
   or use the provided batch script:
   ```
   start_api.bat
   ```

2. In a separate terminal, run the tests:
   ```
   pytest test_endpoints.py -v
   ```
   or use the provided batch script:
   ```
   run_tests.bat
   ```

Note: The tests require the API server to be running on localhost:8001 to connect to it. All tests will fail if the server is not running.

### Option 2: Run tests in Docker
1. Build the Docker image:
   ```
   docker build -t supabase-audio-api .
   ```

2. Run tests in a container:
   ```
   docker run --env-file .env supabase-audio-api python -m pytest test_endpoints.py -v
   ```

## Documentation

Comprehensive API documentation is available in `API_DOCUMENTATION.md` which includes:
- Detailed endpoint descriptions
- Usage examples
- Setup instructions
- Supported audio formats
- Error handling information

## Client Example

A Python client example is provided in `client_example.py` that demonstrates how to:
- Upload audio files
- List all uploaded files
- Get file information
- Download files
- Delete files

## CI/CD Pipeline

This project includes a GitHub Actions workflow that:
- Runs security scans using Bandit
- Performs code quality checks with Pylint
- Builds and tests the Docker image
- Automatically deploys to GitHub Container Registry on main branch changes

## Production Considerations

The Dockerfile includes several production-ready features:
- Runs as a non-root user for security
- Uses uvicorn with multiple workers for better performance
- Optimized layer caching for faster builds
- Minimal base image to reduce attack surface

## Convenience Scripts

- `start_api.bat` - Starts the API server
- `run_tests.bat` - Runs the test suite

## Note

Due to compatibility issues with the Supabase Python client, some features may not work as expected. The API will still run and provide basic functionality, but file operations may fail. Make sure to properly configure your Supabase project with the required table and storage bucket as described in the installation steps.

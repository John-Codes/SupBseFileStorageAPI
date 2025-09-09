# Detailed Setup Guide for Supabase Audio File Storage API

This guide provides detailed instructions for setting up your Supabase project to work with the Audio File Storage API.

## Prerequisites

1. A Supabase account (free tier available at [supabase.com](https://supabase.com/))
2. This API project cloned to your local machine
3. Python 3.8+ installed

## Step-by-Step Setup

### 1. Create a New Supabase Project

1. Go to [supabase.com](https://supabase.com/) and sign in to your account
2. Click "New Project"
3. Enter a name for your project
4. Select a region closest to you
5. Set a secure database password
6. Click "Create New Project"

Wait for your project to be created (this may take a few minutes).

### 2. Get Your Supabase Credentials

1. In your project dashboard, click on the "Settings" gear icon in the left sidebar
2. Click "API" in the settings menu
3. Copy your "Project URL" and "anon public" key (service_role key for full access)
4. Create a `.env` file in your project root with these values:

```
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here
```

### 3. Create the Database Table

1. In your Supabase project dashboard, click on "Table Editor" in the left sidebar
2. Click "New Table"
3. Name the table `audio_files`
4. Add the following columns:
   - `id` (Text, Primary Key)
   - `filename` (Text)
   - `content_type` (Text)
   - `size` (Integer)
   - `upload_timestamp` (Timestamp)
   - `storage_path` (Text)
5. Click "Save"

### 4. Create the Storage Bucket

1. In your Supabase project dashboard, click on "Storage" in the left sidebar
2. Click "New bucket"
3. Name the bucket `audio-files`
4. Decide if you want the bucket to be public:
   - Public: Anyone with the URL can access files
   - Private: Only authenticated users can access files
5. Click "Save"

### 5. Set up Row Level Security (RLS)

RLS is enabled by default on the `audio_files` table. For the API to work properly, you need to configure the policies to allow the service role key to perform operations. Even though the service role key should bypass RLS, explicit policies are still required for all operations.

You need to create policies for each operation (SELECT, INSERT, UPDATE, DELETE) with these settings. Here's how to set up these policies in the Supabase dashboard:

1. In the Table Editor, click on the `audio_files` table
2. Click on "RLS policies" at the top
3. Ensure "Enable RLS" is toggled on
4. Create policies for each operation (SELECT, INSERT, UPDATE, DELETE) with these settings:
   - Policy name: "Allow all operations for service role" (or specific names for each)
   - Operation: Select the operation (SELECT, INSERT, etc.)
   - Roles: Add both "authenticated" and "anon" roles, or use "service_role" if available
   - USING expression (for SELECT): `true` (allows all rows to be selected)
   - WITH CHECK expression (for INSERT/UPDATE): `true` (allows all inserts/updates)
   - Click "Save policy"

For development and testing, you can create more permissive policies that allow all operations for all users. Here's how to set up these policies in the Supabase dashboard:

1. In the Table Editor, click on the `audio_files` table
2. Click on "RLS policies" at the top
3. Ensure "Enable RLS" is toggled on
4. Create policies for each operation (SELECT, INSERT, UPDATE, DELETE) with these settings:
   - Policy name: "Allow all operations" (or specific names for each)
   - Operation: Select the operation (SELECT, INSERT, etc.)
   - Roles: Leave as "authenticated" or add "anon" if needed
   - USING expression (for SELECT): `true` (allows all rows to be selected)
   - WITH CHECK expression (for INSERT/UPDATE): `true` (allows all inserts/updates)
   - Click "Save policy"

Alternatively, for development only, you can disable RLS temporarily:
1. In the Table Editor, click on the `audio_files` table
2. Click on "RLS policies" at the top
3. Toggle "Enable RLS" to off

Note: Disabling RLS is not recommended for production environments as it removes an important security layer.

### 6. Verify Your Setup

Run the provided setup verification script:

```bash
python setup_supabase.py
```

This script will check if your table and bucket exist and provide guidance if they don't.

## Troubleshooting Common Issues

### 500 Internal Server Errors

If you're getting 500 errors when uploading files, check:

1. That the `audio-files` bucket exists in your Supabase Storage
2. That your Supabase credentials in `.env` are correct
3. That the `audio_files` table exists with the correct schema
4. That RLS policies are properly configured

### Authentication Issues

If you're having authentication issues:

1. Make sure you're using the correct API key (anon public for basic access, service_role for full access)
2. Check that your Supabase project URL is correct
3. Ensure your network connection is stable

### File Upload Issues

If files aren't uploading correctly:

1. Check that the `audio-files` bucket exists and is properly configured
2. Verify that your RLS policies allow INSERT operations
3. Ensure the bucket has sufficient storage space

## Testing Your Setup

After completing all setup steps, run the tests:

```bash
pytest test_endpoints.py -v
```

All tests should pass if your setup is correct.

## Running the API

Start the API server:

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

The API will be available at `http://localhost:8001`.

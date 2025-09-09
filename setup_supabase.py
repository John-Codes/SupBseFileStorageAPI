import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if environment variables are set
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_audio_files_table():
    """Create the audio_files table if it doesn't exist"""
    try:
        # Try to query the table to see if it exists
        response = supabase.table('audio_files').select('*').limit(1).execute()
        print("audio_files table already exists")
        return True
    except Exception as e:
        print(f"audio_files table might not exist: {e}")
        print("Please create the table manually in your Supabase dashboard:")
        print("1. Go to your Supabase project dashboard")
        print("2. Navigate to Table Editor")
        print("3. Click 'New Table'")
        print("4. Name it 'audio_files'")
        print("5. Add the following columns:")
        print("   - id (Text, Primary Key)")
        print("   - filename (Text)")
        print("   - content_type (Text)")
        print("   - size (Integer)")
        print("   - upload_timestamp (Timestamp)")
        print("   - storage_path (Text)")
        print("6. Click 'Save'")
        return False

def create_audio_files_bucket():
    """Create the audio-files storage bucket if it doesn't exist"""
    try:
        # Try to list buckets to see if our bucket exists
        buckets = supabase.storage.list_buckets()
        for bucket in buckets:
            if bucket.name == 'audio-files':
                print("audio-files bucket already exists")
                return True
        
        print("audio-files bucket not found, attempting to create it...")
        # Try to create the bucket
        try:
            response = supabase.storage.create_bucket('audio-files')
            print("Successfully created audio-files bucket")
            return True
        except Exception as create_error:
            print(f"Failed to create bucket programmatically: {create_error}")
            print("Please create the bucket manually in your Supabase dashboard:")
            print("1. Go to your Supabase project dashboard")
            print("2. Navigate to Storage")
            print("3. Click 'New bucket'")
            print("4. Name it 'audio-files'")
            print("5. Set it as public if you want public access to files")
            print("6. Click 'Save'")
            return False
    except Exception as e:
        print(f"Error checking/creating bucket: {e}")
        print("Please create the bucket manually in your Supabase dashboard:")
        print("1. Go to your Supabase project dashboard")
        print("2. Navigate to Storage")
        print("3. Click 'New bucket'")
        print("4. Name it 'audio-files'")
        print("5. Set it as public if you want public access to files")
        print("6. Click 'Save'")
        return False

if __name__ == "__main__":
    print("Setting up Supabase for Audio File Storage API...")
    print(f"Supabase URL: {SUPABASE_URL}")
    
    # Try to create/check table
    table_exists = create_audio_files_table()
    
    # Try to create/check bucket
    bucket_exists = create_audio_files_bucket()
    
    if table_exists and bucket_exists:
        print("\nSetup complete! Both table and bucket exist.")
    else:
        print("\nPlease follow the instructions above to complete setup.")

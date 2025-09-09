import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {'*' * len(SUPABASE_KEY) if SUPABASE_KEY else 'None'}")

# Validate environment variables
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    exit(1)

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully")
    
    # Try to list tables
    try:
        # Try a simple query to check connection
        response = supabase.table("audio_files").select("*").limit(1).execute()
        print("Successfully connected to Supabase and queried audio_files table")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error querying audio_files table: {e}")
        print("The audio_files table might not exist yet.")
        
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    exit(1)

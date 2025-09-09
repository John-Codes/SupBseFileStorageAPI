#!/usr/bin/env python3
"""
Detailed Setup Guide for Supabase Audio File Storage API

This script provides detailed, interactive instructions for setting up the required
database table and storage bucket in your Supabase dashboard.
"""

import os
from dotenv import load_dotenv

def print_welcome():
    """Print welcome message and overview"""
    print("=" * 70)
    print("Supabase Audio File Storage API - Detailed Setup Guide")
    print("=" * 70)
    print("\nThis guide will help you set up the required resources in your")
    print("Supabase dashboard. Please follow each step carefully.\n")

def verify_env_file():
    """Verify that the .env file exists and contains the required variables"""
    print("Step 1: Verify .env File")
    print("-" * 30)
    
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        print("✓ .env file found with SUPABASE_URL and SUPABASE_KEY")
        print(f"  Supabase URL: {supabase_url[:30]}...")
        return True
    else:
        print("✗ .env file is missing or doesn't contain SUPABASE_URL and SUPABASE_KEY")
        print("\nPlease create a .env file in your project directory with your Supabase credentials:")
        print("\n  SUPABASE_URL=your_supabase_url")
        print("  SUPABASE_KEY=your_supabase_key\n")
        return False

def setup_database_table():
    """Provide detailed instructions for setting up the database table"""
    print("\nStep 2: Create the Database Table")
    print("-" * 40)
    print("1. Go to your Supabase project dashboard")
    print("2. In the left sidebar, click on 'Table Editor'")
    print("3. Click the 'New Table' button")
    print("4. In the 'Name' field, enter: audio_files")
    print("5. Add the following columns:")
    print("   a. Column 1:")
    print("      - Name: id")
    print("      - Type: text")
    print("      - Check 'Is Primary Key'")
    print("   b. Column 2:")
    print("      - Name: filename")
    print("      - Type: text")
    print("   c. Column 3:")
    print("      - Name: content_type")
    print("      - Type: text")
    print("   d. Column 4:")
    print("      - Name: size")
    print("      - Type: int4 (integer)")
    print("   e. Column 5:")
    print("      - Name: upload_timestamp")
    print("      - Type: timestamptz (timestamp with time zone)")
    print("   f. Column 6:")
    print("      - Name: storage_path")
    print("      - Type: text")
    print("6. Click 'Save' to create the table")
    input("\nPress Enter after completing these steps...")

def setup_storage_bucket():
    """Provide detailed instructions for setting up the storage bucket"""
    print("\nStep 3: Create the Storage Bucket")
    print("-" * 40)
    print("1. Go to your Supabase project dashboard")
    print("2. In the left sidebar, click on 'Storage'")
    print("3. Click the 'New bucket' button")
    print("4. In the 'Name' field, enter: audio-files")
    print("5. Decide if you want the bucket to be public:")
    print("   - For testing: Check 'Public bucket'")
    print("   - For production: Leave unchecked and set up proper access controls")
    print("6. Click 'Save' to create the bucket")
    input("\nPress Enter after completing these steps...")

def setup_rls_policies():
    """Provide instructions for setting up RLS policies"""
    print("\nStep 4: Set up Row Level Security (RLS)")
    print("-" * 40)
    print("1. Go to your Supabase project dashboard")
    print("2. In the left sidebar, click on 'Table Editor'")
    print("3. Find and click on the 'audio_files' table")
    print("4. Click on the 'RLS policies' tab")
    print("5. Toggle 'Enable RLS' to ON")
    print("6. For testing, you can create simple policies:")
    print("   - For SELECT: (true) - allows anyone to read")
    print("   - For INSERT: (true) - allows anyone to insert")
    print("   - For UPDATE: (true) - allows anyone to update")
    print("   - For DELETE: (true) - allows anyone to delete")
    print("\nNote: For production, you should implement proper authentication")
    print("and authorization policies.")
    input("\nPress Enter after completing these steps...")

def verify_setup():
    """Verify that the setup is complete"""
    print("\nStep 5: Verify Setup")
    print("-" * 25)
    print("Let's verify that your setup is complete.")
    
    # Try to check if the table exists
    try:
        from config import supabase
        if supabase:
            try:
                response = supabase.table('audio_files').select('*').limit(1).execute()
                print("✓ Database table 'audio_files' exists")
            except Exception as e:
                print("✗ Database table 'audio_files' might not exist yet")
                print(f"  Error: {e}")
        else:
            print("✗ Supabase client not available")
    except Exception as e:
        print(f"✗ Could not verify database table: {e}")
    
    # Try to check if the bucket exists
    try:
        from config import supabase
        if supabase:
            try:
                buckets = supabase.storage.list_buckets()
                bucket_names = [bucket.name for bucket in buckets]
                if 'audio-files' in bucket_names:
                    print("✓ Storage bucket 'audio-files' exists")
                else:
                    print("✗ Storage bucket 'audio-files' not found")
            except Exception as e:
                print("✗ Could not verify storage bucket")
                print(f"  Error: {e}")
        else:
            print("✗ Supabase client not available")
    except Exception as e:
        print(f"✗ Could not verify storage bucket: {e}")

def main():
    """Main function to run the detailed setup guide"""
    print_welcome()
    
    # Verify .env file
    if not verify_env_file():
        print("\nPlease create the .env file and run this script again.")
        return
    
    # Setup database table
    setup_database_table()
    
    # Setup storage bucket
    setup_storage_bucket()
    
    # Setup RLS policies
    setup_rls_policies()
    
    # Verify setup
    verify_setup()
    
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print("\nYou're now ready to run the API and tests:")
    print("  - Start the API: python main.py")
    print("  - Run tests: pytest test_endpoints.py -v")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()

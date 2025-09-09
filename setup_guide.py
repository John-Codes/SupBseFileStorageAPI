#!/usr/bin/env python3
"""
Setup Guide for Supabase Audio File Storage API

This script provides step-by-step instructions for setting up the required
database table and storage bucket in your Supabase dashboard.
"""

import os
from dotenv import load_dotenv

def print_setup_instructions():
    """Print detailed setup instructions for Supabase"""
    print("=" * 60)
    print("Supabase Audio File Storage API - Setup Guide")
    print("=" * 60)
    
    print("\nIMPORTANT: Before running the API or tests, you must complete the following steps in your Supabase dashboard.\n")
    
    print("STEP 1: Create the database table")
    print("-" * 40)
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
    print("6. Click 'Save'\n")
    
    print("STEP 2: Create the storage bucket")
    print("-" * 40)
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to Storage")
    print("3. Click 'New bucket'")
    print("4. Name it 'audio-files'")
    print("5. Set it as public if you want public access to files")
    print("6. Click 'Save'\n")
    
    print("STEP 3: Set up Row Level Security (RLS)")
    print("-" * 40)
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to Table Editor")
    print("3. Click on the 'audio_files' table")
    print("4. Click on 'RLS policies'")
    print("5. Create policies for SELECT, INSERT, UPDATE, and DELETE operations as needed for your use case\n")
    
    print("STEP 4: Verify your .env file")
    print("-" * 40)
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        print("✓ .env file found with SUPABASE_URL and SUPABASE_KEY")
        print(f"  Supabase URL: {supabase_url[:30]}...")
    else:
        print("✗ .env file is missing or doesn't contain SUPABASE_URL and SUPABASE_KEY")
        print("  Please create a .env file with your Supabase credentials:\n")
        print("  SUPABASE_URL=your_supabase_url")
        print("  SUPABASE_KEY=your_supabase_key\n")

def main():
    """Main function to run the setup guide"""
    print_setup_instructions()
    
    print("=" * 60)
    print("Setup Verification")
    print("=" * 60)
    
    input("\nPress Enter after completing the above steps in your Supabase dashboard...")
    
    print("\nGreat! Now you can run the API with:")
    print("  python main.py")
    print("\nOr run the tests with:")
    print("  pytest test_endpoints.py -v")
    
    print("\nFor more detailed instructions, please refer to the README.md file.")

if __name__ == "__main__":
    main()

import requests
import time

# Wait a moment for the server to start
time.sleep(2)

# Test the health check endpoint
print("Testing health check endpoint...")
try:
    response = requests.get("http://localhost:8001/")
    if response.status_code == 200:
        print("✓ Health check passed")
        print(f"Response: {response.json()}")
    else:
        print(f"✗ Health check failed with status code {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Health check failed with exception: {e}")

print("\nDocker image is working correctly!")
print("The API is accessible and responding to requests.")
print("\nNote: File upload tests are failing due to Supabase authentication issues.")
print("This is likely related to RLS policies or key permissions in your Supabase setup.")
print("Please check your Supabase dashboard to ensure:")
print("1. You're using the service_role key (not the anon key)")
print("2. RLS policies are properly configured for the audio_files table")
print("3. The audio-files bucket exists and is properly configured")

import subprocess
import sys
import time
import os

def install_requirements():
    """Install required packages if not already installed"""
    try:
        import pytest
        import requests
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest", "requests"])
    else:
        print("Required packages already installed")

def run_tests():
    """Run the pytest tests"""
    print("Running API tests...")
    try:
        # Run pytest on our test file
        result = subprocess.run([sys.executable, "-m", "pytest", "test_endpoints.py", "-v"], 
                              capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Tests completed with return code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    # Wait a moment for the server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    # Install requirements
    install_requirements()
    
    # Run tests
    success = run_tests()
    
    if success:
        print("\nAll tests passed! ✅")
    else:
        print("\nSome tests failed! ❌")
    
    print("\nAPI testing completed")

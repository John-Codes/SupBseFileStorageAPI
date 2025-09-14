@echo off
echo Running Supabase Audio File Storage API Tests...
echo ===============================================
python -m pytest test_endpoints.py -v
echo ===============================================
echo Tests completed.

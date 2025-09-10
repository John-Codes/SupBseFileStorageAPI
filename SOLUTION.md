# Solution for Supabase Audio File Storage API RLS Issues

## Problem
The tests are failing with a "403 Unauthorized" error and "new row violates row-level security policy" message. This is because the Row Level Security (RLS) policies in Supabase are not properly configured.

## Solution

### Option 1: Use Service Role Key (Recommended)
1. In your Supabase project dashboard, go to Settings > API
2. Copy the "service_role" key (this key bypasses RLS restrictions)
3. Update your `.env` file with the service_role key:

```
SUPABASE_URL=https://wabhntpzxvthzjhybwar.supabase.co
SUPABASE_KEY=YOUR_SERVICE_ROLE_KEY_HERE
```

### Option 2: Configure RLS Policies
If you want to keep using the anon key, you need to configure RLS policies in your Supabase dashboard:

1. Go to Table Editor > audio_files > RLS policies
2. Ensure "Enable RLS" is toggled on
3. Create policies for each operation:
   - For SELECT: Name "Allow all SELECT", USING expression: `true`
   - For INSERT: Name "Allow all INSERT", WITH CHECK expression: `true`
   - For UPDATE: Name "Allow all UPDATE", WITH CHECK expression: `true`
   - For DELETE: Name "Allow all DELETE", USING expression: `true`

### Option 3: Disable RLS (Development Only)
For development purposes only, you can disable RLS:
1. Go to Table Editor > audio_files > RLS policies
2. Toggle "Enable RLS" to off

## After Applying the Solution
1. Save your `.env` file
2. Run the API server: `python main.py`
3. In another terminal, run the tests: `python test_endpoints.py`

The tests should now pass successfully.

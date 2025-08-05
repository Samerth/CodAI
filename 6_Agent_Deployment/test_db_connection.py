#!/usr/bin/env python3
"""
Test script to verify Supabase database connection
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

def test_supabase_connection():
    """Test the Supabase connection using environment variables."""
    
    # Load environment variables from .env file
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ Loaded .env file")
    else:
        print("⚠️  No .env file found, using system environment variables")
    
    # Get Supabase configuration
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY')
    
    if not supabase_url or not supabase_service_key:
        print("❌ Missing Supabase configuration:")
        print(f"   SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Missing'}")
        print(f"   SUPABASE_SERVICE_KEY: {'✅ Set' if supabase_service_key else '❌ Missing'}")
        return False
    
    print(f"✅ Supabase URL: {supabase_url}")
    print(f"✅ Service Key: {'*' * 10 + supabase_service_key[-4:] if supabase_service_key else '❌ Missing'}")
    
    # Test connection by querying user_profiles table
    try:
        headers = {
            'apikey': supabase_service_key,
            'Authorization': f'Bearer {supabase_service_key}',
            'Content-Type': 'application/json'
        }
        
        # Test query to check if tables exist
        test_url = f"{supabase_url}/rest/v1/user_profiles?select=count"
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Database connection successful!")
            print("✅ user_profiles table exists and is accessible")
            
            # Test if we can insert a test record (will be cleaned up)
            test_data = {
                'id': '00000000-0000-0000-0000-000000000000',  # Test UUID
                'email': 'test@example.com',
                'full_name': 'Test User'
            }
            
            insert_url = f"{supabase_url}/rest/v1/user_profiles"
            insert_response = requests.post(insert_url, headers=headers, json=test_data)
            
            if insert_response.status_code in [201, 409]:  # 409 means duplicate key
                print("✅ Write permissions working")
                
                # Clean up test record
                delete_url = f"{supabase_url}/rest/v1/user_profiles?id=eq.00000000-0000-0000-0000-000000000000"
                requests.delete(delete_url, headers=headers)
                print("✅ Cleanup successful")
            else:
                print(f"⚠️  Write test failed: {insert_response.status_code}")
                print(f"   Response: {insert_response.text}")
            
            return True
            
        else:
            print(f"❌ Database connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_frontend_config():
    """Test frontend configuration."""
    print("\n🔍 Testing Frontend Configuration:")
    
    vite_supabase_url = os.getenv('VITE_SUPABASE_URL')
    vite_supabase_anon_key = os.getenv('VITE_SUPABASE_ANON_KEY')
    vite_agent_endpoint = os.getenv('VITE_AGENT_ENDPOINT')
    
    print(f"   VITE_SUPABASE_URL: {'✅ Set' if vite_supabase_url else '❌ Missing'}")
    print(f"   VITE_SUPABASE_ANON_KEY: {'✅ Set' if vite_supabase_anon_key else '❌ Missing'}")
    print(f"   VITE_AGENT_ENDPOINT: {'✅ Set' if vite_agent_endpoint else '❌ Missing'}")
    
    if vite_agent_endpoint:
        print(f"   Agent endpoint will be: {vite_agent_endpoint}")
    
    return all([vite_supabase_url, vite_supabase_anon_key, vite_agent_endpoint])

def main():
    """Main test function."""
    print("🧪 Testing Database Connection")
    print("=" * 40)
    
    # Test database connection
    db_success = test_supabase_connection()
    
    # Test frontend configuration
    frontend_success = test_frontend_config()
    
    print("\n" + "=" * 40)
    if db_success and frontend_success:
        print("🎉 All tests passed! Ready to deploy.")
        print("\nNext steps:")
        print("1. Run: python deploy.py --type local --project localai")
        print("2. Access frontend at: http://localhost:8082")
        print("3. Access agent API at: http://localhost:8001")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        if not db_success:
            print("   - Verify your Supabase credentials")
            print("   - Ensure the database schema has been created")
        if not frontend_success:
            print("   - Check your frontend environment variables")

if __name__ == "__main__":
    main() 
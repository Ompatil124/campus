import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Try to get secrets from Streamlit secrets first, then environment variables
# Helper function to safely get secrets
def get_secret(key_name):
    try:
        return st.secrets.get(key_name)
    except Exception:
        return None

url = get_secret("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
key = get_secret("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    # Don't raise error immediately to allow importing safely, but operations will fail
    print("Warning: Supabase URL and SERVICE_ROLE_KEY not found.")
    supabase = None
else:
    try:
        supabase: Client = create_client(url, key)
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
        supabase = None

def init_db():
    """
    Checks the database connection.
    Returns True if connected, False otherwise.
    """
    if not supabase:
        return False
    try:
        # Simple health check query
        supabase.table('incidents').select('count', count='exact').limit(0).execute()
        return True
    except Exception as e:
        print(f"Supabase Connection Check Error: {e}")
        return False

def upload_proof(file_obj, file_name):
    """
    Uploads a file to Supabase Storage 'proofs' bucket.
    Returns the public URL of the uploaded file.
    """
    if not supabase: return None
    try:
        bucket_name = "proofs"
        file_path = f"{file_name}"
        file_obj.seek(0)
        file_content = file_obj.read()
        
        # Upload
        supabase.storage.from_(bucket_name).upload(
            file=file_content,
            path=file_path,
            file_options={"content-type": file_obj.type}
        )
        
        # Get Public URL
        res = supabase.storage.from_(bucket_name).get_public_url(file_path)
        return res
    except Exception as e:
        print(f"Supabase Storage Error: {e}")
        return None

def insert_incident(data):
    """
    Inserts a new incident into the Supabase 'incidents' table.
    Returns the response object or None on failure.
    """
    if not supabase: return None
    try:
        # Map generic 'timestamp' to 'last_updated' as per actual schema
        payload = data.copy()
        
        # Ensure we have a valid timestamp compatible with Supabase (ISO format preferred)
        if 'timestamp' in payload:
            payload['last_updated'] = payload.pop('timestamp')
        
        response = supabase.table('incidents').insert(payload).execute()
        return response
    except Exception as e:
        print(f"Supabase Insert Error: {e}")
        return None

def get_status(report_id):
    """
    Retrieves the status and admin remark for a given report_id.
    Returns (status, admin_remark) tuple or None if not found.
    """
    if not supabase: return None
    try:
        response = supabase.table('incidents').select('status, admin_remark').eq('report_id', report_id).execute()
        if response.data and len(response.data) > 0:
            record = response.data[0]
            return record.get('status'), record.get('admin_remark')
        return None
    except Exception as e:
        print(f"Supabase Get Status Error: {e}")
        return None

def get_all_incidents():
    """
    Retrieves all incidents, ordered by timestamp descending.
    Returns a list of dictionaries.
    """
    if not supabase: return []
    try:
        # Sort by last_updated which acts as our timestamp
        response = supabase.table('incidents').select('*').order('last_updated', desc=True).execute()
        data = response.data if response.data else []
        
        # Map 'last_updated' back to 'timestamp' for app compatibility
        for row in data:
            if 'last_updated' in row:
                row['timestamp'] = row['last_updated']
        
        return data
    except Exception as e:
        print(f"Supabase Get All Error: {e}")
        return []

def update_incident(report_id, status, remark):
    """
    Updates the status and admin_remark for a specific incident.
    """
    if not supabase: return None
    try:
        response = supabase.table('incidents').update({
            'status': status, 
            'admin_remark': remark
        }).eq('report_id', report_id).execute()
        return response
    except Exception as e:
        print(f"Supabase Update Error: {e}")
        return None

def delete_incident(report_id):
    """
    Deletes an incident from the Supabase 'incidents' table.
    """
    if not supabase: return None
    try:
        response = supabase.table('incidents').delete().eq('report_id', report_id).execute()
        return response
    except Exception as e:
        print(f"Supabase Delete Error: {e}")
        return None

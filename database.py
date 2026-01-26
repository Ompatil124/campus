import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
# Use service role key to bypass RLS policies
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    raise ValueError("Supabase URL and SERVICE_ROLE_KEY must be set in .env file")

supabase: Client = create_client(url, key)

def init_db():
    """
    Initializes the database connection.
    For Supabase, the table creation is handled via the dashboard/SQL editor,
    so this function is a placeholder or can be used for connection checks.
    """
    pass

def upload_proof(file_obj, file_name):
    """
    Uploads a file to Supabase Storage 'proofs' bucket.
    Returns the public URL of the uploaded file.
    """
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
    """
    try:
        # Map generic 'timestamp' to 'last_updated' as per actual schema
        payload = data.copy()
        if 'timestamp' in payload:
            payload['last_updated'] = payload.pop('timestamp')
        
        # Remove any keys that shouldn't be sent if they are None/Empty and not nullable in DB?
        # Based on schema check, most are text.
        
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
    try:
        response = supabase.table('incidents').delete().eq('report_id', report_id).execute()
        return response
    except Exception as e:
        print(f"Supabase Delete Error: {e}")
        return None

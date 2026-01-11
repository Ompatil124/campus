import os

from dotenv import load_dotenv
load_dotenv()

from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_ANON_KEY or SUPABASE_URL.startswith('your_'):
    raise ValueError("Please set valid SUPABASE_URL and SUPABASE_ANON_KEY in .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_connection():
    return supabase

def create_tables():
    # Tables are created in Supabase dashboard
    pass

def check_connection():
    try:
        supabase.table('incidents').select('count').limit(1).execute()
        return "Supabase connected"
    except Exception as e:
        return f"Supabase connection failed: {e}"

def insert_incident(data):
    if data.get('proof'):
        import tempfile
        import os
        file_name = f"{data['report_id']}.{data.get('proof_type', 'file').split('/')[-1]}"
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
            temp_file.write(data['proof'])
            temp_path = temp_file.name
        try:
            options = {"content-type": data.get('proof_type')}
            supabase.storage.from_('proofs').upload(file_name, temp_path, options)
            proof_url = f"{SUPABASE_URL}/storage/v1/object/public/proofs/{file_name}"
            data['proof'] = proof_url
        finally:
            # Clean up temp file
            os.unlink(temp_path)
    supabase.table('incidents').insert(data).execute()

def get_status(report_id):
    result = supabase.table('incidents').select('status').eq('report_id', report_id).execute().data
    return result[0]['status'] if result else None

def get_admin_remark(report_id):
    result = supabase.table('incidents').select('admin_remark').eq('report_id', report_id).execute().data
    return result[0]['admin_remark'] if result and result[0]['admin_remark'] else None

def get_all_incidents():
    response = supabase.table('incidents').select('*').order('last_updated', desc=True).execute()
    return response.data

def update_incident(report_id, updates):
    supabase.table('incidents').update(updates).eq('report_id', report_id).execute()

# CampusSafe

A Streamlit-based platform for anonymous incident reporting on campus, featuring AI-powered classification and sentiment analysis.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Supabase:
   - Create a Supabase account at [supabase.com](https://supabase.com)
   - Create a new project
   - Go to Settings > API to get your Project URL and anon public key
   - Update the `.env` file with your credentials:
     ```
     SUPABASE_URL=your_project_url
     SUPABASE_ANON_KEY=your_anon_key
     ```
   - Create a storage bucket:
     - Go to Storage in your Supabase dashboard
     - Create a new bucket named 'proofs'
     - Make it public (uncheck "Private")
   - Create the 'incidents' table in Supabase with this SQL:
     ```sql
     CREATE TABLE incidents (
         report_id TEXT PRIMARY KEY,
         category TEXT,
         description TEXT,
         sentiment REAL,
         urgency TEXT CHECK (urgency IN ('Low', 'Medium', 'High')),
         location TEXT,
         status TEXT CHECK (status IN ('Pending', 'Under Review', 'Resolved')),
         admin_remark TEXT,
         last_updated TEXT,
         proof TEXT,
         proof_type TEXT
     );
     ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

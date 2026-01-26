import sqlite3
import os
from datetime import datetime

DB_NAME = "campussafe.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            report_id TEXT PRIMARY KEY,
            category TEXT,
            description TEXT,
            sentiment REAL,
            urgency TEXT,
            location TEXT,
            status TEXT,
            admin_remark TEXT,
            timestamp TEXT,
            proof_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_incident(data):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO incidents (
                report_id, category, description, sentiment, urgency, 
                location, status, admin_remark, timestamp, proof_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['report_id'], data['category'], data['description'], 
            data['sentiment'], data['urgency'], data['location'], 
            data.get('status', 'Pending'), data.get('admin_remark', ''), 
            data['timestamp'], data.get('proof_type')
        ))
        conn.commit()
    except Exception as e:
        print(f"DB Error: {e}")
    finally:
        conn.close()

def get_status(report_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT status, admin_remark FROM incidents WHERE report_id = ?', (report_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_all_incidents():
    conn = sqlite3.connect(DB_NAME)
    # Return as list of dicts for pandas compatibility
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM incidents ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_incident(report_id, status, remark):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE incidents 
        SET status = ?, admin_remark = ? 
        WHERE report_id = ?
    ''', (status, remark, report_id))
    conn.commit()
    conn.close()

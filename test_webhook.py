import requests
import json

def send_to_discord(report_id, proof_bytes, report_data):
    url = "https://discordapp.com/api/webhooks/1464631979491201211/gVERDrnBmxhLnIpJIZyHTabE7psdCxrG4WA7Y4frYQ3pOwaB6alyw80OLRMZ7Tvo_Lav"
    embed = {
        "title": f"Incident Report: {report_id}",
        "description": report_data['description'],
        "color": 0xFF6B6B,
        "fields": [
            {"name": "Category", "value": report_data['category'], "inline": True},
            {"name": "Urgency", "value": report_data['urgency'], "inline": True},
            {"name": "Location", "value": report_data['location'], "inline": True},
            {"name": "Sentiment Score", "value": str(report_data['sentiment']), "inline": True},
            {"name": "Status", "value": report_data['status'], "inline": True},
            {"name": "Submitted At", "value": report_data['last_updated'], "inline": True},
        ]
    }
    payload = {"embeds": [embed]}
    if proof_bytes:
        files = {"file": ("proof", proof_bytes), "payload_json": (None, json.dumps(payload))}
        response = requests.post(url, files=files)
    else:
        response = requests.post(url, json=payload)

    print(f"Response status: {response.status_code}")

# Sample report data
sample_data = {
    'category': 'Academic Stress',
    'description': 'I witnessed a student being bullied in the library due to academic pressure.',
    'sentiment': -0.2,
    'urgency': 'High',
    'location': 'Campus Library',
    'status': 'Pending',
    'last_updated': '2026-01-25 11:00:00',
}

send_to_discord("TEST456", b"Sample proof content", sample_data)
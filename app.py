from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
import traceback

# Google Sheets (MODERN - No deprecated libraries)
GOOGLE_SHEETS_AVAILABLE = False
try:
    import gspread
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    GOOGLE_SHEETS_AVAILABLE = True
    print("✅ Modern Google Sheets library loaded")
except ImportError:
    print("⚠️  Install: pip install gspread google-auth")

app = Flask(__name__)

# Paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_DIR, 'form_submissions.json')

# Google Sheets
gc = None
SHEET = None
SHEET_ID = None

def init_google_sheets():
    global gc, SHEET, SHEET_ID
    try:
        creds_file = os.path.join(PROJECT_DIR, 'credentials.json')
        if not os.path.exists(creds_file):
            print("⚠️  No credentials.json found")
            return False
            
        # MODERN AUTH (2026 standard)
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = ServiceAccountCredentials.from_service_account_file(
            creds_file, scopes=scope
        )
        gc = gspread.authorize(creds)
        
        SHEET_ID = 'https://docs.google.com/spreadsheets/d/1DdS5w16shJnhz1Ufey_foAWMaA4nsQLHNXj9ylCr7Eg/edit?usp=drive_link'  # Replace this!
        if SHEET_ID == 'https://docs.google.com/spreadsheets/d/1DdS5w16shJnhz1Ufey_foAWMaA4nsQLHNXj9ylCr7Eg/edit?usp=drive_link':
            print("⚠️  Update SHEET_ID in app.py")
            return False
            
        SHEET = gc.open_by_key(SHEET_ID)
        print(f"✅ Google Sheets: {SHEET.sheet1.title}")
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets setup failed: {e}")
        return False

def log_form_submission(data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    submission = {
        'timestamp': timestamp,
        'name': data.get('name', ''),
        'phone': data.get('phone', ''),
        'email': data.get('email', ''),
        'business': data.get('business', ''),
        'message': data.get('message', '')
    }
    
    # 1. ALWAYS SAVE JSON
    json_success = False
    try:
        submissions = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    submissions = json.load(f)
            except:
                pass
        
        submissions.append(submission)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, indent=2, ensure_ascii=False)
        json_success = True
        print(f"✅ JSON: {submission['name']} - {submission['phone']}")
    except Exception as e:
        print(f"❌ JSON failed: {e}")
    
    # 2. GOOGLE SHEETS (Bonus)
    if SHEET:
        try:
            row = [timestamp, submission['name'], submission['phone'], 
                   submission['email'], submission['business'], submission['message']]
            SHEET.sheet1.append_row(row)
            print(f"✅ SHEETS: {submission['name']} - {submission['phone']}")
        except Exception as e:
            print(f"❌ Sheets failed: {e}")
    
    return json_success

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    try:
        data = request.json
        print(f"📥 FORM: {data}")
        success = log_form_submission(data)
        return jsonify({
            'success': success,
            'message': 'Lead saved! Check console + form_submissions.json'
        })
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/test')
def test():
    log_form_submission({
        'name': 'TEST USER', 'phone': '9999999999',
        'email': 'test@example.com', 'business': 'Test Co.',
        'message': 'Test submission OK'
    })
    return f"""
    <h1>✅ TEST SUCCESS!</h1>
    <p>📄 JSON: {LOG_FILE}</p>
    <p>📊 Sheets: {'✅ Connected' if SHEET else '⚠️ Not configured'}</p>
    <a href="/">← Website</a> | <a href="/test">Test Again</a>
    """

if __name__ == '__main__':
    print("🚀 CrestWeb Server v2.0")
    print(f"📁 Folder: {PROJECT_DIR}")
    
    init_google_sheets()
    print("🌐 http://127.0.0.1:5000")
    print("🧪 http://127.0.0.1:5000/test")
    print("📄 JSON always works | Sheets optional")
    app.run(debug=True, host='0.0.0.0', port=5000)

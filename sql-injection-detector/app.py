from flask import Flask, request, jsonify
from sql_injection_detector import SQLInjectionDetector, ThreatLogger

app = Flask(__name__)
detector = SQLInjectionDetector()
logger = ThreatLogger()

@app.route('/analyze', methods=['POST'])
def analyze_request():
    try:
        request_data = request.get_json()
        if detector.analyze_parameters(request_data):
            logger.log_attempt(request_data)
            return jsonify({
                "status": "danger",
                "message": "Potential SQL injection attempt detected!"
            }), 403
        return jsonify({"status": "safe"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import time

app = Flask(__name__)

# 1. Setup Gemini using Environment Variable (Safe for K8s)
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/log', methods=['POST'])
def analyze_log():
    data = request.json
    incoming_log = data.get('log', 'No log data provided')
    
    print(f"\n[Incoming Alert]: {incoming_log}")

    try:
        # 2. Ask Gemini for a fix (Keep it brief to save tokens/time)
        prompt = f"Act as an Expert SRE. Explain this error and give one command-line fix: {incoming_log}"
        
        response = model.generate_content(prompt)
        
        print(f"[Gemini Advice]: {response.text}")
        
        # Artificial small delay to prevent hitting free-tier limits too fast
        time.sleep(1) 
        
        return jsonify({
            "status": "success",
            "analysis": response.text
        }), 200

    except Exception as e:
        print(f"[Error]: {str(e)}")
        return jsonify({"status": "api_error", "message": "Gemini is busy or rate limited"}), 500

if __name__ == '__main__':
    # 0.0.0.0 allows the container to be reached by other pods in the cluster
    app.run(host='0.0.0.0', port=5000)
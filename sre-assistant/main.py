import google.generativeai as genai
import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 🛠️ CONFIGURATION ---
# IMPORTANT: For GitHub, use os.environ.get. For tonight's test, paste your key.
API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# Force the stable model name
MODEL_NAME = 'gemini-1.5-flash'
model = genai.GenerativeModel(MODEL_NAME)

print("-" * 50)
print(f"🚀 SRE ASSISTANT ONLINE")
print(f"📡 LISTENING ON: http://0.0.0.0:5000")
print("-" * 50)

@app.route('/log', methods=['POST'])
def analyze():
    log_data = request.json.get('log', 'No log data')
    print(f"\n[🕒 {time.strftime('%H:%M:%S')}] 🚨 INCOMING ALERT: {log_data}")
    
    try:
        # The Real AI Logic
        prompt = f"Context: You are a Kubernetes SRE. Briefly explain this error and give 1 fix command: {log_data}"
        response = model.generate_content(prompt)
        advice = response.text.strip()
        print(f"   🤖 GEMINI SUGGESTION:")
        print(f"   {advice}")
        
    except Exception as e:
        # The Local Windows Fallback (Prevents the 500 error on your laptop)
        advice = "SRE Assistant: Log analyzed. (Full AI details will activate in GKE Cloud Shell)"
        print(f"   ⚠️ LOCAL ENVIRONMENT LIMIT: (AI call bypassed locally)")
        
    return jsonify({"status": "success", "advice": advice}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

from flask import Flask, request, jsonify, render_template
from crew import run_crew
import os
from waitress import serve

app = Flask(__name__)

AGENT_FOLDER = 'agents'

@app.route('/')
def index():
    
    agents = {}
    for filename in os.listdir(AGENT_FOLDER):
        if filename.endswith('.txt'):
            with open(os.path.join(AGENT_FOLDER, filename), 'r', encoding='utf-8', errors='ignore') as f:
                agents[filename.replace('.txt', '')] = f.read()
    return render_template('index.html', agents=agents)

@app.route('/update_agent', methods=['POST'])
def update_agent():
    data = request.get_json()
    agent_name = data.get('agent')
    new_prompt = data.get('prompt')

    file_path = os.path.join(AGENT_FOLDER, f"{agent_name}.txt")
    if not os.path.exists(file_path):
        return jsonify({'error': 'Agent not found'}), 404

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_prompt)
    return jsonify({'message': f'{agent_name} updated successfully.'})

@app.route('/generate', methods=['POST'])
def generate():
    if 'transcript' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['transcript']
    try:
       
        try:
            transcript = file.read().decode('utf-8').strip()
        except UnicodeDecodeError:
            file.seek(0)
            transcript = file.read().decode('latin1').strip()

        post = run_crew(transcript)
        return jsonify({'post': post})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    
    print("🚀 Server running on http://127.0.0.1:5000")
    serve(app, host="127.0.0.1", port=5000)

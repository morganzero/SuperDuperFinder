from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run')
def run_script():
    # Run the script and get the output
    result = subprocess.run(['python', 'dupefinder.py'], capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

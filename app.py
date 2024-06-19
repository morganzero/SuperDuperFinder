from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def run_script():
    process = subprocess.Popen(
        ['python', 'dupefinder.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    for stdout_line in iter(process.stdout.readline, ""):
        socketio.emit('new_output', {'data': stdout_line})
    process.stdout.close()
    process.wait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run')
def run():
    thread = threading.Thread(target=run_script)
    thread.start()
    return "Script started"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)

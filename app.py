from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import threading
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def run_script():
    process = subprocess.Popen(
        ['python', 'dupefinder.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    logging.info("Started dupefinder.py script")
    for stdout_line in iter(process.stdout.readline, ""):
        logging.info("Script output: %s", stdout_line.strip())
        socketio.emit('new_output', {'data': stdout_line})
        socketio.sleep(0)
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
    socketio.run(app, host='0.0.0.0', port=80)

import sys
import os
import subprocess
import http.server
import socketserver
import threading

PORT = int(os.environ.get('PORT') or 10270)

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')
        elif self.path == '/sub':
            try:
                with open("./sub.txt", 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Error reading file')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

httpd = socketserver.TCPServer(('', PORT), MyHandler)
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

# ⭐ 并行启动两个脚本
shell_command = """
chmod +x start.sh start1.sh
./start.sh &
./start1.sh &
wait
"""

try:
    subprocess.run(
        ['bash', '-c', shell_command],
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True,
        check=True
    )
    print("App is running")
except subprocess.CalledProcessError as e:
    print(f"Error: {e.returncode}")
    sys.exit(1)

# ⭐ 阻塞主进程，防止容器退出
server_thread.join()

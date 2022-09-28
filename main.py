import os
import urllib
import paramiko

from flask import Flask, render_template, request

URL_VUL_PY = 'https://raw.githubusercontent.com/vulmon/Vulmap/master/Vulmap-Linux/vulmap-linux.py'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/files', methods=['GET', 'POST'])
def list_files():
    ip = request.form['ip']
    username = request.form['username']
    password = request.form['password']
    paramiko_test(username, password, ip)
    files = os.listdir('stdout/')
    return render_template('files.html', files=files)

@app.route('/files/open', methods=['GET', 'POST'])
def openFile():
    path = os.path.dirname(os.path.realpath(__file__))
    filename = request.args.get('filename')
    url = 'file://' + path + '/stdout/' + filename
    file = urllib.request.urlopen(url)
    content = file.read().decode('utf-8')
    return '<pre>' +  content + '</pre>'

def paramiko_test(user, password, ip):
    ssh = paramiko.SSHClient()

    # Adding new host key to the local
    # HostKeys object(in case of missing)
    # AutoAddPolicy for missing host key to be set before connection setup.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ip, port=22, username=user,
                password=password, timeout=3)

    ssh.exec_command('wget -N '+URL_VUL_PY)
    ssh.exec_command('python3 -m venv .env')
    ssh.exec_command('source .env/bin/activate')
    ssh.exec_command('pip install requests')
    ssh.exec_command('sudo yum install nmap -y')

    if not os.path.exists("stdout"):
        os.makedirs("stdout")

    mes_test = {'nmap-os': f'sudo nmap -O {ip}',
                'nmap-vuln': f'sudo nmap -sV --script vuln {ip}',
                'vulmap': 'python vulmap-linux.py'
                }
    for name, command in mes_test.items():
        _, stdout,_ = ssh.exec_command(command)
        with open(f'stdout/{name}.txt', "wb+") as file:
            file.write(stdout.read())   

if __name__ == '__main__':
    app.run(host='0.0.0.0')

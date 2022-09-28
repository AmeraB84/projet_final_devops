import os
import sys
import urllib
import paramiko

from flask import Flask, render_template, request

url_vul_py = 'https://raw.githubusercontent.com/vulmon/Vulmap/master/Vulmap-Linux/vulmap-linux.py'
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
    content = file.read()
    return content

def paramiko_test(user, password, ip):
    print("Paramiko test")
    ssh = paramiko.SSHClient()

    # Adding new host key to the local
    # HostKeys object(in case of missing)
    # AutoAddPolicy for missing host key to be set before connection setup.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ip, port=22, username=user,
                password=password, timeout=3)
    print("ssh connected")

    ssh.exec_command('wget -N '+url_vul_py)
    ssh.exec_command('python3 -m venv .env')
    ssh.exec_command('source .env/bin/activate')
    ssh.exec_command('pip install requests')

    if not os.path.exists("stdout"):
        os.makedirs("stdout")
    
    _, stdoutO,_ = ssh.exec_command(f'sudo nmap -O {ip}')
    with open('stdout/nse-O.txt', "w+") as file:
        file.write(stdoutO.read().decode('utf-8'))   

    _, stdoutV,_ = ssh.exec_command(f'nmap -sV --script vuln {ip}')
    with open('stdout/nse-vuln.txt', "w+") as file:
        file.write(stdoutV.read().decode('utf-8'))   
    
    _, stdout, _ = ssh.exec_command('python vulmap-linux.py')

    with open('stdout/tmp.txt', "w+") as file:
        file.write(stdout.read().decode('utf-8'))

    with open('stdout/tmp.txt', "r", encoding='utf-8') as file:
        mon_fichier = file.read()
        print(mon_fichier)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

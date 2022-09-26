import sys
import codecs
import paramiko
import os

from getpass import getpass

url_vul_py = 'https://raw.githubusercontent.com/vulmon/Vulmap/master/Vulmap-Linux/vulmap-linux.py'

def demande_identifiants():
    passwd = None

    user_name = input("Saisir le nom d'utilisateur : ")

    if user_name:
        passwd = getpass("Saisir le mot de passe : ")
    ip_address = input("Saisir l'IP : ")

    return user_name, passwd, ip_address


def paramiko_test(user, password, ip):
    ssh = paramiko.SSHClient()

    # Adding new host key to the local
    # HostKeys object(in case of missing)
    # AutoAddPolicy for missing host key to be set before connection setup.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ip, port=22, username=user,
                password=password, timeout=3)
    

    ssh.exec_command('wget -N '+url_vul_py)
    ssh.exec_command('python3 -m venv .env')
    ssh.exec_command('source .env/bin/activate')
    ssh.exec_command('pip install requests')

    if not os.path.exists("stdout"):
        os.makedirs("stdout")
    
    _, stdoutO,_ = ssh.exec_command(f'sudo nmap -O {ip}')
    with open('stdout/nse-O.txt', "w") as file:
        file.write(stdoutO.read().decode('utf-8'))   

    _, stdoutV,_ = ssh.exec_command(f'nmap -sV --script vuln {ip}')
    with open('stdout/nse-vuln.txt', "w") as file:
        file.write(stdoutV.read().decode('utf-8'))   
    
    _, stdout, _ = ssh.exec_command('python vulmap-linux.py')
    print(dir(stdout))
    print(stdout.readable())

    with open('stdout/tmp.txt', "wb") as file:
        file.write(stdout.read())

    with open('stdout/tmp.txt', "r", encoding='utf-8') as file:
        mon_fichier = file.read()
        print(mon_fichier)

if __name__ == '__main__':
    # user, password, ip = demande_identifiants()
    _, user, password, ip = sys.argv

    paramiko_test(user, password, ip)
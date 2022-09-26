import paramiko

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
    

    _, stdout, _ = ssh.exec_command('wget -N '+url_vul_py)
    _, stdout, _ = ssh.exec_command('python3 -m venv .env')
    _, stdout, _ = ssh.exec_command('source .env/bin/activate')
    _, stdout, _ = ssh.exec_command('pip install requests')
    #_, stdout, _ = ssh.exec_command('ls')
    _, stdout, se = ssh.exec_command('python vulmap-linux.py')
    
    cmd_output = stdout.read()
    print('log stdout: ', cmd_output)
    print('log stderr: ', se.read())

    #with open('tmp.txt', "a") as file:
    #    file.write(str(cmd_output)+'\n')

if __name__ == '__main__':
    # user, password, ip = demande_identifiants()

    user = 'ec2-user'
    password = 'Floride5623'
    ip = '18.133.236.161'

    paramiko_test(user, password, ip)
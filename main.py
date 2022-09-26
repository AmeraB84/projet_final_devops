from getpass import getpass

def demande_identifiants():
    passwd = None

    user_name = input("Saisir le nom d'utilisateur : ")

    if user_name:
        passwd = getpass("Saisir le mot de passe : ")
    ip_address = input("Saisir l'IP : ")

    return user_name, passwd, ip_address

if __name__ == '__main__':
    user, password, ip = demande_identifiants()

    print(f'{user.__repr__()}:{password},{ip}')
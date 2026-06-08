import webbrowser
import configparser
import os
import shutil
import ftplib
import time

def optionselect():
    # Options selectable via the program
    option = int(input("1. Import Search Engine 2. Load search engine(s) 3.Exit 4. Generate script folder 5. FTP Mode "))
    if option == 1:
        inimport()
        os.system('cls' if os.name == 'nt' else 'clear')

    if option == 2:
        iniload()
        os.system('cls' if os.name == 'nt' else 'clear')
    if option == 3:
        exit(0)

    if option == 4:
        inital_setup()
        os.system('cls' if os.name == 'nt' else 'clear')
    if option == 5:
        ftp_mode()
        os.system('cls' if os.name == 'nt' else 'clear')


def inital_setup():
    # Using the OS library this function creates a folder named Scripts
    print("making a Scirpts folder...")
    os.makedirs("Scripts", exist_ok=True)
    print("Folder has been made")
    optionselect()

def inimport():
    path = str(input("Please enter the path to the INI file that contains the information or type back to go back: "))
    extension = ".ini"
    if path == "back":
        optionselect()
    if extension not in path:
        print("Error no ini file specified")
        inimport()
    shutil.move(path, "Scripts")
    optionselect()


def iniload():

    engine_choice = str(input("Chose the ini files you have saved WITHOUT THE ini extension: "))
    extension = ".ini"
    path = "Scripts/"
    file = path + engine_choice + extension
    config = configparser.ConfigParser()
    config.read(file)

    url = config['MAIN']['url']
    site_name = config['META']['name']
    site_name_char_count = len(site_name)
    if site_name_char_count >= 50:
        ovrrid = bool(input("ERROR SITE NAME IS LONGER THAN 50 CHARACTERS DO YOU WANT TO OVERRIDE THIS Y/N "))
        if ovrrid == ['y', 'Y']:
            return True
        if ovrrid == ['N''n']:
            return False
        if ovrrid:
            spacer_char = config['MAIN']['space_formatting']
            base_query = input(f"What do you want to search on {site_name}? ")
            formatted_query = base_query.replace(" ", spacer_char)
            webbrowser.open(url + formatted_query)
        if not ovrrid:
            exit(12)

    spacer_char = config['MAIN']['space_formatting']

    base_query = input(f"What do you want to search on {site_name}? ")

    formatted_query = base_query.replace(" ", spacer_char)

    webbrowser.open(url + formatted_query)

def ftp_mode():
    os.system('cls' if os.name == 'nt' else 'clear')
    options = int(input('1. Import FTP Server 2. Load FTP Server 3. Go Back '))

    if options == 1:
        inimport()
    if options == 2:
        load_ftp()
    if options == 3:
        optionselect()

def load_ftp():
    os.system('cls' if os.name == 'nt' else 'clear')
    file = str(input('Please enter the INI file with the FTP information '))
    folder = 'Scripts/'
    file_path = folder + file
    config = configparser.ConfigParser()
    config.read(file_path)
    # Reads the INI file to find the hostname and the port the username and password
    url = config['MAIN']['url']
    port = config['MAIN']['port']
    username = config['AUTH']['user']
    password = config['AUTH']['password']
    # Uses the ftplib libraries to connect and login to ftp servers
    ftp = ftplib.FTP()
    ftp.connect( host=url, port=int(port))
    ftp.login(user=username, passwd=password)


    ftp_server_options = int(input('1. List files 2. Upload Files 3. Retrive Files 4. Disconnect '))

    if ftp_server_options == 1:
        ftp.dir()
        ftp.quit()
        input("\nPress Enter to close the program...")
    if ftp_server_options == 2:
        source = str(input('Please enter the path to the file you want to upload: '))
        ftp.dir()
        target = str(input('Enter the target folder name EXACTLY as it appears above: '))
        ftp.cwd(target)
        clean_filename = os.path.basename(source)
        with open(source, 'rb') as local_file:
            ftp.storbinary('STOR ' + clean_filename, local_file)

    if ftp_server_options == 3:
        target_folder = str(input('Please enter the folder name on the server where the file is located: '))
        ftp.cwd(target_folder)
        ftp.dir()
        source_file = str(input('Please enter the exact name of the file you want to download: '))
        clean_local_name = os.path.basename(source_file)
        with open(clean_local_name, 'wb') as local_file:
            ftp.retrbinary('RETR ' + source_file, local_file.write)
        print(f"Successfully downloaded {source_file} to your computer as {clean_local_name}!")
    if ftp_server_options == 4:
        print('Disconnecting...')
        ftp.close()
        question = str(input('Do you want to go back to the Menu or Exit '))
        if question == 'Menu':
            optionselect()
        if question == 'Exit':
            exit(0)



optionselect()

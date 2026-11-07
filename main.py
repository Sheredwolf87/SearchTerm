import webbrowser
import configparser
import os
import shutil



def optionselect():
    option = int(input("1. Import Search Engine 2. Load search engine(s) 3.Exit 4. Generate script folder "))
    if option == 1:
        inimport()

    if option == 2:
        iniload()

    if option == 3:
        exit(0)

    if option == 4:
        inital_setup()


def inital_setup():
    print("making a Scirpts folder...")
    os.makedirs("Scripts", exist_ok=True)
    print("Folder has been made")
    optionselect()

def inimport():
    path = str(input("Please enter the path to the INI file that contains the search engine data or type back to go back: "))
    extension = ".ini"
    if path == "back":
        optionselect()
    if extension not in path:
        print("Error no ini file specified")
        inimport()
    shutil.move(path, "Scripts")
    optionselect()


def iniload():
    choice = str(input("Chose the ini files you have saved WITHOUT THE ini extension: "))
    extension = ".ini"
    path = "Scripts/"
    file = path + choice + extension

    config = configparser.ConfigParser()
    config.read(file)

    url = config['MAIN']['url']
    site_name = config['META']['name']
    site_name_char_count = len(site_name)
    if site_name_char_count >= 50:
        ovrrid = bool(input("ERROR SITE NAME IS LONGER THAN 50 CHARACTERS DO YOU WANT TO OVERRIDE THIS Y/N"))
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


optionselect()

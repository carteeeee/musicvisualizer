from colorama import Fore, Back, Style
import os
print(Style.DIM+"`"+Style.RESET_ALL+Fore.MAGENTA+"pip3"+Style.RESET_ALL+Fore.BLUE+Style.BRIGHT+" install -r requirements.txt"+Style.RESET_ALL+Style.DIM+"`"+Style.BRIGHT)
os.system("pip3 install -r requirements.txt")
print(Style.RESET_ALL+Style.BRIGHT+Fore.CYAN+"You're all good to go!"+Style.RESET_ALL)

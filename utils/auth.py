import getpass
from colorama import Fore, Style
from models.user import User

class Auth:
    @staticmethod
    def login():
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}           LMS LOGIN SYSTEM")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        user_id = input(f"{Fore.GREEN}Enter 6-digit ID: {Style.RESET_ALL}")
        # Use input() instead of getpass.getpass() for compatibility
        password = input(f"{Fore.GREEN}Enter Password: {Style.RESET_ALL}")
        
        if len(user_id) != 6 or not user_id.isdigit():
            print(f"{Fore.RED}Invalid ID format!{Style.RESET_ALL}")
            return None
            
        user = User.authenticate(user_id, password)
        if user:
            print(f"{Fore.GREEN}Login successful! Welcome {user['name']}{Style.RESET_ALL}")
            return user
        else:
            print(f"{Fore.RED}Invalid credentials!{Style.RESET_ALL}")
            return None
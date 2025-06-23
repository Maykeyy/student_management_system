import os
import sys
from colorama import init, Fore, Style
from database import db
from utils import Auth, Display
from portals import AdminPortal, TeacherPortal, StudentPortal

def main():
    init(autoreset=True)
    
    if not db.connect():
        print(f"{Fore.RED}Database connection failed!{Style.RESET_ALL}")
        sys.exit(1)
    
    display = Display()
    
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            user = Auth.login()
            
            if user:
                if user['role'] == 'admin':
                    portal = AdminPortal(user)
                elif user['role'] == 'teacher':
                    portal = TeacherPortal(user)
                elif user['role'] == 'student':
                    portal = StudentPortal(user)
                
                portal.show_menu()
            
            if input(f"\n{Fore.YELLOW}Login again? (y/n): {Style.RESET_ALL}").lower() != 'y':
                break
                
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
from colorama import Fore, Style

class Display:
    @staticmethod
    def header(title):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}{title.center(60)}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    @staticmethod
    def menu(options):
        print(f"\n{Fore.MAGENTA}Choose an option:{Style.RESET_ALL}")
        for i, option in enumerate(options, 1):
            print(f"{Fore.WHITE}{i}. {option}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}0. Exit{Style.RESET_ALL}")

    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

    @staticmethod
    def error(message):
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

    @staticmethod
    def info(message):
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")

    @staticmethod
    def table_header(headers):
        print(f"\n{Fore.YELLOW}{' | '.join(f'{h:^15}' for h in headers)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*15*len(headers)}{Style.RESET_ALL}")

    @staticmethod
    def table_row(data):
        print(f"{Fore.WHITE}{' | '.join(f'{str(d):^15}' for d in data)}{Style.RESET_ALL}")
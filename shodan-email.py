import requests
import re
import os
from bs4 import BeautifulSoup
from colorama import Fore, Style

class color:
    RED = Fore.RED + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Fore.RESET + Style.RESET_ALL

url = 'https://www.shodan.io/search?query='
ip_api = 'https://api.techniknews.net/ipgeo/'

def error(text):
    print(color.WHITE + '\n[*] Error: ' + color.WHITE + text)
    main()

def main():
    query = input(color.WHITE + '[*] Enter the query to search: ')
    if not '@' in query:
        error('No email detected')

    res = requests.get(str(url + query))
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    with open('results.txt', 'a') as file:  
        result_divs = soup.find_all('div', class_='result')
        
        if result_divs:
            for div in result_divs:
                ip_element = div.find('pre')
                if ip_element:
                    file.write(f'Result Data:\n{ip_element.text}\n')
                
                ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                ip_text = div.get_text()
                result = re.search(ip_pattern, ip_text)

                if result:
                    address = result.group(0)
                    file.write(f'IP found: {address}\n')
                    file.write(f'Result: {div.text.strip()}\n')
                    file.write('-' * 50 + '\n')  

                    res = requests.get(str(ip_api + address))
                    headers = res.headers
                    
                    for key, value in headers.items():
                        file.write(f'{key}: {value}\n') 
                    
                    file.write('\n' + '=' * 50 + '\n')  # Separador entre resultados
        else:
            file.write('No results found.\n')
            error('No results found.')

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else: 
        os.system('clear')

def print_title():
    clear()
    title = '''
███████╗██╗  ██╗ ██████╗ ██████╗  █████╗ ███╗   ██╗
██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗████╗  ██║
███████╗███████║██║   ██║██║  ██║███████║██╔██╗ ██║
╚════██║██╔══██║██║   ██║██║  ██║██╔══██║██║╚██╗██║
███████║██║  ██║╚██████╔╝██████╔╝██║  ██║██║ ╚████║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
'''
    print(color.RED + title)

if __name__ == '__main__':
    print_title()
    main()

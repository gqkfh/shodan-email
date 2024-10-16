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
    div_with_class = soup.find('div', class_='columns ten')

    with open('results.txt', 'a') as file:  
        if div_with_class:
            desired_elements = div_with_class.find_all('pre')
            for desired_element in desired_elements:
                file.write(desired_element.text + '\n')  

        link_elements = soup.find_all('a', class_='title text-dark')
        if link_elements:
            for link_element in link_elements:
                ip_text = link_element.text
                
                ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                result = re.search(ip_pattern, ip_text)

                if result:
                    address = result.group(0)
                    file.write(f'IP found: {address}\n') 
                    file.write('-' * 50 + '\n')  

                    res = requests.get(str(ip_api + address))
                    headers = res.headers
                    
                    for key, value in headers.items():
                        file.write(f'{key}: {value}\n') 
                    
                    file.write('\n') 

        else:
            file.write('Failure Getting the element')
            error('Failure getting the element')

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

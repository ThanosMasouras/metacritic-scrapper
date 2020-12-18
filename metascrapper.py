import requests
from requests_html import HTMLSession
import datetime
from datetime import datetime
import termcolor
from termcolor import colored


def call_url(url):
    
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except:
        print("error : callURL")

def time_string():

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    return str(current_time)

        

def get_texts_from_all_pages(url, selector):
    
    i = 0
    all_text_table = []
    while (if_empty_page(url+str(i)) == False):

        
        
        all_text_table = all_text_table + get_texts_from_selector(url+str(i), selector)
        i = i+1

    return all_text_table 


def if_empty_page(url):
    
    elements_table = []
    
    response = call_url(url)
    elements_table = response.html.find('.title_bump')
    return ("No games found" in elements_table[0].text)
        
    
def get_texts_from_selector(url, selector):
    
    texts_table = []    
    elements_table = []
    
    response = call_url(url)
    elements_table = response.html.find(selector)

    for element in elements_table:
        texts_table.append(element.text)
        
    #print("###Operation : get_texts_from_selector for the selector : " + selector) 
    return texts_table       


def get_text_from_first_selector(url , selector):
    
    elements_table = []
    response = call_url(url)
    elements_table = response.html.find(selector)
    #print(elements_table[0].text)   
    return(elements_table[0].text)
    
        

class Game:
    def __init__(self, name, releaseDate, platform, summary,developer, metaScore, userScore, gameUrl):
        self.name = name
        self.releaseDate = releaseDate
        self.platform = platform
        self.summary = summary
        self.developer = developer
        self.metaScore = metaScore
        self.userScore = userScore
        self.gameUrl = gameUrl
        
    def getGameDetails(self):
    
        response = call_url(self.gameUrl)

        names_list = response.html.find('a.hover_none > h1')
        self.name = names_list[0].text
        
        releaseDate_list = response.html.find("li.summary_detail.release_data > span.data")
        self.releaseDate = releaseDate_list[0].text
        
        platform_list = response.html.find("span.platform > a")
        self.platform = platform_list[0].text
        
      
        self.summary = find_summary(self.gameUrl)
        developer_list = response.html.find("li.summary_detail.developer > span.data")
        self.developer = developer_list[0].text
        self.metaScore = find_meta_score(self.gameUrl)
        self.userScore = find_user_score(self.gameUrl)

    def getGameName(self):

        return self.name
    
    def getGamePlatform(self):

        return self.platform

        
        
    
    def print_Details(self):
        print("Name: " + self.name)
        print("ReleaseDate: " + self.releaseDate)
        print("Platform: " + self.platform)
        print("Summary: " + self.summary)
        print("Developer: " + self.developer)
        print("Metascore: " + self.metaScore)
        print("Userscore: " + self.userScore)
        
        
def find_summary(gameUrl) :
        try:
            f_summary = get_text_from_first_selector(gameUrl , "span.data > span.inline_expand_collapse.inline_collapsed > span.blurb.blurb_expanded")
            
        except:
            f_summary = get_text_from_first_selector(gameUrl , "span.data > span")
            
        return f_summary
    

def find_meta_score(gameUrl) :
            
        try:
             f_meta_score = get_text_from_first_selector(gameUrl , "div.metascore_w.xlarge.game.positive > span")
                
        except:
            try:
                
                f_meta_score = get_text_from_first_selector(gameUrl , "div.metascore_w.xlarge.game.mixed > span")
                
            except:
                
                 f_meta_score = get_text_from_first_selector(gameUrl , "div.metascore_w.xlarge.game.negative > span")
                    
        return f_meta_score

    
    
def find_user_score(gameUrl):
    
        try:
            f_user_score = get_text_from_first_selector(gameUrl ,"a > div.metascore_w.user.large.game.mixed")
        except:
            try:
                f_user_score = get_text_from_first_selector(gameUrl ,"a > div.metascore_w.user.large.game.positive")
            except:
                try:
                    f_user_score = get_text_from_first_selector(gameUrl ,"a > div.metascore_w.user.large.game.negative")
                except:
                    f_user_score = get_text_from_first_selector(gameUrl ,"a > div.metascore_w.user.large.game.tbd")
                
                
        return f_user_score 

    

    
    


def get_game_url(name, platform):
    
    url = (platform).lower() +'/'+ (name).lower()
    
    url = url.replace("'", "")
    url = url.replace("#", "")
    url = url.replace("[", "")
    url = url.replace("]", "")
    url = url.replace(",", "")
    url = url.replace(":", "")
    url = url.replace(" & ","-")
    url = url.replace(" / ","-")
    url = url.replace(".","")
    url = url.replace(" - ", "---")
    url = url.replace(" ", "-")

    return "https://www.metacritic.com/game/"+url


def get_games_from_one_page(urlList):

        games_title = get_texts_from_selector(urlList, "a.title > h3")
        games_platform = get_texts_from_selector(urlList, 'div.platform > span.data')
        obj_games = []
        for i in range(0,10):
            try:
                url_game = get_game_url(games_title[i], games_platform[i])
                print(url_game)
                obj = Game(None, None, None, None, None, None, None, url_game)
                obj.getGameDetails()
                obj_games.append(obj)
            except:
                   pass
        return obj_games
    
    
def get_games_from_all_pages(urlList):

        print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'SCANNING GAMES FROM THE LIST' ' :: ' + colored('WAITING', 'yellow'))
        print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'THERE ARE ' + get_number_of_pages(urlList) + ' PAGES TO SCAN' ' :: ' + colored('WAITING', 'yellow'))
        games_title = get_texts_from_all_pages(urlList, "a.title > h3")
        games_platform = get_texts_from_all_pages(urlList, 'div.platform > span.data')
        print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'SCANNING GAMES FROM THE LIST' ' :: ' + colored('COMPLETED', 'green'))
        obj_games = []
        print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
        for i in range(0,len(games_title)):
            try:
                url_game = get_game_url(games_title[i], games_platform[i])
                #print(url_game)
                
                obj = Game(None, None, None, None, None, None, None, url_game)
                obj.getGameDetails()
                print('['+ time_string() + ']' + colored(' GAME ', 'magenta') + ':: ' '['+ obj.getGamePlatform() + '] ' + obj.getGameName() + ' :: ' + colored('SCANNED', 'green'))
                #obj.print_Details()
                
                obj_games.append(obj)
            except:
                print('['+ time_string() + ']' + colored(' GAME ', 'magenta') + ':: ' + "URL didnt reach" + ' :: ' + colored('ERROR', 'red'))
                pass
                   
              
        return obj_games

def get_number_of_pages(urlList):

    x = get_text_from_first_selector(urlList, ' li.page.last_page > a.page_num')
    return x




import json

def save_games_to_json(obj_games, filename):
    
    gamesDB = []
    for i in range(len(obj_games)):
        
        game_data = {}
        game_data["full_name"] = obj_games[i].name
        game_data["release_date"] = obj_games[i].releaseDate
        game_data["platform"] = obj_games[i].platform
        game_data["developer"] = obj_games[i].developer
        game_data["meta_score"] = obj_games[i].metaScore
        game_data["user_score"] = obj_games[i].userScore
        game_data["url"] = obj_games[i].gameUrl
        gamesDB.append(game_data)
        
    with open(filename + ".json", "w") as f:
        json.dump(gamesDB, f)

def load_games_from_json(filename):
    
    json_data = []
    try:
        with open(filename +".json") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = []
    return json_data



def menu():
    print("""\
                    _                  _ _   _          ____                                       
    _ __ ___   ___| |_ __ _  ___ _ __(_) |_(_) ___    / ___|  ___ _ __ __ _ _ __  _ __   ___ _ __ 
    | '_ ` _ \ / _ \ __/ _` |/ __| '__| | __| |/ __|   \___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__|
    | | | | | |  __/ || (_| | (__| |  | | |_| | (__     ___) | (__| | | (_| | |_) | |_) |  __/ |   
    |_| |_| |_|\___|\__\__,_|\___|_|  |_|\__|_|\___|___|____/ \___|_|  \__,_| .__/| .__/ \___|_|   
                                                |_____|                   |_|   |_|                       
    """)
    print("I always wanted to print something like this\n")

    print("Choose platform?")
    print("[1] PS4")
    print("[2] PS5")
    print("[3] XBOX ONE")
    print("[4] XBOX SERIES X/S")
    print("[5] SWITCH")
    print("[6] PC")
    print("[7] ALL")

    option = int(input("Enter your option: "))
    print("\n")
    while option != 0:
        if option == 1 :
            print("PS4 Submenu")
            print("[1] New Releases")
            print("[2] Comming Soon")
            print("[3] Best games this year")
            print("[4] All PS4 Games")
            print("[5] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")
            while option != 0:
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'NEW RELEASES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/new-releases/ps4/date?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'COMMING SOON - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/coming-soon/ps4/date?page=')
                    print(y[1])
                elif option1 == 3:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/ps4/filtered?page=')
                    print(y[1])
                elif option1 == 4:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'ALL PS4 GAMES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/available/ps4/metascore?page=')
                elif option1 == 5:
                    exit()
        elif option == 2 :
            print("PS5 Submenu")
            print("[1] New Releases")
            print("[2] Comming Soon")
            print("[3] Best games this year")
            print("[4] All PS5 Games")
            print("[5] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")

            while option != 0:
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'NEW RELEASES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/new-releases/ps5/date?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'COMMING SOON - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/coming-soon/ps5/date?page=')
                    print(y[1])
                elif option1 == 3:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/ps5/filtered?page=')
                    print(y[1])
                elif option1 == 4:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'ALL PS5 GAMES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/available/PS5/metascore?page=')
                elif option1 == 5:
                    exit()
        elif option == 3 :
            print("XBOXONE Submenu")
            print("[1] New Releases")
            print("[2] Comming Soon")
            print("[4] All Xbox One Games")
            print("[5] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")
            while option != 0:
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'NEW RELEASES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/new-releases/xboxone/date?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'COMMING SOON - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/coming-soon/xboxone/date?page=')
                    print(y[1])
                elif option1 == 3:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/xboxone/filtered?page=')
                    print(y[1])
                elif option1 == 4:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'ALL XBOX ONE GAMES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/available/xboxone/metascore?page=')
                elif option1 == 5:
                    exit()
        elif option == 4 :
            print("XBOX SERIES X/S Submenu")
            print("[1] New Releases")
            print("[2] Comming Soon")
            print("[3] Best games this year")
            print("[4] All Xbox Series X/S Games")
            print("[5] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")
            while option != 0:
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'NEW RELEASES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/new-releases/xbox-series-x/date?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'COMMING SOON - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/coming-soon/xbox-series-x/date?page=')
                    print(y[1])
                elif option1 == 3:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/xbox-series-x/filtered?page=')
                    print(y[1])
                elif option1 == 4:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'ALL XBOX SERIES X/S GAMES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/available/xbox-series-x/metascore?page=')
                elif option1 == 5:
                    exit()

        elif option == 5 :
            print("SWITCH Submenu")
            print("[1] New Releases")
            print("[2] Comming Soon")
            print("[3] Best games this year")
            print("[4] All Switch Games")
            print("[5] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")
            while option != 0:
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'NEW RELEASES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/new-releases/switch/date?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'COMMING SOON - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/coming-soon/switch/date?page=')
                    print(y[1])
                elif option1 == 3:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/switch/filtered?page=')
                    print(y[1])
                elif option1 == 4:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'ALL SWITCH GAMES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/available/switch/metascore?page=')
                elif option1 == 5:
                    exit()
        elif option == 6 :
            print("PC Submenu")
            print("[1] New Releases")
            print("[2] Comming Soon")
            print("[3] Best games this year")
            print("[4] All PC Games")
            print("[5] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")
            while option != 0:
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'NEW RELEASES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/new-releases/pc/date?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'COMMING SOON - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/coming-soon/pc/date?page=')
                    print(y[1])
                elif option1 == 3:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/pc/filtered?page=')
                    print(y[1])
                elif option1 == 4:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'ALL PC GAMES - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/release-date/available/PC/metascore?page=')
                elif option1 == 5:
                    exit()
        elif option == 7 :
            print("ALL Submenu")
            print("[1] Best Games of all time")
            print("[2] Best Games this Year")
            print("[3] Exit\n")

            option1 = int(input("Enter your option: "))
            print("\n")
            while option != 0:
                
                if option1 == 1:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES ALL TIME - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=')
                    print(y[1])
                elif option1 == 2:
                    print('['+ time_string() + ']' + colored(' info ', 'green') + ':: ' + 'BEST GAMES THIS YEAR - GETTING GAME DETAILS' ' :: ' + colored('WAITING', 'yellow'))
                    y = get_games_from_all_pages('https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?page=')
                    print(y[1])
                elif option1 == 3:
                    exit()
        else:
            print("invalid option")

        option = int(input("Enter your option: \n"))


menu()
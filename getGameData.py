import requests
from game import Game
from goal import Goal
from penalty import Penalty
import os
from bs4 import BeautifulSoup

"""
Retrieve the game data from the NHL website using the API
"""

class GetGameData:

    def game_retrieval(self, retrieval_type:str, url:str = 'none'):
        self.retrieval_type = retrieval_type
        self.url = url

        # If file path provided then, open the game page and scan it
        if self.retrieval_type == 'file':
            with open(url) as game_page:
                print(url)
                return self.scan_game_page(game_page)

        elif self.retrieval_type == 'website':
            # specify the url
            game_page = url

            page = requests.get(game_page)

            return self.scan_game_page(game_page)

        elif self.retrieval_type == 'folder':
            for filename in os.listdir(url):
                with open(os.path.join(url, filename)) as game_page:
                    return self.scan_game_page(game_page)
        
        

    # return the number of seconds that have elapsed at the start of a period
    # ie 0 for period 1, 1200 for period 2...
    # will calculate the over time periods up to 9
    def find_period_start(self, header:str):
        print('Period ' + header[0])

        period = 0
        overtime = 0        # Seconds to add if overtime (playoffs)
        multiplier = 1200   # Seconds per period
        
        # Don't process shootout
        if 'Shootout' in header:
            return -2
        
        elif 'OT' in header:
            overtime = 3600
        
        elif 'Period' in header:
            period = int(header[0]) 

        else:
            return -1           # Error

        return ((period - 1) * multiplier + overtime)
        
    # Convert the score clock to seconds for easier calulations
    def convert_score_clock_to_seconds(self, time:str):
        m, s = time.split(':')
        return int(m) * 60 + int(s) 

    # Scan the game page
    def scan_game_page(self, game_page):

        soup = BeautifulSoup(game_page, 'html.parser')

        scoring = soup.find(id='all_scoring')
        penalty = soup.find(id='all_penalty')

        period_start = 0
        
        # Scan through game information section
        # Get link, date, away, home
        link = soup.find('link', {'rel': 'canonical'}).get('href')

        date = soup.find('div', {'class': 'scorebox_meta'}).find_all('div')
        date = date[0].get_text().split(',')
        date = (date[0] + ', ' + date[1])

        # home and visitor done in steps to hopefully make it more readable
        visitor = soup.find(id='inner_nav').find('section').find_all('p')
        visitor = visitor[1].find('a').get('href')
        visitor = visitor.split('/')
        visitor = visitor[2]

        home = soup.find(id='inner_nav').find('section').find_all('p')
        home = home[2].find('a').get('href')
        home = home.split('/')
        home = home[2]

        #print(link + ' ' + date + ' ' + visitor + ' @ ' + home)

        # Create game
        game = Game(link, date, visitor, home)
        print(game)
        

        # Scan through the scoring section
        print('Goals')
        scoring_rows = scoring.find_all('tr')
        for row in scoring_rows:
            cells = row.find_all(['td', 'th'])

            # If row is a period header or not
            if (cells[0].name == 'th'):
                period_start = self.find_period_start(cells[0].get_text())

                print('period starts: ' + str(period_start))

                # Skip shootout data
                if period_start == -2:
                    print("Skipping Shootout")
                    break


                # Error check period_start
                if period_start == -1:
                    print("error with period")
                    exit()
                
            
            # else it should be a 'td' and be a goal summary
            # time | team | PP/SH | Goal Scorer | Assits
            else: 
                time = cells[0].get_text()
                seconds = self.convert_score_clock_to_seconds(time) + period_start

                team = cells[1].get_text()

                type = ''

                if 'PP' in cells[2].get_text():
                    type = 'PP'
                elif 'SH' in cells[2].get_text():
                    type = 'SH'

                player = cells[3].get_text().split('(')[0].strip('\n')
                
                goal_row = (str(seconds) + ', ' + team + ', ' + type + ', ' +
                    player)
                
                print(goal_row)
                game.goals.append(Goal(int(seconds), team, player, type))

        # Scan through the penalty section
        print('Penalties')
        period_start = 0
        penalty_rows = penalty.find_all('tr')
        for row in penalty_rows:
            cells = row.find_all(['td', 'th'])

            # If row is a period header or not
            if (cells[0].name == 'th'):
                period_start = self.find_period_start(cells[0].get_text())

                print('period starts: ' + str(period_start))

                # Error check period_start
                if period_start == -1:
                    print("error with period")
                    exit()

            # else it should be a 'td' and be a goal summary
            # time | team | player | infraction | duration
            else: 
                time = cells[0].get_text()
                seconds = self.convert_score_clock_to_seconds(time) + period_start

                team = cells[1].get_text()
                player = cells[2].get_text()
                infraction = cells[3].get_text()
                if cells[4].get_text().endswith('min'):
                    duration = int(cells[4].get_text().split(' ')[0]) * 60
                else:
                    duration = 0

                print (str(seconds) + ', ' + team + ', ' + player + ', '
                + infraction + ', ' + str(duration))

                game.penalties.append(Penalty(int(seconds), team, player, 
                infraction, duration))
        
        #print(game)
        return game

def main():
    '''
    # open local folder for testing
    dir_path = '/home/j/nhl_game_python/2019-2020'
    GetGameData('folder', dir_path)
    '''

    # open local file
    file_path = '/home/j/nhl_game_python/2019-2020/201910090BUF.html'
    get_game_data = GetGameData()
    get_game_data.game_retrieval('file', file_path)


if __name__ == "__main__":
    main()

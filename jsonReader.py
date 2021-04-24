import requests
from game import Game
import events
from stats import Team_Stats

"""
Scan through the JSON from the NHL website
Get the goals, penalties, and all the plays for a game

Can import the entire season of games and scan through each of them
"""

class JSON_Reader:

    ## Constants ##

    FIRST_HALF_OF_URL = 'https://statsapi.web.nhl.com'

    data: str

    def __init__(self):
        
        self.data = ''


    def get_url(self, url) :
        r = requests.get(url)
        self.data = r.json()
        
        
    def game_reader(self, url) -> Game:
        
        ## Work ##

        self.get_url(url)
        gameData = self.data['gameData']
        goalIds = self.data['liveData']['plays']['scoringPlays']
        penaltyIds = self.data['liveData']['plays']['penaltyPlays']
        allPlays = self.data['liveData']['plays']['allPlays']

        # Place all game information into variables for an easier time
        # building the game object
        gameId = self.data['gamePk']
        nhl_website_link = (self.FIRST_HALF_OF_URL + self.data['link'])
        date = (gameData['datetime']['dateTime'][0:10])
        away_team = gameData['teams']['away']['triCode']
        home_team = gameData['teams']['home']['triCode']


        # Print game information for testing
        print(nhl_website_link)
        print(gameId)
        print(date)
        print('away: ' + away_team)
        print('home: ' + home_team)


        # Get goal information
        # playId, period, periodTime, team, type
        goals : events.Goal = []   
        for goalId in goalIds:
            period = allPlays[goalId]['about']['period']
            periodTime = allPlays[goalId]['about']['periodTime']
            team = allPlays[goalId]['team']['triCode']
            type = allPlays[goalId]['result']['strength']['code']

            goals.append(events.Goal(goalId, period, periodTime, team, type))

        # Get penalty information
        # playId, period, periodTime, team, infraction, duration, type
        penalties: events.Penalty = []
        for penaltyId in penaltyIds:
            period = allPlays[penaltyId]['about']['period']
            periodTime = allPlays[penaltyId]['about']['periodTime']
            team = allPlays[penaltyId]['team']['triCode']
            infraction = allPlays[penaltyId]['result']['secondaryType']
            duration = allPlays[penaltyId]['result']['penaltyMinutes']
            type = allPlays[penaltyId]['result']['penaltySeverity']

            if duration == 2:
                penalties.append(events.minorPenalty(penaltyId, period,
                periodTime, team, infraction, duration, type))
            elif duration == 4:
                penalties.append(events.doubleMinorPenalty(penaltyId, period,
                periodTime, team, infraction, duration, type))
            elif duration == 5:
                penalties.append(events.majorPenalty(penaltyId, period,
                periodTime, team, infraction, duration, type))


        # Create the game object, and place in the game information
        game = Game(nhl_website_link, gameId, date, away_team, home_team,
            goals, penalties)

        # Print the game
        print(game)

        return game

    def season_reader(self, url):

        if (isinstance(url, int)):
            url = 'https://statsapi.web.nhl.com/api/v1/schedule?season=' + str(url)

        r = requests.get(url)

        seasonData = r.json()

        totalGames = seasonData['totalGames']
        print (totalGames)

        games = []

        for date in seasonData['dates']:
            gameDate = date['date']
            for game in date['games']:
                status = game['status']['detailedState']

                if status == 'Final':
                    gameLink = self.FIRST_HALF_OF_URL + game['link']
                    games.append(gameLink)

        return games

    def season_team_stats(self, url):

        statsToReturn = []
        
        teamName: str                   # teams, name
        abbreviation: str               # teams, abbreviation
        powerPlayGoals: int             # team, teamStats, 0, splits, 0, stat, powerPlayGoals
        powerPlayGoalsAgainst: int      # team, teamStats, 0, splits, 0, stat, powerPlayGoalsAgainst
        powerPlayOpportunities: int     # team, teamStats, 0, splits, 0, stat, powerPlayGoalOpportunities

        if isinstance(url, int):
            url = 'https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats&season=' + str(url)

        self.get_url(url)

        for team in self.data['teams']:
            teamName = team['name']
            abbreviation = team['abbreviation']

            stats = team['teamStats'][0]['splits'][0]['stat']
            powerPlayGoals = int(stats['powerPlayGoals'])
            powerPlayGoalsAgainst = int(stats['powerPlayGoalsAgainst'])
            powerPlayOpportunities = int(stats['powerPlayOpportunities'])

            statsToReturn.append(
                Team_Stats(teamName, abbreviation, powerPlayGoals, 
                powerPlayGoalsAgainst, powerPlayOpportunities)
            )

        return statsToReturn

def main():

    # 20192020 for shortend pandemic season
    # 20202021 for the full short pandemic season (current)
    season = 20192020
    game = 'https://statsapi.web.nhl.com/api/v1/game/2019030121/feed/live'
    seasonURL = 'https://statsapi.web.nhl.com/api/v1/schedule?season=' + str(season)
    season_stats = 'https://statsapi.web.nhl.com/api/v1/teams?expand=team.stats&season=' + str(season)
    jsonReader = JSON_Reader()

    #print(jsonReader.game_reader(game))

    print(jsonReader.season_reader(seasonURL))

    #print(jsonReader.season_team_stats(season_stats))

if __name__ == "__main__":
    main()

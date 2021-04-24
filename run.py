from game import Game
from penaltyChecker import PenaltyChecker
from doubleMinorFinder import DoubleMinorFinder
from latePPGCheck import LatePPGCheck
from jsonReader import JSON_Reader
from stats import Team_Stats
import events

"""
Change the season to change the season you want to run
TODO: setup a CLI to set the options to run a season (and set season)
or to runa  specific game (helpful for testing)
"""

season:int = 20192020

def main():

    reader = JSON_Reader()
    penaltyChecker = PenaltyChecker()
    latePPGchecker = LatePPGCheck()

    latePPGList = []

    # get the current PPG, PPGA stats for the season
    
    stats = reader.season_team_stats(season)
    print(stats)

    # get links for each game in the season

    gamesList = reader.season_reader(season)
    print (gamesList)

    for gameLink in gamesList:
        game = reader.game_reader(gameLink)

        # Check for coincidentals
        penaltyChecker.coincidentals(game)

        # Match PPG with penalties
        penaltyChecker.find_penalty_for_PPG(game)

        # Late PPG check
        latePPGchecker.check_goal(game)

        for latePPG in game.latePPgoals:
            latePPGList.append(latePPG)

            ppgPosition = index_of_team(stats, latePPG.team)

            if latePPG.team == game.home:
                ppgaPosition = index_of_team(stats, game.visitors)
            else:
                ppgaPosition = index_of_team(stats, game.home)

            stats[ppgPosition].adjustedPPG = stats[ppgPosition].adjustedPPG + 1
            stats[ppgaPosition].adjustedPPGA = stats[ppgaPosition].adjustedPPGA + 1

        print(stats)
	
    # Write out the late PPG to a csv
    f = open(str(season) + "_LatePPG.csv", 'w')
    print('-----------------')
    print('Late goals')
    print('-----------------')

    for latePPG in latePPGList:
        print(latePPG)
        f.write(str(latePPG))

    f.close()
	
    # Write out the stats to a csv
    f = open(str(season) + "_stats.csv", 'w')

    print('-----------------')
    print('Stats')
    print('-----------------')
    print(stats)
    f.write(str(stats))

    f.close()


# Get the index of the team
def index_of_team(stats, team):
    for i in range(0, len(stats)):
        if (team == stats[i].abbreviation):
            return i
    print('Looking for ' + team)

    exit('no team found in stats list')

if __name__ == "__main__":
    main()

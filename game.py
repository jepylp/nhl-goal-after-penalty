import events
from penalty import Penalty
from latePPgoal import LatePPgoal

"""
Game object to store the teams, date, goals, and penalties
"""

class Game:
    

    def __init__(self, url:str, gameId:int, date: str, visitors: str, 
        home: str, goals: events.Goal = [], penalties: events.Penalty = [] 
    ):
        self.url = url
        self.gameId = gameId
        self.date = date
        self.visitors = visitors
        self.home = home
        self.boxscore = 'https://www.nhl.com/gamecenter/'+ str(gameId) +'/recap/stats' 
        self.goals: events.Goal = goals
        self.penalties: events.Penalty = penalties
        self.latePPgoals: LatePPgoal = []

    def __repr__(self):
        strGoals = ''
        strPenalties = ''
        strLatePPG = ''

        for goal in self.goals:
            strGoals += (str(goal) + '\n')

        for penalty in self.penalties:
            strPenalties += (str(penalty) + '\n')

        for latePPG in self.latePPgoals:
            strLatePPG += (str(latePPG) + '\n')

        return (
            'URL: ' + self.url +
            ' gameId: ' + str(self.gameId) +
            ' Date: ' + self.date +
            ', Visitor: ' + self.visitors +
            ', Home: ' + self.home +
            '\nGoals: \n' + strGoals +
            '\nPenalties: \n' + strPenalties +
            '\nLate PP goals: \n' + strLatePPG
        )

def main():

    # Test Game Information
    game = Game('test', '2021-01-14', 'EXA', 'EXB')

    print('Game loaded: ')
    print(game)

if __name__ == "__main__":
    main()

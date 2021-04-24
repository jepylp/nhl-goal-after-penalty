# Store the team stats 
# TODO change to a dataclass

class Team_Stats:

    teamName: str                   # teams, name
    abbreviation: str               # teams, abbreviation
    powerPlayGoals: int             # teamStats, 0, splits, 0, stat, powerPlayGoals
    powerPlayGoalsAgainst: int      # teamStats, 0, splits, 0, stat, powerPlayGoalsAgainst
    powerPlayOpportunities: int     # teamStats, 0, splits, 0, stat, powerPlayGoalOpportunities
    adjustedPPG: int                # calculated
    adjustedPPGA: int               # calculated

    def __init__(self, 
        teamName: str,                   
        abbreviation: str,
        powerPlayGoals: int,             
        powerPlayGoalsAgainst: int,
        powerPlayOpportunities: int
    ):
        self.teamName = teamName   
        self.abbreviation = abbreviation
        self.powerPlayGoals = powerPlayGoals
        self.powerPlayGoalsAgainst = powerPlayGoalsAgainst
        self.powerPlayOpportunities = powerPlayOpportunities
        self.adjustedPPG = powerPlayGoals
        self.adjustedPPGA = powerPlayGoalsAgainst

    def __repr__(self):
        return(
            self.abbreviation + ' PPG: ' + str(self.powerPlayGoals) + 
            ' PPO: ' + str(self.powerPlayOpportunities) +
            ' PPGA: ' + str(self.powerPlayGoalsAgainst) +
            ' Adjusted PPG: ' + str(self.adjustedPPG) +
            ' Adjusted PPGA: '+ str(self.adjustedPPGA) +
            '\n'
        )

    

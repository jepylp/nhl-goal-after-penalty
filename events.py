## Super class for penalties, goals, and late Power Play Goals

class Event:

    SECONDS_PER_PERIOD = 1200

    playId: int
    period: int
    periodTime: str
    team: str
    time: int

    def __init__(self,
        playId: int,
        period: int,
        periodTime: str,
        team: str
    ) -> None:

        # Assign variables
        self.playId = playId
        self.period = period
        self.periodTime = periodTime
        self.team = team
        self.time = self.convert_periodTime_to_seconds()

    # Period, Time, Team, playId, seconds
    def __repr__(self):
        return(
            'Period: ' + str(self.period) +
            ', Time: ' + self.periodTime +
            ', Team: ' + self.team +
            ', playId: ' + str(self.playId) +
            ', seconds: ' + str(self.time) 
        )

    # Convert the periodTime to seconds to more easily compare event times
    def convert_periodTime_to_seconds(self) -> int:
        addedPeriodTime = (self.period - 1) * self.SECONDS_PER_PERIOD # Period in seconds
        
        # Period time is a string, split the minutes and seconds
        t = self.periodTime.split(':')
        minutes = int(t[0]) * 60
        seconds = int(t[1])

        # Add those minutes up and return it
        return (addedPeriodTime + minutes + seconds)


# Store the goals for a game
class Goal(Event):
    
    playId: int
    period: int
    periodTime: str
    team: str
    type: str

    def __init__(self, 
        playId: int,
        period: int,
        periodTime: str,
        team: str,
        type: str           # PPG, EVEN, SH, PS
    ) -> None:

        super().__init__(playId, period, periodTime, team)
        self.type = type
    
    # Period, Time, Team, playId, seconds, type 
    def __repr__(self):
        return (
            super().__repr__() +
            ', Type: ' + self.type 
        )
    
    # Return a string for csv file outputs
    def csv(self):
        return (
            str(self.period) +
            ',' + self.periodTime +
            ',' + self.team +
            ',' + str(self.playId) +
            ',' + str(self.time) +
            ',' + self.type
        )

# Penalty super class, coincidentals will be calculated after by comparing time,
# It's not a variable that is stored on the NHL API as far as I can tell.
class Penalty(Event):

    playId: int
    period: int
    periodTime: str
    team: str
    infraction: str
    duration: int
    type: str
    duration_seconds: int
    coincidental: bool

    def __init__(self,
        playId: int,
        period: int,
        periodTime: str,
        team: str,
        infraction: str,
        duration: int,
        type: str
    ):
        super().__init__(playId, period, periodTime, team)
        self.infraction = infraction
        self.duration = duration
        self.time = super().convert_periodTime_to_seconds()
        self.duration_seconds = self.duration * 60
        self.type = type
        self.coincidental = False

    # Period, Time, Team, playId, seconds, type
    def __repr__(self):
        return(
            super().__repr__() +
            ', type: ' + self.type +
            ', infraction: ' + self.infraction +
            ', duration: ' + str(self.duration) +
            ', coincidental: ' + str(self.coincidental)
        )

# minor penalties
class minorPenalty(Penalty):

    result: str

    def __init__(self,
        playId: int,
        period: int,
        periodTime: str,
        team: str,
        infraction: str,
        duration: int,
        type: str
    ):
        super().__init__(playId, period, periodTime, team, infraction, duration, type)
        self.result = ''

    def __repr__(self):
          
        return(super().__repr__() + ', result: ' + str(self.result))

# Double minor, Still need to confirm how a coincidental with a minor penalty
# will work.
class doubleMinorPenalty(Penalty):
    
    firstHalfResult: str
    secondHalfResult: str
    secondCoincidental: bool

    def __init__(self,
        playId: int,
        period: int,
        periodTime: str,
        team: str,
        infraction: str,
        duration: int,
        type: str
    ):
        super().__init__(playId, period, periodTime, team, infraction, duration, type)
        self.firstHalfResult = ''
        self.secondHalfResult = ''
        self.secondCoincidental = False

    def __repr__(self):
        return(super().__repr__() + 
            ', Second half coincidental: ' + str(self.secondCoincidental) +
            ', First half result: ' + str(self.firstHalfResult) +
            ', Second half result: ' + str(self.secondHalfResult) 
        )

# Major Penalty
class majorPenalty(Penalty):

    results:str = []

    def __init__(self,
        playId: int,
        period: int,
        periodTime: str,
        team: str,
        infraction: str,
        duration: int,
        type: str
    ):
        super().__init__(playId, period, periodTime, team, infraction, duration, type)
        self.results = []

    def __repr__(self):
        return(super().__repr__() + 
            ', results: ' + str(self.results)
        )

# A goal shortly after a penatly has expired
class LatePPgoal (Event):
    def __init__(self,
        playId: int,
        period: int,
        periodTime: str,
        gameId: int,
        team: str,
        url: str,
        gameDate: str,
        time: int,
        seconds_elapsed: int
    ):
        super().__init__(playId, period, periodTime, team)
        self.gameId = gameId
        self.url = url
        self.gameDate = gameDate
        self.time = time
        self.seconds_elapsed = seconds_elapsed

    def __repr__(self):
        return(
            'URL: ' + 'https://www.nhl.com/gamecenter/' + str(self.gameId) + '/recap/stats'
            ', Team: ' + str(self.team) +
            ', Period: ' + str(self.period) +
            ', Time: ' + str(self.periodTime) +
            ', Second(s) Elapsed: ' + str(self.seconds_elapsed)
        )
    # Return all the captured info
    def all_info(self) -> str:
        return (
            'playId: ' + str(self.playId) +
            ', period: ' + str(self.period) +
            ', periodTime: ' + str(self.periodTime) +
            ', gameId: ' + str(self.gameId) +
            ', team: ' + str(self.team) +
            ', url: ' + str(self.url) +
            ', gameDate: ' + str(self.gameDate) +
            ', time: ' + str(self.time) +
            ', seconds_elapsed: ' + str(self.seconds_elapsed)
        )
        
## For testing
def main():
    goal = Goal(1, 1, '01:02', 'AAA', 'EVEN')
    print(goal)

    minor = minorPenalty(2, 2, '14:53', 'AAA', 'Slashing', 2, 'minor')
    print(minor)

    double = doubleMinorPenalty(3, 2, '15:53', 'AAA', 'Slashing', 4, 'double')
    print(double)

    major = majorPenalty(4, 3, '17:53', 'AAA', 'Slashing', 5, 'major')
    print(major)

    late = LatePPgoal(1,1, '1:03', 2019020222, 'AAA', 'gameURL', '2011-01-01', 63, 1)
    print(late)

    print('all of late: \n' + late.all_info())

if __name__ == "__main__":
    main()

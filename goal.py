# Store goal information from game
from events import Event


class Goal(Event):
    def __init__(self, period: int, periodTime: str, team: str, player: str, type: str):
        self.period = period
        self.periodTime = periodTime # will be broken down with time convertion

        self.time = time
        self.team = team
        self.player = player
        self.type = type        # PPG, SH, EVEN

    def __repr__(self):
        return (
            'Time: ' + str(self.time) +
            ', Team: ' + self.team +
            ', Player: ' + self.player +
            ', Type: ' + self.type + '\n'
        )

def main():
    test_goal = Goal(321, 'CAL', 'bob missing', 'EV')
    print(test_goal)
    
if __name__ == "__main__":
    main()
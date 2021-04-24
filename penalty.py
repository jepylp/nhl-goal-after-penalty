# Store penalty information from game
class Penalty:

    def __init__(self, 
        time: int, 
        team: str, 
        player: str,
        infraction: str,
        duration: int,
        result = ''
    ):
        self.time = time
        self.team = team
        self.player = player
        self.infraction = infraction
        self.duration = duration
        self.result = result

    def __repr__(self):
        return (
            'Time: ' + str(self.time) +
            ', Team: ' + self.team +
            ', Player: ' + self.player +
            ', Infraction: ' + self.infraction +
            ', Duration: ' + str(self.duration) +
            ', Result: ' + str(self.result) + '\n'
        )

    ## Check if penalties are coincidental
    def coincidental(self, penalty) -> bool:
        
        if (self.time == penalty.time
        and self.team != penalty.team
        and self.duration == penalty.duration
        and penalty.result == ''
        and self.result == '') :
            return True
        else:
            return False

def main():
    test_penalty = Penalty(321, 'VAN', 'mike nobody', 'slashing', 120, 'expired')
    print(test_penalty)

if __name__ == "__main__":
    main()
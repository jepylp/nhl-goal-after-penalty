# Store late power play goal information

class LatePPgoal:
    def __init__(
        self,
        link: str,
        game_date: str,
        scoring_team: str,
        time_of_goal: int,
        seconds_elapsed: int
    ):
        self.link = link
        self.game_date = game_date
        self.scoring_team = scoring_team
        self.time_of_goal = time_of_goal
        self.seconds_elapsed = seconds_elapsed
        self.year: int
        self.month: int
        self.day: int

    def convert_seconds(self):
        minutes = int(self.time_of_goal / 60)
        period = int(minutes / 20) + 1
        seconds = self.time_of_goal % 60
        return(str(minutes).zfill(2) + ':' + str(seconds).zfill(2))

    def __repr__(self):
        return(
            'Link: ' + self.link +
            ', Date: ' + self.game_date +
            ', Team: ' + self.scoring_team +
            ', Time: ' + self.convert_seconds() +
            ', Second Elapsed: ' + str(self.seconds_elapsed) +
            ',' + self.year +
            ',' + self.month +
            ',' + self.day
        )

def main():
    test_latePPgoal = LatePPgoal('Link', '2019-09-01', 'EDM', 303, 1)
    print(test_latePPgoal)

    test_latePPgoal = LatePPgoal('Link', '2019-09-01', 'EDM', 627, 4)
    print(test_latePPgoal)

    test_latePPgoal = LatePPgoal('Link', '2019-09-01', 'EDM', 633, 4)
    print(test_latePPgoal)

    test_latePPgoal = LatePPgoal('Link', '2019-09-01', 'EDM', 1633, 2)
    print(test_latePPgoal)

if __name__ == "__main__":
    main()
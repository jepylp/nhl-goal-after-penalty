from game import Game
import events as e

# Check even strength goals to see if they are close enough to a penalty
class LatePPGCheck:
    
    def check_goal(self, game: Game):

        MAX_ELAPSED_TIME = 30

        timeElapsed = MAX_ELAPSED_TIME + 1 # Initialize with value higher than cut off 

        for goal in game.goals:

            # Only check 'EVEN' goals

                # Check each penalty
                for penalty in game.penalties:

                    timeElapsed = MAX_ELAPSED_TIME + 1

                    # Goal and penalty must be on different teams and must
                    # not be coincidental, true for all penalties
                    if (
                        (goal.type == 'EVEN') and
                        (goal.team != penalty.team) and 
                        (goal.time >= penalty.time)
                    ):
                        
                        # Minor penalty
                        if (
                            (penalty.duration == 2) and
                            not (penalty.coincidental)
                        ):
                            timeElapsed = self.minor_penalty_check(
                                goal, penalty)
                        
                        # Double minor penalty
                        elif (
                            (penalty.duration == 4)
                        ):   
                            timeElapsed = self.double_minor_penalty_check(
                                goal, penalty)
                        
                        # Major penalty
                        elif(
                            (penalty.duration == 5) and
                            not (penalty.coincidental)
                        ):
                            timeElapsed = self.major_penalty_check(
                                goal, penalty)

                    if (0 <= timeElapsed <= MAX_ELAPSED_TIME):
                        game = self.update_game(game, goal, penalty, timeElapsed)
                        if (penalty.duration == 2):
                            penalty.result = 'LatePPG'
                        elif (penalty.duration == 4):
                            penalty.secondHalfResult = 'LatePPG'
                        elif (penalty.duration == 5):
                            penalty.results.append('LatePPG')     
        return game

    # Check the minor penalty to make sure it hasn't been scored on,
    # Then return the elasped seconds from the penalty to the goal.
    def minor_penalty_check(self, goal: e.Goal, penalty: e.minorPenalty) -> int:
        if (
            (penalty.result == '') and
            (goal.time >= (penalty.time + penalty.duration_seconds))
        ):
            return (goal.time - (penalty.time + penalty.duration_seconds))
        else:
            return -1

    # Check the double minor penalty. If the second half contains a goal
    # then we know to skip the remaining checks. If a goal was scored in
    # the first half then set the start time for the second half for the 
    # time of the goal. Duration will then be 2 minutes from that goal.
    def double_minor_penalty_check(self, goal: e.Goal, penalty: e.doubleMinorPenalty) -> int:
        
        # Goal wasn't scored in the second half
        if (
            (penalty.secondHalfResult == '') and
            not (penalty.secondCoincidental) and
            (goal.team != penalty.team)
        ):
            # no goal in fist half
            if (
                (penalty.firstHalfResult == '') and
                (goal.time >= penalty.time + penalty.duration_seconds)
            ):
                return int(goal.time - (penalty.time + penalty.duration_seconds))
            
            # goal in first half
            elif (
                (penalty.firstHalfResult != '') and
                (goal.time >= penalty.firstHalfResult.time + penalty.duration_seconds / 2)
            ):
                penalty_second_half_start = penalty.firstHalfResult.time
                penalty_second_half_end = penalty_second_half_start + (penalty.duration_seconds / 2)
                if (goal.time >= penalty_second_half_end):
                    return int(goal.time - penalty_second_half_end)
            
            # first half is coincidental, there fore only 2 minutes
            elif (
                (penalty.coincidental) and
                (goal.time >= penalty.time + penalty.duration_seconds / 2)
            ):
                return int(goal.time - (penalty.time + penalty.duration_seconds / 2))

            else :
                return -1
        
        else:
            return -1
    
    # Major Penalty will nore expire if scored on so just check that the
    # goal time is later the penalty time and return the elapsed time 
    def major_penalty_check(self, goal: e.Goal, penalty: e.majorPenalty) -> int:
        if (
            (goal.time > penalty.time + penalty.duration_seconds)  
        ):
            return (goal.time - (penalty.time + penalty.duration_seconds))

    def update_game(self, game: Game, goal: e.Goal, penalty: e.Penalty, timeElapsed):
        # playId, period, periodTime, gameId, team, url:, gameDate,
        # time, seconds_elapsed
        late_PPG = e.LatePPgoal(
            goal.playId, goal.period, goal.periodTime, game.gameId,
            goal.team, game.url, game.date, goal.time, timeElapsed
        )
        game.latePPgoals.append(late_PPG)

        penalty.result = late_PPG


        return game
                

def main():
    late_PPG_check = LatePPGCheck()

    home = 'AAA'
    away = 'BBB'

    game = Game('url', 202, '2021-01-14', away, home)
    

    # Goals
    game.goals.append(e.Goal(1, 1, '01:30', home, 'EVEN'))  # A normal goal

    ## Goal checks
    game.penalties.append(e.minorPenalty(2, 1, '02:00', away, '3s', 2, 'Minor'))
    game.goals.append(e.Goal(3, 1, '04:03', home, 'EVEN'))
    game.goals.append(e.Goal(4, 1, '04:05', home, 'EVEN')) # Should be skipped

    game.penalties.append(e.minorPenalty(5, 1, '05:00', away, '30s', 2, 'Minor'))
    game.goals.append(e.Goal(6, 1, '07:30', home, 'EVEN'))

    game.penalties.append(e.doubleMinorPenalty(7, 1, '08:00', away, '4s', 4, 'Minor'))
    game.goals.append(e.Goal(8, 1, '12:04', home, 'EVEN'))

    # Goal in first half oh double minor
    game.penalties.append(e.doubleMinorPenalty(9, 1, '13:00', away, '5s', 4, 'Minor'))
    game.goals.append(e.Goal(10, 1, '14:00', home, 'PPG'))
    game.penalties[3].firstHalfResult = (e.Goal(10, 1, '14:00', home, 'PPG'))
    game.goals.append(e.Goal(11, 1, '16:05', home, 'EVEN'))

    # Major Penalty
    game.penalties.append(e.majorPenalty(12, 1, '17:00', away, '6s', 5, 'Major'))
    game.goals.append(e.Goal(13, 2, '2:06', home, 'EVEN'))

    # coincidental double minor
    game.penalties.append(e.doubleMinorPenalty(14, 2, '3:00', away, '7s', 4, 'Minor'))
    game.penalties.append(e.minorPenalty(15, 2, '03:00', away, 'coincidental', 2, 'Minor'))
    game.penalties[5].coincidental = True
    game.penalties[6].coincidental = True
    game.goals.append(e.Goal(16, 2, '05:07', home, 'EVEN'))

    # coincidental second half double minor (should be skipped)
    game.penalties.append(e.doubleMinorPenalty(17, 2, '08:00', away, 'skip', 4, 'Minor'))
    game.penalties[7].coincidental = True
    game.penalties[7].secondCoincidental = True
    game.goals.append(e.Goal(18, 2, '07:10', home, 'EVEN'))
    game.goals.append(e.Goal(19, 2, '08:10', home, 'EVEN'))
    game.goals.append(e.Goal(20, 2, '09:10', home, 'EVEN'))
    game.goals.append(e.Goal(21, 2, '10:10', home, 'EVEN'))


    print('Game before testing:')
    print(str(game))

    
    game = late_PPG_check.check_goal(game)

    print('Game after running though goal check')
    print(str(game))

    

if __name__ == "__main__":
    main()
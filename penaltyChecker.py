import events
from game import Game

"""
Check for coincidental penalties and match up PPG with the penalties they were scored on
"""
class PenaltyChecker:
    
    ## Scan penalties for what appears to be two coincidental penalties
    def coincidentals(self, game: Game) -> Game:
        
        # Loop through all penalties
        for i in range(len(game.penalties)):

            # coincidental should be False
            if (game.penalties[i].coincidental == False):

                # Only check minor and major penalties currently
                if (
                    (game.penalties[i].duration == 2) or
                    (game.penalties[i].duration == 4) or  
                    (game.penalties[i].duration == 5)
                ):
                    
                    # Loop through the remaining penalties
                    for j in range(i + 1, len(game.penalties)):

                        # The coincidental check:
                        # Time must match, using time (in seconds) becuase
                        # that only requires one check instead of checking
                        # period and periodTime
                        # Must be opposing teams, same type (without doubles),  
                        # coincidental must be False for both

                        if (
                            (game.penalties[i].time == game.penalties[j].time) and
                            not (game.penalties[i].team == game.penalties[j].team) and
                            (game.penalties[i].type == game.penalties[j].type) and
                            (game.penalties[i].coincidental == False) and 
                            (game.penalties[j].coincidental == False)
                        ):
                            print('Matching: ' + str(game.penalties[i]) + 
                            ' AND ' + str(game.penalties[j]))
                            game.penalties[i].coincidental = True
                            game.penalties[j].coincidental = True
                            
                            # If the penalties are double minors then
                            # make sure the second Coincidental is set to
                            # true also
                            if (
                                game.penalties[i].duration == 4
                            ):

                                game.penalties[i].secondCoincidental = True
                                game.penalties[j].secondCoincidental = True

                        ## Double Minor if statments ##

                        # If first penalty in a double minor, check if first half is
                        # coincidental, if not then use that, other wise check the
                        # second half
                        elif (
                            (game.penalties[i].time == game.penalties[j].time) and
                            game.penalties[i].duration == 4 and 
                            game.penalties[j].duration == 2 and
                            not (game.penalties[i].team == game.penalties[j].team) and
                            (game.penalties[i].coincidental == False) and 
                            (game.penalties[j].coincidental == False)
                        ):
                            print('Matching: ' + str(game.penalties[i]) + 
                            ' AND ' + str(game.penalties[j]))
                            game.penalties[i].coincidental = True
                            game.penalties[j].coincidental = True

                        # If first penalty in a double minor and the first
                        # penalty is already flagged as a coincidental
                        elif (
                            (game.penalties[i].time == game.penalties[j].time) and
                            game.penalties[i].duration == 4 and
                            game.penalties[j].duration == 2 and
                            not (game.penalties[i].team == game.penalties[j].team) and
                            (game.penalties[i].coincidental == True) and
                            (game.penalties[j].coincidental == False)
                        ):
                            # Can't include in the above if statment as it might
                            # other minor penalties

                            if (
                                (game.penalties[i].secondCoincidental == False)
                            ):
                           
                                print('Matching: ' + str(game.penalties[i]) + 
                                ' AND ' + str(game.penalties[j]))
                                game.penalties[i].secondCoincidental = True
                                game.penalties[j].coincidental = True

                        # If the first penalty is a minor matching against a
                        # double minor, neither are flag as coincidental
                        elif (
                            (game.penalties[i].time == game.penalties[j].time) and
                            game.penalties[i].duration == 2 and
                            game.penalties[j].duration == 4 and
                            not (game.penalties[i].team == game.penalties[j].team) and
                            (game.penalties[i].coincidental == False) and
                            (game.penalties[j].coincidental == False) 
                        ):
                            print('Matching: ' + str(game.penalties[i]) + 
                            ' AND ' + str(game.penalties[j]))
                            game.penalties[i].coincidental = True
                            game.penalties[j].coincidental = True

                        # If the first penalty is a minor matching against a
                        # double minor
                        elif (
                            (game.penalties[i].time == game.penalties[j].time) and
                            game.penalties[i].duration == 2 and 
                            game.penalties[j].duration == 4 and
                            not (game.penalties[i].team == game.penalties[j].team) and
                            (game.penalties[i].coincidental == False) and
                            (game.penalties[j].coincidental == True)
                        ):
                            # Can't include in the above if statment as it might
                            # other minor penalties
                            if (
                                (game.penalties[j].secondCoincidental == False)
                            ):
                                print('Matching: ' + str(game.penalties[i]) + 
                                ' AND ' + str(game.penalties[j]))
                                game.penalties[i].coincidental = True
                                game.penalties[j].secondCoincidental = True

        # After looping through all the penalties in the game return the game
        return game

    ## Find the penalty that the PPG was scored on
    # Time of penalty will have to be from before the goal was scored
    def find_penalty_for_PPG(self, game:Game) -> Game: 

        # Loop through each goal in the game
        # Goals: playId, period, periodTime, team, type

        for goal in game.goals:

            if (goal.type == 'PPG'):
                print('finding penalty for: ' + str(goal))

                # Loop through each penalty looking at minors then majors,
                # If there is a two man advantage with one penalty being a major and
                # the other a minor, then player with the minor penalty will be 
                # released and minor penalty is complete

                # Penalty can't already be acccounted for by already being
                # matched or a coincidental, goal must be within the
                # time + duration window, and the teams must be different

                # Minor Penalty
                for penalty in game.penalties:
                    print ('Checking: ' + str(penalty))
                    if (penalty.duration == 2):

                        if (
                            (penalty.result == '') and
                            not (penalty.coincidental) and 
                            (goal.team != penalty.team)
                        ):  
                            # Check that the goal happened between the beginning
                            # and end of the penalty
                            if((goal.time > penalty.time) 
                            and (goal.time < (penalty.time + penalty.duration_seconds))):
                                print('found a minor match')
                                penalty.result = goal
                                break
                

                    # Double Minor Penalty (4 min)
                    # have to check if coincidental in first half and second half
                    # then we can check for goals
                    elif (penalty.duration == 4):
                        
                        #if the penalty is second coincidental, then we skip it
                        #if the penalty is coincidental then reduce the amount
                        # of time being shorthanded  
                        if (
                            (penalty.coincidental) and 
                            not (penalty.secondCoincidental) and
                            (penalty.secondHalfResult == '') and
                            (goal.team != penalty.team)
                        ):
                            # Penalty is only 2 minutes with the first half a coincidental
                            if (
                                (goal.time > penalty.time) and 
                                (goal.time < penalty.time + (penalty.duration_seconds / 2))
                            ):
                                print('found a second half double minor match with first half coincidental')
                                penalty.secondHalfResult = goal
                                break
                        
                        # Double is no coinicidental at all
                        # Blank result means that the penalty hasn't had a goal assigned
                        elif (
                            (penalty.firstHalfResult == '') and
                            (penalty.secondHalfResult == '') and
                            not (penalty.coincidental) and
                            not (penalty.secondCoincidental) and
                            (goal.team != penalty.team)
                        ):

                            # Goal in the first half
                            if (
                                (goal.time > penalty.time) and 
                                (goal.time < penalty.time + (penalty.duration_seconds / 2))
                            ):
                                print('found a first half double minor match')
                                penalty.firstHalfResult = goal
                                break
                        
                            # Goal in the second half
                            elif (
                                (goal.time > penalty.time + (penalty.duration_seconds / 2)) and 
                                (goal.time  < penalty.time + (penalty.duration_seconds))
                            ):
                                print('found a second half double minor match')
                                penalty.secondHalfResult = goal
                                break
                    
                        # if a goal was already scored in the first half
                        elif (
                            not (penalty.firstHalfResult == '') and
                            not (penalty.coincidental) and
                            not (penalty.secondCoincidental) and
                             (goal.team != penalty.team)
                        ):
                            # Get the goal time of the first half
                            second_half_start_time = penalty.firstHalfResult.time

                            if(
                                (goal.time > second_half_start_time) and 
                                (goal.time < (second_half_start_time + (penalty.duration_seconds / 2)))
                            ):
                                
                                # Append the second goal to the penalty
                                print('found a second half double minor match, first half already scored on')
                                penalty.secondHalfResult = goal
                                break

                # Major Penalty
                for penalty in game.penalties:
                    if (penalty.duration == 5):

                        if (
                            not (penalty.coincidental) and 
                            (goal.team != penalty.team)
                        ):
                            if(
                                (goal.time > penalty.time) and 
                                (goal.time < penalty.time + penalty.duration_seconds)
                            ):
                                
                                print('found a major match')
                                # Major penalties don't expire when a goal is scored
                                # So we'll track the number of goals scored
                                penalty.results.append(goal)
                                break

        # return the game after all PP goals have been processed
        return game

# Testing
def main():
    pen_check = PenaltyChecker()

    home = 'EXH'
    away = 'EXA'

    # Game
    # url, gameId, date, visitors, home, goals, penalties
    game = Game('url', 1, '2021-01-14', away, home)

    # Penalties
    # playId, period, periodTime, team, infraction, duration, type

    # Minor coincidental
    game.penalties.append(events.minorPenalty(1, 1, '1:00', away, 'coincidental minor', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(2, 1, '1:00', home, 'coincidental minor', 2, 'Minor'))

    # Major Coincidental
    game.penalties.append(events.majorPenalty(3, 1, '2:00', home, 'coincidental major', 5, 'Major'))
    game.penalties.append(events.majorPenalty(4, 1, '2:00', away, 'coincidental major', 5, 'Major'))

    # Minor and major at the same time, not coincidental
    game.penalties.append(events.minorPenalty(5, 1, '3:00', home, 'non-coincidental minor', 2, 'Minor'))
    game.penalties.append(events.majorPenalty(6, 1, '3:00', away, 'non-coincidental major', 5, 'Major'))

    # Double minor and minor, should be skipped for now
    # Need to figure out how the double matches with the a minor
    game.penalties.append(events.doubleMinorPenalty(7, 1, '8:00', home, 'coincidental double minor', 4, 'Double'))
    game.penalties.append(events.majorPenalty(8, 1, '8:00', away, 'non-coincidental major', 5, 'Major'))
    game.penalties.append(events.minorPenalty(9, 1, '8:00', away, 'coincidental minor', 2, 'Minor'))

    # Make sure the loop is exiting correctly, only the first two should
    # be coincidental penalties
    game.penalties.append(events.minorPenalty(10, 1, '10:00', away, 'coincidental minor', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(11, 1, '10:00', home, 'coincidental minor', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(12, 1, '10:00', home, 'non-coincidental minor', 2, 'Minor'))

    # Two double minor penalties 
    game.penalties.append(events.doubleMinorPenalty(101, 1, '11:00', home, 'coincidental double minor', 4, 'Double'))
    game.penalties.append(events.doubleMinorPenalty(102, 1, '11:00', away, 'coincidental double minor', 4, 'Double'))

    # Doube minor matched against two minors
    game.penalties.append(events.doubleMinorPenalty(103, 1, '12:00', home, 'coincidental double minor', 4, 'Double'))
    game.penalties.append(events.minorPenalty(104, 1, '12:00', away, 'coincidental minor', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(105, 1, '12:00', away, 'coincidental minor', 2, 'Minor'))

    # Not coincidental 
    game.penalties.append(events.minorPenalty(106, 1, '13:00', away, 'not coincidental minor', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(107, 1, '13:01', away, 'not coincidental minor', 2, 'Minor'))
    

    ## Goal checks, should all be in second period
    # Goals: playId, period, periodTime, team, type
    game.penalties.append(events.minorPenalty(13, 2, '01:00', home, 'minor PPG', 2, 'Minor'))
    game.goals.append(events.Goal(14, 2, '01:30', away, 'PPG'))
    
    # Only one penalty should be matched to the goal 
    game.penalties.append(events.minorPenalty(15, 2, '02:00', home, 'minor PPG', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(16, 2, '02:15', home, 'minor no match', 2, 'Minor'))
    game.goals.append(events.Goal(17, 2, '02:30', away, 'PPG'))
    
    # Major Penalty, both goals should be counted against the penalty
    game.penalties.append(events.majorPenalty(18, 2, '05:00', away, 'Should be 3', 5, 'Major'))
    game.goals.append(events.Goal(19, 2, '05:30', home, 'PPG'))
    game.goals.append(events.Goal(20, 2, '05:45', home, 'PPG'))

    # Major penalty still in effect, minor should match with goal.
    game.penalties.append(events.minorPenalty(21, 2, '06:00', away, 'minor along wth major', 2, 'Minor'))
    game.goals.append(events.Goal(22, 2, '06:30', home, 'PPG'))

    # Double minor, goal in first and second half
    game.penalties.append(events.doubleMinorPenalty(23, 2, '11:00', home, 'Double minor, 2 goals', 4, 'Minor'))
    game.goals.append(events.Goal(24, 2, '11:30', away, 'PPG'))
    game.goals.append(events.Goal(25, 2, '12:30', away, 'PPG'))

    # Double minor, goal only in second half
    game.penalties.append(events.doubleMinorPenalty(26, 2, '14:00', home, 'Double minor, second haf goal', 4, 'Minor'))
    game.goals.append(events.Goal(27, 2, '16:30', away, 'PPG'))

    # double minor, coincidental first, goal in second
    game.penalties.append(events.doubleMinorPenalty(108, 3, '1:00', home, 'coincidental first', 4, 'Double'))
    game.penalties.append(events.minorPenalty(109, 3, '1:00', away, 'coincidental minor', 2, 'Minor'))
    game.goals.append(events.Goal(110, 3, '1:30', away, 'PPG'))

    # double minor 
    game.penalties.append(events.minorPenalty(111, 3, '1:35', away, 'non-coincidental minor', 2, 'Minor'))
    game.penalties.append(events.minorPenalty(112, 3, '1:36', home, 'non-coincidental minor', 2, 'Minor'))
    game.goals.append(events.Goal(111, 3, '1:40', away, 'EVEN'))


    print(game)

    game = pen_check.coincidentals(game)
    print('\nGame after Coincidental Check\n')
    print(game)

    
    game = pen_check.find_penalty_for_PPG(game)

    print('\nGame after goal checks\n')
    print(game)
    

if __name__ == "__main__":
    main()

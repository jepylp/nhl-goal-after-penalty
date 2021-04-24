from game import Game
import events
import jsonReader

## Find the double minors in a game

class DoubleMinorFinder:
    def __init__(self) -> None:
        jsr = jsonReader.JSON_Reader()

        season = 20202021

        gameLinks = jsr.season_reader(season)

        print(gameLinks)

        gameList = []

        for gameLink in gameLinks:
            game = jsr.game_reader(gameLink)

            for penalty in game.penalties:
                if penalty.duration == 4:
                    gameList.append(game)
                    break

        for game in gameList:
            print (game.boxscore + ' ,' + game.visitors + ',' + game.home)


def main():
    test = DoubleMinorFinder()

if __name__ == "__main__":
    main()

# Games that have double minors
#   https://statsapi.web.nhl.com/api/v1/game/2020020037/feed/live goal in first half 
#   https://statsapi.web.nhl.com/api/v1/game/2020020073/feed/live goal in second half
#   https://statsapi.web.nhl.com/api/v1/game/2020020098/feed/live No goal
#   https://statsapi.web.nhl.com/api/v1/game/2020020170/feed/live coincidentals, double no goal
#

import random
from enum import Enum

from pygolf.golfers import Golfer
from pygolf.course import GolfCourse


class GolfGame:
    """ Encapsulation of God's greatest game """

    def __init__(self, golfers: list(Golfer)):
        """ Construct a new game with a set of one or more golfers

            Arguments:
                * `golfers`: a list of Golfer objects which represent
                participants in the round
        """
        if len(golfers) < 1:
            raise ValueError('golf game cannot begin with 0 players')

        self._golfers = golfers
        self._scorecard = Scorecard(golfers)
        self._course = GolfCourse()

    @property
    def scorecard(self):
        return self._scorecard

#class StartingTees(Enum):
#    RED_TEES = 0
#    WHITE_TEES = 1
#    BLUE_TEES = 2
#    BLACK_TEES = 3
#    CHAMPIONSHIP_TEES = 4

class Scorecard:
    """ Represents a golf game's score """

    def __init__(self, golfers: list(Golfer), holes=18):
        self._golfers = golfers
        self._holes = 18

        # generate the blank scorecard
        self._scorecard = {}
        for golfer in golfers:
            self._scorecard[golfer.id] = []

    @property
    def golfers(self):
        return self._golfers

    @property
    def holes(self):
        return self._holes

    @property
    def scores(self):
        return self._scorecard

"""
Utilities for a game/match/round of golf to be played
"""

from pygolf.golfers import Golfer, Scorecard
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

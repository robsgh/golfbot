"""
Golfer-related items such as GolfBags, Scorecards, and Golfer game entities
"""

from uuid import uuid4

class Golfer:
    """ A Golfer's profile, which can also be used for participating in a game"""
    def __init__(self, name=''):
        """ Create a Golfer with a name

            Arguments:
            * `name`: The display name of the golfer (an id will be generated for server use)
        """
        self._name = name
        self._id = uuid4()
        self._bag = GolfBag()

    @property
    def name(self):
        """ The Golfer's name """
        return self._name

    @property
    def current_club(self):
        """ The club being used by the golfer """
        return self._bag.club

    @current_club.setter
    def current_club(self, club_code: str):
        self._bag.club = club_code

    @property
    def golfer_id(self):
        """ Identification tag for the golfer """
        return self._id


class Scorecard:
    """ Represents a golf game's score """
    def __init__(self, golfers: list(Golfer), holes=18):
        self._golfers = golfers
        self._holes = holes

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


class GolfBag:
    """ A bag of clubs """
    def __init__(self):
        self._clubs = [i+1 for i in range(14)]

    @property
    def club(self):
        return self._current_club

    @club.setter
    def club(self, club_code: str):
        if club_code not in ['driver','1','2','3','4','5','6','7','8','9','pw','gw','sw','lw','putter']:
            raise ValueError('tried to select a club which is not in the bag')

        self._current_club = club_code

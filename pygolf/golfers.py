class Golfer:
    """ A Golfer's profile, which can also be used for participating in a game"""
    def __init__(self, name='', match_history=[]):
        """ Create a Golfer with a name that has an established match history

            Arguments:
            * `name`: The display name of the golfer (an id will be generated for server use)
            * `match_history`: a list of Scorecard objects that represent past games
        """
        self.name = name
        self.match_history = match_history

    @property
    def name(self):
        """ Returns the Golfer's name """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def match_history(self):
        """ Returns the match history of the player """
        return self._match_history

    #@match_history.setter
    #def match_history(self, matches: list(Scorecard)):
    #    if len(matches) > 0 and isinstance(matches[0], Scorecard):
    #        self._match_history = matches

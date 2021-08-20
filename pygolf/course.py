from random import Random
import time
import math

class GolfCourse:
    """ Rolling greens and buttery swings """

    def __init__(self, hole_count: int=18, course_seed: int=None):
        """ Create a random golf course with a defined slope

            Arguments:
                * `hole_count`: Amount of holes which can be played on the course
                * `course_seed`: RNG seed for replaying a previous course
        """
        self._holes = hole_count
        self._seed = course_seed
        if not self._seed:
            self._seed = time.time()

        # create a random number generator with a time-based seed or a previous
        # seed from another course to replay it
        self._rng = Random(self._seed)

        # create the course
        self._course_data = self._generate_course()

    @property
    def holes(self) -> int:
        return self._holes

    @property
    def seed(self):
        return self._seed

    @property
    def total_distance(self) -> float:
        return self._course_data['total_distance']

    @property
    def course_par(self) -> int:
        return self._course_data['course_par']

    def hole_par(self, hole_number: int) -> int:
        """ Get the par for a specific hole on the course """
        if hole_number < 1 or hole_number > self.holes:
            raise ValueError('hole number out of course length bounds')
        return self._course_data['hole_par'][hole_number - 1]

    def _create_hole(self, par: int, length: float) -> dict:
        """ Create a single hole on a course with a set par and length

        Arguments:
        * `par`: number of strokes a scratch golfer would complete in
        * `length`: distance to cover for this hole
        """
        return {'par': par, 'length': length}

    def _calculate_par(self) -> int:
        """ Calculate a par [3,5] from the normal distribution centered around 4.4 """
        return min(max(math.floor(self._rng.normalvariate(4.4, 0.5)), 3), 5)

    def _generate_course(self) -> dict:
        """ Generate a full course and return the course data as a dictionary """
        # calculate the hole distribution
        distrib = []
        distrib.extend([3 for x in range(self._rng.randint(2,4))])
        distrib.extend([5 for x in range(self._rng.randint(2,4))])
        distrib.extend([4 for x in range(18-len(distrib))])
        self._rng.shuffle(distrib)

        course_par = 0
        for i in distrib:
            course_par += i

        total_dist = 0.0
        course_data = {'course_par': course_par, 'hole_par': distrib}
        for hole, par in enumerate(distrib):
            d = 0.0

            # adjust distances based on the USGA yardage guidelines for par
            # 3: 0-250yds   4: 251-470yds   5: 471-690yds
            if par == 3:
                d = self._rng.random() * 130.0 + 120.0
            elif par == 4:
                d = self._rng.random() * 219.0 + 251.0
            elif par == 5:
                d = self._rng.random() * 219.0 + 471.0
            course_data[hole] = self._create_hole(par, round(d))
            total_dist += round(d)

        # set the total course distance
        course_data['total_distance'] = total_dist
        return course_data

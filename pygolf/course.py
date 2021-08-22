"""
Course utilities and GolfCourse container
"""

from random import Random
from enum import Enum
import time


class CourseHazard(Enum):
    NONE = 0
    BUNKER = 1
    WATER = 2
    FESCUE = 3
    TREES = 4


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
        """ Amount of holes on the golf course """
        return self._holes

    @property
    def seed(self):
        """ Random number generator seed for this course """
        return self._seed

    @property
    def total_distance(self) -> float:
        """ Total course distance in yards """
        return self._course_data['total_distance']

    @property
    def course_par(self) -> int:
        """ Course par """
        return self._course_data['course_par']

    def stats(self):
        """ Print out general information about the course """
        print(f'Par: {self.course_par}, distance: {self.total_distance}')
        water = 0
        trees = 0
        fw_bunker = 0
        gs_bunker = 0
        for i in self._course_data['holes']:
            for j in i['fairway_hazards']:
                if j == CourseHazard.WATER: water += 1
                elif j == CourseHazard.TREES: trees += 1
                elif j == CourseHazard.BUNKER: fw_bunker += 1
            for j in i['greenside_hazards']:
                if j == CourseHazard.BUNKER: gs_bunker += 1
        print(f'Hazards:\n\tWater: {water}\n\tTrees: {trees}')
        print(f'\tBunkers:\n\t\tFairway: {fw_bunker}\tGreenside: {gs_bunker}')

    def hole_stats(self, hole_number: int):
        """ Print out general information about a specific hole on the course

        Arguments:
        * `hole_number`: hole number (1-self.holes) to view more info about
        """
        try:
            hole_info = self.get_hole(hole_number)
            print(f'Hole #{hole_number}: Par {hole_info["par"]}, Length: {hole_info["length"]}')
            print('Hazards:\n\tFairway:')
            for i, hazard in enumerate(hole_info['fairway_hazards']):
                if hazard == CourseHazard.NONE:
                    continue
                if i % 2 == 0:
                    print(f'left: {hazard}')
                else:
                    print(f'right: {hazard}')

            print('\tGreenside:')
            if hole_info['greenside_hazards'][0] != CourseHazard.NONE:
                print('Front: CourseHazard.BUNKER')
            if hole_info['greenside_hazards'][1] != CourseHazard.NONE:
                print('Back: CourseHazard.BUNKER')
            if hole_info['greenside_hazards'][2] != CourseHazard.NONE:
                print('Left: CourseHazard.BUNKER')
            if hole_info['greenside_hazards'][3] != CourseHazard.NONE:
                print('Right: CourseHazard.BUNKER')

        except ValueError as e:
            print(f'cannot display information about hole #{hole_number}: {e.with_traceback()}')
            return

    def hole_par(self, hole_number: int) -> int:
        """ Get the par for a specific hole on the course

        Arguments:
        * `hole_number`: the hole number 1-self.holes to check par

        Returns:
        * The par for a specific hole
        """
        return self.get_hole(hole_number)['par']

    def get_hole(self, hole_number: int) -> dict:
        """ Get the decription of a specific hole, including hazards and stats

        Arguments:
        * `hole_number`: the hole number (1-self.holes) to gather information about

        Returns:
        * A `dict` object that contains par, distance, and hazard information about the hole
        """
        if hole_number < 1 or hole_number > self.holes:
            raise ValueError(f'hole number {hole_number} is out of the interval [1-{self.holes}]')
        return self._course_data['holes'][hole_number-1]

    def _create_hole(self, par: int, length: float) -> dict:
        """ Create a single hole on a course with a set par and length

        Arguments:
        * `par`: number of strokes a scratch golfer would complete in
        * `length`: distance to cover for this hole
        """
        # green has a bunker near it 50% of the time
        greenside_hazards = []
        green_bunker_threshold = 0.5
        # four positions for the bunkers: front, back, left, right
        for _ in range(4):
            if self._rng.random() < green_bunker_threshold:
                greenside_hazards.append(CourseHazard.BUNKER)
            else:
                greenside_hazards.append(CourseHazard.NONE)

        # fairway has the following hazard percentages:
        fairway_hazards = []
        fairway_bunker_threshold = 0.8
        fairway_water_threshold = 0.75
        fairway_trees_threshold = 0.9
        # hazard is on left side when i%2==0 and right when i%2==1
        for _ in range(self._rng.randrange(0, 4)):
            val = self._rng.randrange(0,3)
            if val == 0 and self._rng.random() < fairway_bunker_threshold:
                fairway_hazards.append(CourseHazard.BUNKER)
            elif val == 1 and self._rng.random() < fairway_water_threshold:
                fairway_hazards.append(CourseHazard.WATER)
            elif val == 2 and self._rng.random() < fairway_trees_threshold:
                fairway_hazards.append(CourseHazard.TREES)
            else:
                fairway_hazards.append(CourseHazard.NONE)

        return {
            'par': par, 'length': length,
            'fairway_hazards': fairway_hazards,
            'greenside_hazards': greenside_hazards
        }

    def _calculate_pars(self) -> int:
        """ Create the random distribution of pars for the course

        Returns:
        * a tuple: 1st=hole_distribution, 2nd=course_par
        """
        # determine the amount of each par to create
        par_threes = self._rng.randrange(2,5)
        par_fives  = self._rng.randrange(2,4)
        par_fours  = self.holes - (par_threes + par_fives)

        # create the holes and randomly shuffle the list
        d = []
        d.extend([3 for x in range(par_threes)])
        d.extend([4 for x in range(par_fours)])
        d.extend([5 for x in range(par_fives)])
        self._rng.shuffle(d)

        # calculate course par and return
        course_par = (3 * par_threes) + (4 * par_fours) + (5 * par_fives)
        return d, course_par

    def _generate_course(self) -> dict:
        """ Generate a full course and return the course data as a dictionary """
        # calculate the hole distribution
        distrib, course_par = self._calculate_pars()

        total_dist = 0.0
        course_data = {'course_par': course_par, 'hole_par': distrib, 'holes': []}

        # adjust distances based on the USGA yardage guidelines for par
        # 3: 0-250yds   4: 251-470yds   5: 471-690yds
        # the upper bounds are represented as displacement from lower (upper - lower)
        # due to the usage of the bounds in Random.random()
        usga_lengths = {
            3: (120.0, 130.0),
            4: (251.0, 219.0),
            5: (471.0, 219.0),
        }

        for par in distrib:
            # calculate a distance for each hole based on the par guidelines in usga_lengths
            d = round(self._rng.random() * usga_lengths[par][0] + usga_lengths[par][1], 1)
            course_data['holes'].append(self._create_hole(par, d))
            total_dist += d

        # set the total course distance (rounded to correct float imprecision)
        course_data['total_distance'] = round(total_dist, 1)

        # return the completed course
        return course_data

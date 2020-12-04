# Authors: Jakub Wirkus, Paweł Zborowski
# Description: Calculating hotel rating based on 3 ratings (food quality, service quality, cleanness) using fuzzy logic

from skfuzzy import control as ctrl
import numpy as np
import skfuzzy as fuzz
import math


class Rating:

    def __init__(self):
        self.names = ['lowest', 'low', 'medium', 'high', 'highest']
        self.food = self.configure_input_value(np.arange(0, 11, 1), 'food')
        self.service = self.configure_input_value(np.arange(0, 11, 1), 'service')
        self.clean = self.configure_input_value(np.arange(0, 11, 1), 'clean')
        self.rating = self.configure_output_value(np.arange(0, 11, 1), 'rating')
        self.initialize_names()
        self.rating_sim = None

    @staticmethod
    def configure_input_value(input_range, name):
        return ctrl.Antecedent(input_range, name)

    @staticmethod
    def configure_output_value(output_range, name):
        return ctrl.Consequent(output_range, name)

    def initialize_names(self):
        self.food.automf(names=self.names)
        self.service.automf(names=self.names)
        self.clean.automf(names=self.names)
        self.rating.automf(names=self.names)

    def get_grade_of_rating_triangle(self, grade, triangle_list):
        self.rating[grade] = fuzz.trimf(self.rating.universe, triangle_list)
        return self.rating

    def get_grade_of_rating_quadrangle(self, grade, quadrangle_list):
        self.rating[grade] = fuzz.trapmf(self.rating.universe, quadrangle_list)
        return self.rating

    @staticmethod
    def get_rating_ctr(list_of_rules):
        return ctrl.ControlSystem(list_of_rules)

    def get_rating_sim(self, list_of_rules):
        return ctrl.ControlSystemSimulation(self.get_rating_ctr(list_of_rules))

    def initialize_rating_sim(self, list_of_rules):
        self.rating_sim = self.get_rating_sim(list_of_rules)
        return self.rating_sim

    def enter_quality(self, value):
        self.rating_sim.input[value] = int(input(f'Enter {value} quality <0,10>: '))
        return self.rating_sim

    def compute(self):
        return self.rating_sim.compute()

    def print_result(self):
        rating_value = 0
        if self.rating_sim.output['rating'] > 9.66:
            rating_value = math.ceil(self.rating_sim.output['rating'])
        elif self.rating_sim.output['rating'] < 1.70:
            rating_value = math.floor(self.rating_sim.output['rating'])
        else:
            rating_value = round(self.rating_sim.output['rating'])
        print("Calculated rating: ", self.rating_sim.output['rating'], "\nFinal rating: ", rating_value)

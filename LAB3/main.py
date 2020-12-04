# Authors: Jakub Wirkus, Paweł Zborowski
# Description: Calculating hotel rating based on
# 3 ratings (r.food quality, r.service quality, r.cleanness) using fuzzy logic

from LAB3.HotelRatingFuzzy import Rating
from skfuzzy import control as ctrl

if __name__ == '__main__':

    r = Rating()
    r.get_grade_of_rating_triangle('lowest', [0, 0, 1])
    r.get_grade_of_rating_triangle('low', [0, 2, 4])
    r.get_grade_of_rating_quadrangle('medium', [3, 4, 6, 7])
    r.get_grade_of_rating_triangle('high', [6, 8, 10])
    r.get_grade_of_rating_triangle('highest', [9, 10, 10])

    # Rules
    rule1 = ctrl.Rule(antecedent=(
        (r.service['lowest'] & r.clean['lowest'] & r.food['lowest']) |
        (r.service['lowest'] & r.clean['lowest'] & r.food['low'])),
        consequent=r.rating['lowest'])
    rule2 = ctrl.Rule(antecedent=(
        (r.service['low'] & r.clean['low'] & r.food['low']) |
        (r.service['low'] & r.clean['lowest'] & r.food['low']) |
        (r.service['lowest'] & r.clean['low'] & r.food['low']) |
        (r.service['low'] & r.clean['lowest'] & r.food['medium']) |
        (r.service['lowest'] & r.clean['low'] & r.food['medium'])),
        consequent=r.rating['low'])
    rule3 = ctrl.Rule(antecedent=(
        (r.service['medium'] & r.clean['medium'] & r.food['medium']) |
        (r.service['medium'] & r.clean['low'] & r.food['medium']) |
        (r.service['low'] & r.clean['medium'] & r.food['medium']) |
        (r.service['medium'] & r.clean['low'] & r.food['high']) |
        (r.service['low'] & r.clean['medium'] & r.food['high'])),
        consequent=r.rating['medium'])
    rule4 = ctrl.Rule(antecedent=(
        (r.service['high'] & r.clean['high'] & r.food['high']) |
        (r.service['high'] & r.clean['medium'] & r.food['high']) |
        (r.service['medium'] & r.clean['high'] & r.food['high']) |
        (r.service['high'] & r.clean['medium'] & r.food['highest']) |
        (r.service['medium'] & r.clean['high'] & r.food['highest'])),
        consequent=r.rating['high'])
    rule5 = ctrl.Rule(antecedent=(
        (r.service['highest'] & r.clean['highest'] & r.food['highest']) |
        (r.service['highest'] & r.clean['highest'] & r.food['high'])),
        consequent=r.rating['highest'])
    r.initialize_rating_sim([rule1, rule2, rule3, rule4, rule5])

    r.enter_quality('food')
    r.enter_quality('service')
    r.enter_quality('clean')

    r.compute()
    r.print_result()


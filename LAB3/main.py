import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

food = ctrl.Antecedent(np.arange(0, 11, 1), 'food')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
clean = ctrl.Antecedent(np.arange(0, 11, 1), 'clean')
rating = ctrl.Consequent(np.arange(0, 11, 1), 'rating')

names = ['lowest', 'low', 'medium', 'high', 'highest']

food.automf(names=names)
service.automf(names=names)
clean.automf(names=names)
rating.automf(names=names)

rating['lowest'] = fuzz.trimf(rating.universe, [0, 0, 1])
rating['low'] = fuzz.trimf(rating.universe, [0, 2, 4])
rating['medium'] = fuzz.trapmf(rating.universe, [3, 4, 6, 7])
rating['high'] = fuzz.trimf(rating.universe, [6, 8, 10])
rating['highest'] = fuzz.trimf(rating.universe, [9, 10, 10])


# Rules
rule1 = ctrl.Rule(antecedent=(
    (service['lowest'] & clean['lowest'] & food['lowest']) |
    (service['lowest'] & clean['lowest'] & food['low'])),
    consequent=rating['lowest'])
rule2 = ctrl.Rule(antecedent=(
    (service['low'] & clean['low'] & food['low']) |
    (service['low'] & clean['lowest'] & food['low']) |
    (service['lowest'] & clean['low'] & food['low']) |
    (service['low'] & clean['lowest'] & food['medium']) |
    (service['lowest'] & clean['low'] & food['medium'])),
    consequent=rating['low'])
rule3 = ctrl.Rule(antecedent=(
    (service['medium'] & clean['medium'] & food['medium']) |
    (service['medium'] & clean['low'] & food['medium']) |
    (service['low'] & clean['medium'] & food['medium']) |
    (service['medium'] & clean['low'] & food['high']) |
    (service['low'] & clean['medium'] & food['high'])),
    consequent=rating['medium'])
rule4 = ctrl.Rule(antecedent=(
    (service['high'] & clean['high'] & food['high']) |
    (service['high'] & clean['medium'] & food['high']) |
    (service['medium'] & clean['high'] & food['high']) |
    (service['high'] & clean['medium'] & food['highest']) |
    (service['medium'] & clean['high'] & food['highest'])),
    consequent=rating['high'])
rule5 = ctrl.Rule(antecedent=(
    (service['highest'] & clean['highest'] & food['highest']) |
    (service['highest'] & clean['highest'] & food['high'])),
    consequent=rating['highest'])

rating_ctr = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
rating_sim = ctrl.ControlSystemSimulation(rating_ctr)

food_quality = int(input("Enter food quality <0,10>: "))
service_quality = int(input("Enter service quality <0,10>: "))
clean_quality = int(input("Enter cleanness quality <0,10>: "))

rating_sim.input['food'] = food_quality
rating_sim.input['service'] = service_quality
rating_sim.input['clean'] = clean_quality

rating_sim.compute()
ratingValue = 0
if rating_sim.output['rating'] > 9.66:
    ratingValue = math.ceil(rating_sim.output['rating'])
elif rating_sim.output['rating'] < 1.70:
    ratingValue = math.floor(rating_sim.output['rating'])
else:
    ratingValue = round(rating_sim.output['rating'])
print("Calculated rating: ", rating_sim.output['rating'], "\nFinal rating: ", ratingValue)
rating.view(sim=rating_sim)

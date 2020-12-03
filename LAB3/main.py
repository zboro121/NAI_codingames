import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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
rule1 = ctrl.Rule(service['lowest'] & clean['lowest'], rating['lowest'])
rule2 = ctrl.Rule(service['low'] | clean['low'], rating['low'])
rule3 = ctrl.Rule(food['medium'] | service['medium'] | clean['medium'], rating['medium'])
rule4 = ctrl.Rule(service['high'] & clean['high'], rating['high'])
rule5 = ctrl.Rule(food['highest'] & service['highest'] & clean['highest'], rating['highest'])

rating_ctr = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
rating_sim = ctrl.ControlSystemSimulation(rating_ctr)

food_quality = int(input("Enter food quality <0,10>: "))
service_quality = int(input("Enter service quality <0,10>: "))
clean_quality = int(input("Enter cleanness quality <0,10>: "))

rating_sim.input['food'] = food_quality
rating_sim.input['service'] = service_quality
rating_sim.input['clean'] = clean_quality

rating_sim.compute()

print("Rating: ", rating_sim.output['rating'])
rating.view(sim=rating_sim)

# import simpy
# import random
#
#
# # Define the service center
# class ServiceCenter:
#     def __init__(self, env):
#         self.env = env
#         self.server = simpy.Resource(env, capacity=1)
#
#     def serve_customer(self, customer):
#         service_time = random.expovariate(0.5)
#         yield self.env.timeout(service_time)
#
#
# # Define the customer
# def customer(env, name, service_center):
#     print(f'{name} arrived at {env.now}')
#     with service_center.server.request() as request:
#         yield request
#         print(f'{name} started being served at {env.now}')
#         yield env.process(service_center.serve_customer(name))
#         print(f'{name} finished being served at {env.now}')
#
#
# # Define the simulation
# def simulation(env, service_center):
#     i = 0
#     while True:
#         i += 1
#         env.process(customer(env, f'Customer {i}', service_center))
#         inter_arrival_time = random.expovariate(0.2)
#         yield env.timeout(inter_arrival_time)
#
#
# # Run the simulation
# env = simpy.Environment()
# service_center = ServiceCenter(env)
# env.process(simulation(env, service_center))
# env.run(until=20)


###

#           Steal   Share
# Steal     1/1     5/0
# Share     0/5     3/3


from enum import Enum
import random


class Action(Enum):
    STEAL = 1
    SHARE = 2


def simulation(num_games, strategy_1, strategy_2):
    total_1 = 0
    total_2 = 0

    for i in range(num_games):
        action_1 = strategy_1.action()
        action_2 = strategy_2.action()

        strategy_1.add_opp_action(action_2)
        strategy_2.add_opp_action(action_1)

        if action_1 == action_2:
            if action_1 == Action.STEAL:    # steal steal
                total_1 += 1
                total_2 += 1
            else:                           # share share
                total_1 += 3
                total_2 += 3
        else:
            if action_1 == Action.STEAL:    # steal share
                total_1 += 5
                total_2 += 0
            else:                           # share steal
                total_1 += 0
                total_2 += 5

        print(action_1, action_2)
        print(f"\t{total_1} {total_2}")


class TitForTat:
    def __init__(self):
        self.opponents_actions = []

    def add_opp_action(self, action):
        self.opponents_actions.append(action)

    def action(self):
        if not self.opponents_actions:
            return Action.SHARE
        return self.opponents_actions[-1]       # otherwise return opponents last move


class RandomAction:
    def __init__(self):
        self.opponents_actions = []

    def add_opp_action(self, action):
        self.opponents_actions.append(action)

    def action(self):
        a = random.randint(1, 2)
        return Action.SHARE if a == 1 else Action.STEAL


s1 = TitForTat()
s2 = RandomAction()

simulation(10, s1, s2)

import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
import random


class SimpleDriller(Env):
    def __init__(self, env_config):
        # 2d presentative matrix
        self.model = np.loadtxt(env_config['model_path'], delimiter=env_config['delim'])
        # discretizing space
        self.nrow, self.ncol = self.model.shape
        # Available pipe
        self.available_pipe = env_config['available_pipe']

        # Initial production capacity
        self.production = 0

        # Actions we can take
        self.action_space = Discrete(4)

        # Space our agent can interact with
        self.observation_space = Box(low=0, high=1, shape=(self.nrow, self.ncol), dtype='bool')
        self.reset()

    def step(self, action):
        actions = {
            0: [1, 0],  # down
            1: [0, -1],  # left
            2: [0, 1],  # right
            3: [-1, 0],  # up
        }

        def take_action(loc, action):
            available_actions = list(actions.keys())
            stuck = False

            if loc[0] <= 1:
                available_actions.remove(3)

            if loc[0] == (self.nrow - 1):
                available_actions.remove(0)

            if loc[1] == 0:
                available_actions.remove(1)

            if loc[1] == (self.ncol - 1):
                available_actions.remove(2)

            if action not in available_actions:
                action = random.choice(available_actions)

            available_actions.remove(action)
            change = actions[action]
            new_location = [old + new for old, new in zip(loc, change)]

            if new_location in self.trajectory:
                collision = True
                while collision:
                    try:
                        new_action = random.choice(available_actions)
                    except IndexError:
                        stuck = True
                        break

                    try:
                        available_actions.remove(new_action)
                    except ValueError:
                        stuck = True
                        break

                    change = actions[new_action]
                    new_location = [old + new for old, new in zip(loc, change)]

                    if new_location not in self.trajectory:
                        collision = False

            return new_location, stuck

        new_location, stuck = take_action(self.bit_location, action)

        done = False
        if stuck:
            done = True
            reward = 0

        else:
            self.bit_location = new_location

            # adding and saving updated trajectory
            self.trajectory.append(new_location)
            newrow, newcol = new_location

            # reward calculcation
            reward = self.model[newrow, newcol]

            # new state
            self.update_state()

            # Reduce pipe inventory
            self.pipe_used += 1

            # Check if pipe has run out
            if self.pipe_used == self.available_pipe:
                done = True

        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info

    def update_state(self):
        traj_i, traj_j = np.asarray(self.trajectory).T
        self.state[traj_i, traj_j] = 1

    def render(self):
        # Implement viz
        raise NotImplemented("No renderer implemented yet.")
        pass

    def reset(self):
        # Reset SHL
        self.surface_hole_location = [1, random.randint(0, self.ncol - 1)]
        self.state = np.zeros((self.nrow, self.ncol), dtype=bool)
        self.bit_location = self.surface_hole_location
        # Reset Trajectory
        self.trajectory = [self.surface_hole_location]
        # Reset pipe
        self.pipe_used = 0
        return self.state
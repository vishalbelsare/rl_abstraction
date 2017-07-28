# Python imports.
from collections import defaultdict

# Other imports.
from OptionClass import Option

class ActionAbstraction(object):

    def __init__(self, options=[]):
        self.options = self._convert_to_options(options)
        self.is_cur_executing = False
        self.cur_option = None # The option we're executing currently.

    def act(self, agent, abstr_state, ground_state, reward):
        '''
        Args:
            agent (Agent)
            abstr_state (State)
            ground_state (State)
            reward (float)
        '''
        if self.is_next_step_continuing_option(ground_state):
            # We're in an option and not terminating.
            a = self.get_next_ground_action(ground_state)
            # print "continue", self.cur_option.name, ground_state, a
            return a
        else:
            # We're not in an option, check with agent.
            active_options = self._get_active_options(ground_state)
            # print "Active options in", ground_state, 
            # for o in active_options:
            #     print o,
            # print
            # print
            agent.actions = active_options
            abstr_action = agent.act(abstr_state, reward)

            self.set_option_executing(abstr_action)
            return self.abs_to_ground(ground_state, abstr_action)

    def _get_active_options(self, state):
        '''
        Args:
            state (State)

        Returns:
            (list): Contains all active options.
        '''
        result = []
        for o in self.options:
            if o.is_init_true(state):
                result.append(o)
        return result

    def _convert_to_options(self, action_list):
        '''
        Args:
            action_list (list)

        Returns:
            (list of Option)
        '''
        options = []
        for ground_action in action_list:
            o = ground_action
            if type(ground_action) is str:
                o = Option(init_func=make_lambda(True),
                            term_func=make_lambda(True),
                            policy=make_lambda(ground_action))
            options.append(o)
        return options

    def is_next_step_continuing_option(self, ground_state):
        '''
        Returns:
            (bool): True iff an option was executing and should continue next step.
        '''
        # if self.cur_option:
        #     print self.cur_option.name, self.cur_option.is_term_true(ground_state), ground_state
        return self.is_cur_executing and not self.cur_option.is_term_true(ground_state)

    def set_option_executing(self, option):
        if option not in self.options:
            print "Error: agent chose a non-existent option (" + option + ")."
            quit()

        self.cur_option = option
        self.is_cur_executing = True

    def get_next_ground_action(self, ground_state):
        return self.cur_option.act(ground_state)

    def get_actions(self):
        return self.options

    def abs_to_ground(self, ground_state, abstr_action):
        return abstr_action.act(ground_state)

    def add_option(self, option):
        self.options += [option]

    def reset(self):
        self.is_cur_executing = False
        self.cur_option = None # The option we're executing currently.

    def end_of_episode(self):
        self.reset()


def make_lambda(result):
    return lambda x : result
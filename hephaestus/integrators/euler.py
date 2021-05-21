"""
Class to implement the Euler integration method.
"""

from hephaestus.integrators.integrator import Integrator
import tensorflow as tf


class Euler(Integrator):
    """
    Class for Euler integration.
    """

    @tf.function
    def perform_step(self, initial_conditions: dict = None):
        """
        Perform a step of the integrator.

        Parameters
        ----------
        initial_conditions

        Returns
        -------

        """
        self._run_check(initial_conditions)

        new_pos = initial_conditions['x0'] + initial_conditions['v0'] * self.time_step + \
                    0.5 * initial_conditions['a0'] * (self.time_step ** 2)

        return {'x': new_pos}

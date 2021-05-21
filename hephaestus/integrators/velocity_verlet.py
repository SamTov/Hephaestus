"""
Class to implement the Velocity Verlet integration method.
"""

from hephaestus.integrators.integrator import Integrator
import tensorflow as tf


class VelocityVerlet(Integrator):
    """
    Class for Velocity Verlet integration.
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

        pos_update = initial_conditions['x0'] + initial_conditions['v0']*self.time_step + \
                     0.5*initial_conditions['a0']*(self.time_step**2)
        vel_half = initial_conditions['v0'] + 0.5*initial_conditions['a0']*self.time_step
        new_acc = self.model.compute_forces(pos_update)
        new_vel = vel_half + 0.5*new_acc*self.time_step

        return {'x': pos_update, 'v': new_vel, 'a': new_acc}

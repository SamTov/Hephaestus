"""
Module for the single pendulum study.
"""

import tensorflow as tf
from hephaestus.integrators.integrator import Integrator
from hephaestus.integrators.euler import Euler
import numpy as np


class SinglePendulum:
    """
    Class for a single pendulum simulation.

    Attributes
    ----------
    mass : float
            Mass of the bob
    length : float
            Length of the pendulum
    gravity : float
            Gravity experienced by the pendulum
    theta_start : float
            starting position of the pendulum
    steps : int
            Number of simulation steps to perform
    time_step : float
            Time step of the simulation.
    theta : tf.Tensor
            Theta value of the pendulum throughout the simulation
    v0 : float
                starting velocity of the bob.
    pe : tf.Tensor
            Potential energy of the system through time
    ke : tf.Tensor
            Kinetic energy of the system through time.
    velocity : tf.Tensor
            velocity of the system through time.
    force : tf.Tensor
            force of the system through time.
    integrator : Integrator
                Integrator to use in the simulation.
    """
    def __init__(self, mass: float = 1.0, length: float = 1.0, gravity: float = 10.0, theta_start: float = 5.0, 
                 steps: int = 100, time_step: float = 1.0, v0: float = 0.0, integrator: Integrator = None):
        """
        Constructor for the single pendulum class.

        Parameters
        ----------
        mass : float
                Mass of the bob
        length : float
                Length of the pendulum
        gravity : float
                Gravity experienced by the pendulum
        theta_start : float
                starting position of the pendulum
        steps : int
                Number of simulation steps to perform
        time_step : float
                Time step of the simulation.
        v0 : float
                starting velocity of the bob.
        integrator : Integrator
                Integrator to use in the simulation.
        """
        self.mass = mass
        self.length = length
        self.gravity = gravity
        self.theta_0 = theta_start
        self.v0 = v0
        self.steps = steps
        self.time_step = time_step
        self.integrator = integrator

        # Internal Parameters
        self.theta = np.zeros(shape=(steps,))
        self.velocity = np.zeros(shape=(steps,))
        self.force = np.zeros(shape=(steps,))
        self.pe = np.zeros(shape=(steps,))
        self.ke = np.zeros(shape=(steps,))

        self._instantiate_system()

    @staticmethod
    def _deg_to_rad(theta: float):
        """
        Convert degrees to radians.

        Parameters
        ----------
        theta : float
                Degree value to convert to radians.

        Returns
        -------
        The value in radians.
        """
        return theta * np.pi / 180

    def compute_forces(self, theta: float):
        """
        Compute the force on the pendulum bob.

        Parameters
        ----------
        theta : float
                Current theta value to use.

        Returns
        -------
        """
        return -1 * (self.gravity / self.length)*tf.sin(self._deg_to_rad(theta))

    def _compute_ke(self, velocity: float):
        """
        Compute the kinetic energy of the system.

        Parameters
        ----------
        velocity : float
                Current velocity of the system.

        Returns
        -------
        ke : float
                Kinetic energy of the system.
        """
        return 0.5 * self.mass * self.length**2 * velocity**2

    def _compute_pe(self, position: float):
        """
        Compute the potential energy of the system.

        Parameters
        ----------
        position : float
                Current position of the bob.

        Returns
        -------
        pe : float
                potential energy of the system
        """
        return self.gravity * self.mass * self.length * (1 - tf.cos(self._deg_to_rad(position)))

    def _instantiate_system(self):
        """
        Instantiate the initial conditions in the system records.
        Returns
        -------
        Updates the class state.
        """
        if self.integrator is None:
            self.integrator = Euler(self.time_step, self)
        self.theta[0] = self.theta_0
        self.velocity[0] = self.v0
        self.force[0] = self.compute_forces(self.theta_0)
        self.pe[0] = self._compute_pe(self.theta_0)
        self.ke[0] = self._compute_ke(self.v0)

    def _set_conditions(self, step: int) -> dict:
        """
        Set current conditions.

        Parameters
        ----------
        step : int
                Current step, needed to select previous time values.

        Returns
        -------
        conditions : dict
                All conditions of the system at point step - 1.
        """

        return {'x0': self.theta[step-1], 'v0': self.velocity[step-1], 'a0': self.force[step - 1]}

    def _compute_velocity(self, t1: float, t2: float):
        """
        compute the angular velocity of the pendulum.

        Parameters
        ----------
        t1 : float
                position at time 1
        t2 : float
                position at time 2

        Returns
        -------
        velocity : float
                velocity of the system at time t2.
        """
        return (t2 - t1) / self.time_step

    def _partial_update_state(self, integration_data: dict, step: int):
        """
        Update the recorded state of the system.

        Parameters
        ----------
        step : int
                Current time step.

        Returns
        -------
        Updates class attributes.
        """
        self.theta[step] = integration_data['x']
        self.velocity[step] = self._compute_velocity(self.theta[step - 1], self.theta[step])
        self.force[step] = self.compute_forces(self.theta[step])
        self.pe[step] = self._compute_pe(self.theta[step])
        self.ke[step] = self._compute_ke(self.velocity[step])

    def _full_update_state(self, integration_data: dict, step: int):
        """
        Update the recorded state of the system.

        Parameters
        ----------
        step : int
                Current time step.

        Returns
        -------
        Updates class attributes.
        """
        try:
            self.theta[step] = integration_data['x']
            self.velocity[step] = integration_data['v']
            self.force[step] = integration_data['a']
            self.pe[step] = self._compute_pe(self.theta[step])
            self.ke[step] = self._compute_ke(self.velocity[step])
        except KeyError:
            raise ValueError

    def _plot_results(self):
        """
        Plot the results of the simulation.

        Returns
        -------

        """
        pass

    def run_simulation(self):
        """
        Run the simulation.

        Returns
        -------

        """
        for step in range(1, self.steps):
            conditions = self._set_conditions(step)
            integration_step = self.integrator.perform_step(conditions)
            try:
                self._full_update_state(integration_step, step)
            except ValueError:
                self._partial_update_state(integration_step, step)

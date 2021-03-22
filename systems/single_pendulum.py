"""
Module for the single pendulum study.
"""

import tensorflow as tf

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
    pe : tf.Tensor
            Potential energy of the system through time
    ke : tf.Tensor
            Kinetic energy of the system through time.
    """
    def __init__(self, mass: float, length: float, gravity: float, theta_start: float, steps: int, time_step: float):
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
        """
        self.mass = mass
        self.length = length
        self.gravity = gravity
        self.theta_0 = theta_start
        self.steps = steps
        self.time_step = time_step

        # Internal Parameters
        self.theta: tf.Tensor
        self.pe: tf.Tensor
        self.ke: tf.Tensor

    def _compute_forces(self):
        """
        Compute the force on the pendulum bob.

        Returns
        -------

        """
        




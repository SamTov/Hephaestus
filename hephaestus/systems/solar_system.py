"""
This program and the accompanying materials are made available under the terms
of the Eclipse Public License v2.0 which accompanies this distribution,
and is available at https://www.eclipse.org/legal/epl-v20.html
SPDX-License-Identifier: EPL-2.0

Copyright Contributors to the Zincware Project.

Description: A python simulation of planetary motion.
"""
import tensorflow as tf
from hephaestus.integrators.integrator import Integrator
from hephaestus.integrators.euler import Euler
import numpy as np
from tqdm import tqdm


class SolarSystem:
    """
    A class to simulate planetary orbits in a solar system.

    Attributes
    ----------
    solar_system : dict
            solar system to perform a simulation on.
            e.g. {'Sun': {'position': [0, 0 ,0], 'mass': 1.989e30},
            'Earth': {}, 'Earth_Moon': {}, 'Mars': {}}
    gravitational_constant : float
            Value of the gravitational constant to use in the simulation.
    steps : int
            Number of simulation steps to perform
    time_step : float
            Time step of the simulation.
    integrator : Integrator
            Integrator to use in the simulation.
    time_series : dict
            Dictionary containing all information regarding the planetary
             positions, velocities, and forces with respect to time.
            e.g.
    """

    def __init__(self,
                 solar_system: dict,
                 gravitational_constant: float = 6.674e-11,
                 steps: int = 100,
                 time_step: float = 1,
                 integrator: Integrator = None):
        """
        Constructor for the solar system class.

        Parameters
        ----------
        solar_system : dict
                solar system to perform a simulation on.
                e.g. {'Sun': {'position': [0, 0 ,0], 'mass': 1.989e30},
                'Earth': {}, 'Earth_Moon': {}, 'Mars': {}}
        gravitational_constant : float
                Value of the gravitational constant to use in the simulation.
        steps : int
                Number of simulation steps to perform
        time_step : float
                Time step of the simulation.
        integrator : Integrator
                Integrator to use in the simulation.
        """
        self.solar_system = solar_system
        self.gravitational_constant = gravitational_constant
        self.steps = steps
        self.time_step = time_step
        self.integrator = integrator

        self.positions: np.ndarray = np.zeros((len(solar_system), steps, 3))
        self.velocities: np.ndarray = np.zeros((len(solar_system), steps, 3))
        self.forces: np.ndarray = np.zeros((len(solar_system), steps, 3))
        self.ke: np.ndarray = np.zeros((len(solar_system), steps, 1))
        self.pe: np.ndarray = np.zeros((len(solar_system), steps, 1))

    def _compute_forces(self,
                        pos_1: np.ndarray,
                        pos_2: np.ndarray,
                        mass_1: np.ndarray,
                        mass_2: np.ndarray):
        """
        Compute the interactions between the planets.

        Parameters
        ----------
        pos_1 : np.ndarray
                vector position of the first particle.
        pos_2 : np.ndarray
                vector positions of the second particle.
        mass_1 : np.ndarray
                mass of the first particle.
        mass_2 : np.ndarray
                mass of the second particle.

        Returns
        -------
        forces: tf.Tensor
                Forces acting on the particles parsed.
        """
        return self.gravitational_constant * mass_1 * mass_2 / \
               tf.tensordot(pos_1 - pos_2, pos_1 - pos_2)

    def _compute_energy(self,
                        pos_1: np.ndarray,
                        pos_2: np.ndarray,
                        mass_1: np.ndarray,
                        mass_2: np.ndarray):
        """
        Compute the interactions between the planets.

        Parameters
        ----------
        pos_1 : np.ndarray
                vector position of the first particle.
        pos_2 : np.ndarray
                vector positions of the second particle.
        mass_1 : np.ndarray
                mass of the first particle.
        mass_2 : np.ndarray
                mass of the second particle.

        Returns
        -------
        pe : tf.Tensor
                Potential energy of the particles parsed.
        """
        return -1 * self.gravitational_constant * mass_1 * mass_2 / \
               tf.norm(pos_1 - pos_2, pos_1 - pos_2)

    def _build_distance_tensor(self, index: int):
        """

        Parameters
        ----------
        index : int
                Which time step to build the tensor fpr.

        Returns
        -------
        rij : tf.Tensor
                A distance tensor on which to operate.
        """
        r_ij_cartesian = tf.reshape(self.positions[:, index],
                                    (1, len(self.positions[:, index]), 3)) - \
                         tf.reshape(self.positions[:, index],
                                    (len(self.positions[:, index]), 1, 3))

        return tf.norm(r_ij_cartesian, ord='euclidean', axis=2)

    def _set_conditions(self, step: int):
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
        return {'x0': self.positions[:, step - 1],
                'v0': self.velocities[:, step - 1],
                'a0': self.forces[:, step - 1]}

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
        self.positions[step] = integration_data['x']
        # self.velocity[step] = self._compute_velocity(self.positions[step - 1],
        #                                              self.theta[step])
        self.forces[step] = self._compute_forces(self.step)
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

    def run_simulation(self):
        """
        Run the planetary orbit simulation.

        Returns
        -------

        """
        for step in tqdm(range(1, self.steps), ncols=70, desc='Running '
                                                              'simulation.'):
            conditions = self._set_conditions(step)
            integration_data = self.integrator.perform_step(conditions)

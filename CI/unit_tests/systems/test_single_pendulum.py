"""
Test the single pendulum module.
"""
import unittest
from hephaestus.integrators.euler import Euler


class TestEuler(unittest.TestCase):
    """
    Class to test the euler integration module.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Prepare for the Velocity verlet test.
        """
        cls.integrator = Euler(time_step=1.0, model=None)

    def test_perform_step(self):
        """
        Test the perform step method.
        """
        state = {'x0': 1.0,
                 'v0': 0.5,
                 'a0': 2.0}
        outcome = self.integrator.perform_step(state)
        print(outcome['x'])
        self.assertEqual(outcome, {'x': 3.5})


if __name__ == '__main__':
    unittest.main()

import numpy as np
import unittest
from numpy.testing import (assert_almost_equal, assert_equal, assert_)
from scipy import constants
import refnx.reduce.parabolic_motion as pm

class TestParabolicMotion(unittest.TestCase):

    def setUp(self):
        pass

    def test_y_deflection(self):
        # Launch a projectile at 45 degrees at 300 m/s.
        # It should have a flight time of 43.262894944953523 s
        # for which the range is 9177.445 m, at which point the
        # deflection should be 0.
        deflection = pm.y_deflection(45, 9177.4459168013527, 300.)
        assert_almost_equal(deflection, 0)

    def test_elevation(self):
        # angle as it passes y = 0 should be -ve of initial trajectory
        angle = pm.elevation(45., 9177.4459168013527, 300.)
        assert_almost_equal(angle, -45)

    def test_find_trajectory(self):
        # the angle needs to be 45 degrees for a projectile launched
        # at 300 m/s with a range of x=9177, y = 0
        traj = pm.find_trajectory(0, 9177.4459168013527, 300.)
        assert_almost_equal(traj, 45., 5)

        # Test for theta != 0
        # Assume parabolic path passes through known peak height.
        # peak height = v_0y ** 2 / 2 / g
        # the angle needs to be 45 degrees for a projectile passing
        # through x = 9177 / 2, arctan(peak_height / 9177 * 2)
        peak_height = (300 * np.sin(np.radians(45.))) ** 2 / 2. / constants.g
        assert_equal(peak_height, 2294.3614792003382)
        theta = np.degrees(np.arctan(peak_height / 9177.4459168013527 * 2.))

        traj = pm.find_trajectory(theta, 9177.4459168013527 / 2., 300.)
        assert_almost_equal(traj, 45., 5)

    def test_parabola_line_intersection_point(self):
        traj = pm.find_trajectory(-0.62, 3, 300.)

        res = pm.parabola_line_intersection_point(traj, 3, 300, -0.62, 0)
        assert_almost_equal(res[2], 0)
        assert_almost_equal(res[1], pm.y_deflection(traj, 3, 300))
        assert_almost_equal(res[0], 3)

        res = pm.parabola_line_intersection_point(traj, 3.1, 300, -0.62, 0.8)
        assert_(res[0] < 3.1)
        assert_almost_equal(np.array(res),
                            np.array([3.0988052120901273,
                                      -0.033550291159381511,
                                      0.0011947938059390722]))


if __name__ == '__main__':
    unittest.main()
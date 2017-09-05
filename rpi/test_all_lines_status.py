from   mock import Mock
import numpy as np
import sys
import unittest


def print_args(*args):
    print args


# unicornhat is not installed other than on RPi - want to test elsewhere
mock_hat = Mock()
mock_hat.set_pixel = Mock(side_effect=print_args)
mock_hat.get_shape = Mock(return_value=(8, 8))
sys.modules['unicornhat'] = mock_hat
import all_lines_status


class UnicornHatTestCase(unittest.TestCase):

    def test_update_hat(self):
        """ Examine calls being made to the unicorn hat"""
        tube_status = np.ones(48 * 3).reshape(48, 3).astype(int) * 255
        all_lines_status.update_hat(tube_status)


if __name__ == '__main__':
    unittest.main()

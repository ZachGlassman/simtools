import unittest 
from simtools.Simulation import Simulation, parse_time_diff

class test_parse_time_diff(unittest.TestCase):

    def test_seconds(self):
        self.assertEqual(parse_time_diff(1), "1.00 s")

    def test_ms(self):
        self.assertEqual(parse_time_diff(.01), "10.00 ms")

    def test_min(self):
        self.assertEqual(parse_time_diff(61), "1.02 min")
    
    def test_one_min(self):
        self.assertEqual(parse_time_diff(60), "1.00 min")

class test_Simulation(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

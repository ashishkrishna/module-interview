#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-

import unittest
import modules


class ModuleCase(unittest.TestCase):

    def test_1_module_operating_at_stc(self):
        '''
        Task 1: Create a (python) module with functions that describe a
        (solar) module. Load the module coefficients for the Trina TSM PA05
        from the CSV, set the temperature (T), to 25ºC and the irradiance (S)
        to 1000 W/m^2.

        This test will pass when you calculate voltage and current matching the
        correct numerical values along the (solar) module's I/V curve.
        '''

        (voltage, current) = modules.module_i_v(25, 1000, 7.81164023)
        self.assertAlmostEquals(voltage, 5, 2)
        self.assertAlmostEquals(current, 8.345847070106313,
                                msg='Current output at 5V is 8.34584 Amps')

        (voltage, current) = modules.module_i_v(25, 1000, 27.78831673)
        self.assertAlmostEquals(voltage, 25, 2)
        self.assertAlmostEquals(current, 8.276615347828452,
                                msg='Current output at 25V is 8.2766 Amps')

        (voltage, current) = modules.module_i_v(25, 1000, 35.80111755)
        self.assertAlmostEquals(voltage, 34, 2)
        self.assertAlmostEquals(current, 5.3462926879868,
                                msg='Current output at 34V is 5.3462 Amps')

    def test_2_module_operating_at_low_irradiance_high_temperature(self):
        '''
        Task 2:  Make sure your implementation produces accurate results at
        alternative irradiance and temperature levels.

        Here we used an irradiance of 600 W/m^2, and a temperature of 45ºC on
        the same Trina module as in Task 1.
        '''

        (voltage, current) = modules.module_i_v(45, 600, 6.6849030788)
        self.assertAlmostEquals(voltage, 5, 2)
        self.assertAlmostEquals(current, 5.001330819496669, 2,
                                msg='Current output at 5V is 5.00133 Amps')

        (voltage, current) = modules.module_i_v(45, 600, 16.674489)
        self.assertAlmostEquals(voltage, 15, 2)
        self.assertAlmostEquals(current, 4.97041290811022, 2,
                                msg='Current output at 15V is 4.9704 Amps')

        (voltage, current) = modules.module_i_v(45, 600, 31.36776738)
        #print(voltage)
        self.assertAlmostEquals(voltage, 30, 2)
        #print(current)
        self.assertAlmostEquals(current, 4.048128130946268, 2,
                                msg='Current output at 30V is 4.0481 Amps')

    def test_3_optimize_module_power(self):
        '''
        Task 3:  Usually, we don't just need to understand what the potential
        output of a solar module is (e.g. the I/V curve), we want to find out
        what voltage and current the module should be operating at in order to
        produce the most power.

        Write a function/method that determines the voltage and current along a
        modules I/V curve that maximizes power.  We won't tell you what the
        answer is, so also write the test that proves you found it.
        '''

        (voltage, current) = modules.max_power(45,600)
        self.assertAlmostEquals(voltage, 28, 1)
        self.assertAlmostEquals(current, 4.68, 1, msg = 'Optimal power output is at 28 V and 4.68 Amps')
       

    def test_4_optimize_module_power_extreme_conditions(self):
        '''
        Task 4: Write the tests to make sure your algorithm in Task 3 works
        for a range of module operating conditions and handles tricky edge
        cases correctly.

        For your reference, a module in the middle of the the Arizona desert
        at noon might have irradiance of ~1400 W/m^2.  A wintry London day
        might be 600 W/m^2.
        '''
        (voltage, current) = modules.max_power(45, 1400)
        self.assertAlmostEquals(voltage, 27.27, 2)
        self.assertAlmostEquals(current, 10.96, 2)
        (voltage, current) = modules.max_power(0, 600)
        self.assertAlmostEquals(voltage, 33.28, 2)
        self.assertAlmostEquals(current, 4.73, 2)
        (voltage, current) = modules.max_power(-30, 600)
        self.assertAlmostEquals(voltage, 35.12, 2)
        self.assertAlmostEquals(current, 4.76 , 2)
        (voltage, current) = modules.max_power(0, 0)
    


if __name__ == "__main__":
    unittest.main()

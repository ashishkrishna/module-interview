from __future__ import division
import csv
import pprint
import math
import numpy as np
Q = 1.60217657e-19
K = 1.3806488e-23
T = 273.


def module_i_v(temp, irr, v_diode):
    dict_fields = get_parameters('TSM PA05')
    i_sc = float(dict_fields['i_sc'])
    s = float(irr)
    i_0 = float(dict_fields['i0'])
    tau = float(dict_fields['temp_i0'])
    r_p = float(dict_fields['r_parallel'])
    r_s = float(dict_fields['r_series'])
    pwr = float(dict_fields['power'])
    gamma = float(dict_fields['gamma'])
    temp = float(temp+T)
    i_t = float(i_0 * (1+tau)**(temp-298))
    v_diode = float(v_diode)
    i_v_diode = i_sc * (s/1000) - i_t*(math.exp((Q/(K*temp*gamma)) * v_diode) - 1) - (v_diode/r_p)
    v_v_diode = v_diode - i_v_diode * r_s
    return (v_v_diode, i_v_diode)

def max_power(temp, irr):
    dict_fields = get_parameters('TSM PA05')
    i_sc = float(dict_fields['i_sc'])
    r_s = float(dict_fields['r_series'])
    v_lim_1 = i_sc*r_s
    v_diode = v_lim_1
    power_vals = []
    v_v_diode = 0
    while(v_diode-v_v_diode >= 0.01):
        v_v_diode, i_v_diode = module_i_v(temp, irr, v_diode)
        power_vals.append((i_v_diode*v_v_diode, i_v_diode, v_v_diode))
        v_diode+=0.1
    power_vals = sorted(power_vals, key = lambda triple: triple[0])
    starting_point = (power_vals[len(power_vals)-1][2], power_vals[len(power_vals)-1][1])
    #return starting_point
    return hill_climb(temp, irr, starting_point, r_s)


def hill_climb(temp, irr, starting_point, r_s):
    iters = xrange(1, 100,)
    starting_v_d = starting_point[0] + starting_point[1]*r_s
    center_point = starting_v_d
    tup_start = starting_point
    curr_power = starting_point[0]*starting_point[1]
    for x in iters:
        neighbors = [center_point-(1/x), center_point+(1/x)]
        for y in neighbors:
            tup_1 = module_i_v(temp, irr, y)
            if(tup_1[0]*tup_1[1] > curr_power):
                curr_power = tup_1[0]*tup_1[1]
                tup_start = tup_1
                center_point = y
                break
    return tup_start




def read_csv(filename, field_names):
    """load a structured csv file

    Arguments:
        filename {str} -- the path to the file to be loaded
        field_names {List} -- an array of field names in the order of the
                              columns in the csv
    Returns:
        [type] -- [description]
    """
    rtn = []
    with open(filename) as f:
        reader = csv.DictReader(f, fieldnames=field_names)
        reader.next()
        for row in reader:
            rtn.append(row)

    return rtn

def get_parameters(name):
    """get the parameters for a solar module

    Arguments:
        name {str} -- the name of the module you'd like to load
    Returns:
        [dictionary] -- the parameters of the modules
    """
    field_names = ['manufacturer', 'name', 'power', 'i_sc', 'gamma', 'i0',
                   'r_series', 'r_parallel', 'temp_i0']

    all_parameters = read_csv('data.csv', field_names)

    return next(x for x in all_parameters if x['name'] == name)

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_parameters('TSM PA05'))

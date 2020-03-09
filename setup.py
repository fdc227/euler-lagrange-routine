from sympy import *
import pickle
from shape_gen import shape_gen
import numpy as np

generalized_coordinate_list = [] # Will be used to generate q_func, q_func_dt, q_func_dt_dt, q_sym, q_sym_dt, q_sym_dt_dt, should be all strings
dummy_functions = [] # Should be all sympy functions in strings, which represents the dummie functions in the formated functions
T_replace_dict = {} # Should be a dictionary from string of dummy functions to lists of their corresponding replaced terms
U_replace_dict = {}
formated_functions = [] # Should be sympy expressions in strings

########## User programs to fill the above three lists with sympy expressions ############

q_list = []
q_dot_list = []
for i in range(10):
    q_list.append(f'q{i+1}')
    q_dot_list.append(f'q{i+1}_dot')

generalized_coordinate_list += q_list
generalized_coordinate_list += q_dot_list

coefficent_list = ['L', 'EE', 'II', 'rho', 'A']

others_symbols = ['y']
x, y, t = symbols('x, y, t')

dummy_functions = ['k1', 'k2', 'k3', 'k4']
for i in dummy_functions:
    globals()[i] = Function(i)(t)

shapes = shape_gen(4)
for i in range(len(shapes)):
    shapes[i] = shapes[i].subs({x:y})

f = shapes[0]*k1 + shapes[1]*k2 + shapes[2]*k3 + shapes[3]*k4

T_func_format = f'Integral(1/2*rho*A*diff({f}, t, evaluate=False)**2, (y, 0, L))'
U_func_format = f'Integral(1/2*EE*II*diff({f}, (y, 2), evaluate=False)**2, (y, 0, L))'

print(T_func_format)
formated_functions = [T_func_format, U_func_format]

q_list_c = q_list.copy()
q_dot_list_c = q_dot_list.copy()
q_list_c.insert(0, '0')
q_dot_list_c.insert(0, '0')
T_replace_dict['k1'] = q_list_c[0:10]
T_replace_dict['k2'] = q_list_c[1:11]
T_replace_dict['k3'] = q_dot_list_c[0:10]
T_replace_dict['k4'] = q_dot_list_c[1:11]
U_replace_dict['k1'] = q_list_c[0:10]
U_replace_dict['k2'] = q_list_c[1:11]
U_replace_dict['k3'] = q_dot_list_c[0:10]
U_replace_dict['k4'] = q_dot_list_c[1:11]

replace_dict = [T_replace_dict, U_replace_dict]
############ Initial Conditions  ##############

# Assuming r = 10cm = 0.1m
parameter_IC = [1, 10**6, 0.75*10**(-4), 2.7*10**3, 3.14*10**(-2)]
q_IC = []
for i in range(10):
    q_IC.append((i+1)*0.2)
for i in range(10):
    q_IC.append(0.2)
for i in range(20):
    q_IC.append(0)

linear = True
generalized_coordinate_list_expand = [*q_list, *q_dot_list]

parameter_ic_dict = {}
for i in range(len(coefficent_list)):
    parameter_ic_dict[coefficent_list[i]] = parameter_IC[i]

t = np.linspace(0, 10, 100)

IC = [q_IC, parameter_ic_dict, linear, t]

############################################################################

##################  Pickle terms ###########################################

big_container = [generalized_coordinate_list, dummy_functions, replace_dict, formated_functions]

container_raw = open('container.pkl', 'wb')
pickle.dump(big_container, container_raw)

IC_raw = open('IC.pkl', 'wb')
pickle.dump(IC, IC_raw)
import pickle
from string_functions import *

str_raw = open('str_list.pkl', 'rb')
str_list = pickle.load(str_raw)
# print(len(str_list))

(q_str, coeff_str, definitions_str, dummie_func_str, T_repalce_dict_str, T_func_str, U_replace_dict_str, 
U_func_str, q_IC_str, parameter_IC_str, linear_str, t_str) = (str_list[0], str_list[1], str_list[2], str_list[3], 
str_list[4], str_list[5], str_list[6], str_list[7], str_list[8], str_list[9], str_list[10], str_list[11],)
# print(str_list)

q = format1_parsing(q_str)
coeff = format1_parsing(coeff_str)
definitions = format2_parsing(definitions_str)
dummie = format1_parsing(dummie_func_str)
T_replace = format3_parsing(T_repalce_dict_str)
T_func = format4_parsing(T_func_str)
U_replace = format3_parsing(U_replace_dict_str)
U_func = format4_parsing(U_func_str)
q_IC = format5_parsing(q_IC_str)
parameter_IC = format6_parsing(parameter_IC_str)
linearity = format7_parsing(linear_str)
t = format5_parsing(t_str)

print(q)
print(coeff)
print(dummie)
print(definitions)
print(T_replace)
print(T_func)
print(U_replace)
print(U_func)
print(q_IC)
print(parameter_IC)
print(linearity)
print(t)

container = [q, coeff, definitions, dummie, T_replace, T_func, U_replace, U_func, q_IC, parameter_IC, linearity, t]

container_raw = open('container2.pkl', 'wb')
pickle.dump(container, container_raw)


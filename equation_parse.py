from sympy import *
import pickle
from shape_gen import shape_gen
from multiprocessing.pool import Pool
from sympy.physics.mechanics import msubs

container_raw = open('container.pkl', 'rb')
big_container = pickle.load(container_raw)

generalized_coordinates = big_container[0]
dummie_symbols = big_container[1]
replace_list = big_container[2]
formated_functions = big_container[3]

T_replace_list = replace_list[0]
U_replace_list = replace_list[1]

######################################################
###### Sympify strings into symbols / functions ######
######################################################

t = symbols('t')

# generalized_coordinates
q_func = []
q_func_dt = []
q_func_dt_dt = []
q_sym = []
q_sym_dt = []
q_sym_dt_dt = []
for i in generalized_coordinates:
    q_func.append(Function(i)(t))
    q_sym.append(symbols(i))
    q_sym_dt.append(symbols(i+'_dt'))
    q_sym_dt_dt.append(symbols(i+'_dt_dt'))

for i in q_func:
    q_func_dt.append(diff(i, t))
    q_func_dt_dt.append(diff(diff(i, t), t))
# print(q_func_dt_dt)

coordinate_subs = {}
for i in range(len(q_sym)):
    coordinate_subs[q_func_dt_dt[i]] = q_sym_dt_dt[i]
    coordinate_subs[q_func_dt[i]] = q_sym_dt[i]
    coordinate_subs[q_func[i]] = q_sym[i]

# other_functions
dummie_symbol_func = []
for i in dummie_symbols:
    globals()[i] = Function(i)(t)
    dummie_symbol_func.append(globals()[i])

###############           END          ##################

#########################################################
############# Sympify formated functions ################
#########################################################

T = sympify(formated_functions[0])
U = sympify(formated_functions[1])

T_new_replace_dict = {} # Replacing the strings in the replace_dict for sympy functions
U_new_replace_dict = {}
T_new_args = []
U_new_args = []
T_new_values = []
U_new_values = []

for i in T_replace_list:
    if i in dummie_symbols:
        T_new_args.append(dummie_symbol_func[dummie_symbols.index(i)])
    else:
        raise Exception (f'value {i} not in the list of other functions')
for i in U_replace_list:
    if i in dummie_symbols:
        U_new_args.append(dummie_symbol_func[dummie_symbols.index(i)])
    else:
        raise Exception (f'value {i} not in the list of other functions')

for i in T_replace_list:
    value_list = []
    for j in T_replace_list[i]:
        if j in generalized_coordinates:
            value_list.append(q_func[generalized_coordinates.index(j)])
        else:
            value_list.append(sympify(j))
    T_new_values.append(value_list)
for i in U_replace_list:
    value_list = []
    for j in U_replace_list[i]:
        if j in generalized_coordinates:
            value_list.append(q_func[generalized_coordinates.index(j)])
        else:
            value_list.append(sympify(j))
    U_new_values.append(value_list)

for i in range(len(T_new_args)):
    T_new_replace_dict[T_new_args[i]] = T_new_values[i]
for i in range(len(U_new_args)):
    U_new_replace_dict[U_new_args[i]] = U_new_values[i]

T_complete_replace_list = [] # Creating complete detailed replace dictionaries for the substitution function later
for i in range(len(T_new_values[0])):
    local_list = []
    for j in T_new_replace_dict:
        local_list.append((j, T_new_replace_dict[j][i]))
    T_complete_replace_list.append(local_list)
U_complete_replace_list = [] # Creating complete detailed replace dictionaries for the substitution function later
for i in range(len(U_new_values[0])):
    local_list = []
    for j in U_new_replace_dict:
        local_list.append((j, U_new_replace_dict[j][i]))
    U_complete_replace_list.append(local_list)

# Generate the list of T and U expressions by replacing dummie variables with real ones

T_expr = []
U_expr = []
for i in range(len(T_new_values[0])):
    T_expr.append(T.subs(T_complete_replace_list[i]))
for i in range(len(U_new_values[0])):
    U_expr.append(U.subs(U_complete_replace_list[i]))

# print(T_expr)

def T_gen(i):
    T_local = T_expr[i].doit()
    local_list = []
    for j in q_func_dt:
        rs = diff(diff(T_local, j), t)
        local_list.append(msubs(rs, coordinate_subs))
    print(f'Now generating {i+1}/{len(T_expr)} term of T')
    return local_list

def U_gen(i):
    U_local = U_expr[i].doit()
    local_list = []
    for j in q_func:
        rs = diff(U_local, j)
        local_list.append(msubs(rs, coordinate_subs))
    print(f'Now generating {i+1}/{len(U_expr)} term of U')
    return local_list

MP_index = [r for r in range(len(T_expr))]
MP_pool = Pool(len(T_expr))
T_list = MP_pool.map(T_gen, MP_index)
U_list = MP_pool.map(U_gen, MP_index)

T_sf = Matrix(T_list).T.tolist()
U_sf = Matrix(U_list).T.tolist()

T_final = []
U_final = []
for i in T_sf:
    T_final.append(sum(i))
for i in U_sf:
    U_final.append(sum(i))

T_package = [T_final, q_sym_dt_dt]
print(T_final)

T_raw = open('T_package.pkl', 'wb')
U_raw = open('U_final.pkl', 'wb')
pickle.dump(T_package, T_raw)
pickle.dump(U_final, U_raw)

Q_list = [q_sym, q_sym_dt]
Q_raw = open('q_list.pkl', 'wb')
pickle.dump(Q_list, Q_raw)
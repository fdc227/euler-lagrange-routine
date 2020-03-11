from sympy import *
import pickle
from multiprocessing.pool import Pool
from sympy.physics.mechanics import msubs
from string_functions import *

container_raw = open('container2.pkl', 'rb')
container = pickle.load(container_raw)

q = container[0]
dummie = container[3]
T_replace = change_to_qt(container[4], q)
T_format = container[5]
U_replace = change_to_qt(container[6], q)
U_format = container[7]

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
for i in q:
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

#########################################################
############# Sympify formated functions ################
#########################################################

T_strings = []
U_strings = []

# GENERATING STRINGS OF FORMATTED FUNCTIONS WITH DUMMIES REPLACED
for term in T_format:
    T_strings+= function_format_convert(term, T_replace)
for term in U_format:
    U_strings+= function_format_convert(term, U_replace)

tn = len(T_strings)
un = len(U_strings)
# SYMPIFYING THE ABOVE LISTS
# T_expr = []
# U_expr = []
# T_index = [i for i in range(len(T_expr))]


# print(T_expr)

def T_gen(i):
    T_local = sympify(T_strings[i])
    local_list = []
    for j in q_func_dt:
        rs = diff(diff(T_local, j), t)
        local_list.append(msubs(rs, coordinate_subs))
    print(f'Now generating {i+1}/{len(tn)} term of T')
    return local_list

def U_gen(i):
    U_local = sympify(U_strings[i])
    local_list = []
    for j in q_func:
        rs = diff(U_local, j)
        local_list.append(msubs(rs, coordinate_subs))
    print(f'Now generating {i+1}/{len(un)} term of U')
    return local_list

T_index = [r for r in range(len(tn))]
T_pool = Pool(len(tn))
U_index = [r for r in range(len(un))]
U_pool = Pool(len(un))
T_list = T_pool.map(T_gen, T_index)
U_list = U_pool.map(U_gen, U_index)

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
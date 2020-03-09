from sympy import *
import pickle
from sympy import linear_eq_to_matrix

T_raw = open('T_package.pkl', 'rb')
T_package = pickle.load(T_raw)

# print(T_package)
T_final = Matrix(T_package[0])
q_sym_dtdt = T_package[1]

A, b = linear_eq_to_matrix(T_final, q_sym_dtdt)

# print(A)
# print(b)

A_raw = open('A.pkl', 'wb')
pickle.dump(A, A_raw)
b_raw = open('b.pkl', 'wb')
pickle.dump(b, b_raw)
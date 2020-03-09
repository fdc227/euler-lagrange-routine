from sympy import *
import pickle
from sympy.physics.mechanics import msubs
from sympy import linear_eq_to_matrix
import numpy as np
from numpy.linalg import inv, eig
import cmath
from scipy.integrate import odeint

A_raw = open('A.pkl', 'rb')
b_raw = open('b.pkl', 'rb')
IC_raw = open('IC.pkl', 'rb')
q_raw = open('q_list.pkl', 'rb')
U_raw = open('U_final.pkl', 'rb')

A_sym = pickle.load(A_raw)
b_sym = pickle.load(b_raw)
IC = pickle.load(IC_raw)
q_list = pickle.load(q_raw)
U_sym = Matrix(pickle.load(U_raw))

q_IC, parameter_ic_dict, linear, t = IC[0], IC[1], IC[2], IC[3]
q_sym, q_sym_dt = q_list[0], q_list[1]
q_total = []
q_total += q_sym
q_total += q_sym_dt

if linear == True:
    A = A_sym.subs(parameter_ic_dict).tolist()
    C_sym, d_sym = linear_eq_to_matrix(U_sym, q_sym)
    C = C_sym.subs(parameter_ic_dict).tolist()
    A_np = np.array(A, dtype=float)
    C_np = np.array(C, dtype=float)
    M = - np.dot(inv(A_np), C_np)
    w, v = eig(M)
    eig_val = [complex(i) for i in w]
    Q_ = inv(v)
    n = len(q_IC)
    if n != len(q_sym) + len(q_sym_dt):
        raise Exception ('length of q_IC not equal to what it is supposed to be, check the generalized coordniate list')
    M_tilde = np.zeros(shape=(n, n), dtype=np.complex64)
    for i in range(n//2):
        M_tilde[i][2*i] = 1
        M_tilde[i][2*i+1] = 1
        M_tilde[n//2+i][2*i] = np.sqrt(eig_val[i])
        M_tilde[n//2+i][2*i+1] = -np.sqrt(eig_val[i])
    O = np.zeros(shape=(n//2, n//2))
    Q_tilde_upper = np.concatenate((Q_, O), axis=1)    
    Q_tilde_lower = np.concatenate((O, Q_), axis=1)
    Q_tilde_ = np.concatenate((Q_tilde_upper, Q_tilde_lower), axis=0)
    C = np.dot(np.dot(inv(M_tilde), Q_tilde_), q_IC)
    # print(C)
    function_list = [0]*n
    for i in range(n//2):
        function_list[i] = lambda t: np.real(C[i]*np.exp(np.sqrt(eig_val[i])*t) + C[n//2+i]*np.exp(-np.sqrt(eig_val[i])*t))
        function_list[n//2+i] = lambda t: np.real(C[i]*np.sqrt(eig_val[i])*np.exp(np.sqrt(eig_val[i])*t) + C[n//2+i]*(-np.sqrt(eig_val[i]))*np.exp(-np.sqrt(eig_val[i])*t))
    # t = np.linspace(0, 10, 100)
    sol = []
    for f in function_list:
        sol.append(f(t))
else:
    A = A_sym.subs(parameter_ic_dict).tolist()
    b = b_sym.subs(parameter_ic_dict).tolist()
    U = U_sym.subs(parameter_ic_dict).tolist()
    A_np_f = lambdify(q_total, A, 'numpy')
    b_np_f = lambdify(q_total, b, 'numpy')
    U_np_f = lambdify(q_total, U, 'numpy')
    n = len(q_IC)
    def ode_solve(y, t):
        A_np = np.array(A_np_f(*y))
        b_np = np.array(b_np_f(*y))
        U_np = np.array(U_np_f(*y))
        RHS = b_np - U_np
        z_lower = np.dot(inv(A_np), RHS).flatten()
        # print(z_lower)
        z_upper = y[n//2:n]
        z = np.concatenate((z_upper, z_lower), axis=0)
        return z
    # t = np.linspace(0, 10, 100)
    sol = odeint(ode_solve, np.array(q_IC), t)
    
sol_raw = open('sol.pkl', 'wb')
pickle.dump(sol, sol_raw)




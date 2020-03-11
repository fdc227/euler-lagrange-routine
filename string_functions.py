import subprocess
import numpy

# IT CONVERTS A BASH ARRAY INTO A PYTHON LIST
def bash_array_to_python(basharray):
    str_command = 'echo ' + basharray
    l4 = str(subprocess.check_output(str_command, shell=True))
    # print(l4)
    var_str = l4[2:-3]
    var_str_list = var_str.split(' ')
    # print(var_str_list)
    return var_str_list

def numpy_str_to_array(narray_str):
    str_command = 'numpy.' + narray_str + '.astype(float)'
    l = eval(str_command)
    return l

# THE OUTPUT IS A LIST OF ALL THE VARIABLES OF TYPE STRING
def format1_parsing(fstr):
    type_list = fstr.split('//')
    var_str_list = []
    for term in type_list:
        var_str, var_type = term.split('::')[0], term.split('::')[1]
        if var_type.strip().lower() == 'bash':
            var_str_list+=(bash_array_to_python(var_str.strip()))
        elif var_type.strip().lower() == 'python':
            local_list = var_str.replace(' ','').split(',')
            var_str_list+=local_list
        else:
            raise Exception ("Only 'bash' or 'python' type are accepted. Check for typo")
    return var_str_list

# THE OUTPUT IS A DICT OF EXPR_NAME : EXPR_EXPRESSION
def format2_parsing(fstr):
    lines = fstr.split('\n')
    if lines[-1] == '':
        del lines[-1]
    final_dict = {}
    for line in lines:
        sname, sexpr = line.split('=')[0].replace(' ',''), line.split('=')[1].replace(' ', '')
        final_dict[sname] = sexpr
    return final_dict

# THE OUTPUT IS A DICT OF EXPR_NAME : LIST OF VARIABLES IN STRING TYPE
def format3_parsing(fstr):
    lines = fstr.split('\n')
    if lines[-1] == '':
        del lines[-1]
    final_dict = {}
    for line in lines:
        tname, tval = line.split('=')[0].replace(' ',''), line.split('=')[1]
        final_dict[tname] = format1_parsing(tval)
    return final_dict

# THIS RETURNS A LIST OF THE EXPRESISONS PASSED IN
def format4_parsing(fstr):
    lines = fstr.split('\n')
    if lines[-1] == '':
        del lines[-1]
    final_list = []
    for line in lines:
        expr, symb = line.split('::')[0].replace(' ',''), line.split('::')[1].replace(' ','')
        symb_list = symb.split(',')
        final_list.append([expr, symb_list])
    return final_list

# THIS REUTRNS A NUMPY LIST OF ARRAYS PASSED IN
def format5_parsing(fstr):
    lines = fstr.split('//')
    local = []
    for line in lines:
        val, vtype = line.split('::')[0].replace(' ',''), line.split('::')[1].replace(' ','').lower()
        if vtype == 'python':
            val_list = val.split(',')
            local.append(numpy.array(val_list, dtype=float))
        elif vtype == 'numpy':
            local.append(numpy_str_to_array(val))
        else:
            raise Exception ('Only python or numpy types are acceptable, check for typos')
    output = numpy.concatenate(local)
    return output

# SAME AS FORMAT5 EXCEPT IT TAKES LINE CHANGE INTO ACCOUNT
def format6_parsing(fstr):
    lines = fstr.split('\n')
    if lines[-1] == '':
        del lines[-1]
    final = []
    for line in lines:
        final.append(format5_parsing(line))
    output = numpy.concatenate(final)
    return output

def format7_parsing(fstr):
    s = fstr.replace(' ','').lower()
    if s == 'true':
        return True
    elif s == 'false':
        return False
    else:
        raise Exception ('Only true or false can be accepted')

# GIVEN STRING AND TWO SETS, REPLACE THE ELEMENTS FROM OLD_LIST BY THOSE IN NEW_LIST BY CREATING AN ISOMORPHISM BETWEEN THE TWO SETS
def string_replace(_string, old_list, new_list):
    if len(old_list) != len(new_list):
        raise Exception ('Length of two lists must equal')
    n = len(old_list)
    new_string = _string
    for i in range(n):
        new_string = new_string.replace(old_list[i], new_list[i])
    return new_string

# GIVEN A OLD LIST ['K1','K2'] AND A DICTIONARY OF FORMAT {'K1':[NEW_LIST1], 'K2':{NEW_LIST2}}, IT CREATES A LIST OF LISTS WHERE
# EACH ELEMENT IS MADE OF [NEW_LIST1[I], NEW_LIST2[I]], WHERE 'I' IS A INDEX TO LOOP OVER THE LENGTH OF LIST1 
def new_list_gen(old_list, replace_dict):
    final_out = []
    n = len(replace_dict[old_list[0]])
    m = len(old_list)
    for j in range(n):
        local = []
        for i in range(m):
            local.append(replace_dict[old_list[i]][j])
        final_out.append(local)
    return final_out

# IT TAKES THE ABOVE TWO FUNCTIONS AND GENERATES A LIST OF STRINGS WITH DUMMIE VARIABLES BEING REPLACED
def function_format_convert(func_format, replace_dict):
    _string, old_list = func_format[0], func_format[1]
    new_list_list = new_list_gen(old_list, replace_dict)
    final_out = []
    for new_list in new_list_list:
        final_out.append(string_replace(_string, old_list, new_list))
    return final_out

# SIMILAR TO STRING REPLACE, BUT NOW FOR A LIST
def list_replace(in_list, old_list, new_list):
    if len(old_list) != len(new_list):
        raise Exception ('Length of old_list must equal to length of new_list')
    out = []
    em_list = [(i,j) for i, j in enumerate(old_list)]
    em_dict = {}
    for term in em_list:
        em_dict[term[1]] = term[0]
    for i in in_list:
        if i in old_list:
            out.append(new_list[em_dict[i]])
        else:
            out.append(i)
    return out

# CHANGE ELEMENTS IN THE REPLACE_DICT TO FUNCTIONS IF IT IS FOUND IN Q_LIST
def change_to_qt(replace_dict, q_list):
    new_q_list = [x+'(t)' for x in q_list]
    new_dict = {}
    for term in replace_dict:
        new_dict[term] = list_replace(replace_dict[term], q_list, new_q_list)
    return new_dict

if __name__ == "__main__":
    # fstr = 'q{1..10}_dot :: bash // p1, p2, p3 :: python'
    # print(format1_parsing(fstr))

    # fstr2 = 'S1=x**2\nS2=x*y*z'
    # print(format2_parsing(fstr2))

    # fstr3 = 'k1=q{1..10}::bash \nk2=p1, p2, p3, p4 :: python'
    # print(format3_parsing(fstr3))

    # fstr5 = '1,2,3, 4, 5 :: python \n arange(1,10) :: numpy'
    # print(format6_parsing(fstr5))

    # string = 'abcdefg'
    # old = ['a', 'b', 'c', 'd']
    # new = ['1', '2', '3', '4']
    # print(string_replace(string, old, new))

    # old = ['k1','k2']
    replace_dict = {'k1':['q1','q2','q3','q4'], 'k2':['p1','p2','p3','p4']}
    # print(new_list_gen(old, replace_dict))

    # func_format = ['integral(diff(S1*k1+S2*k2,t),x)', ['k1', 'k2']]
    # print(function_format_convert(func_format, replace_dict))

    # l = ['q1','q1','q2','q2','q3']
    # old_list = ['q1','q2','q3']
    # new_list = ['q1(t)', 'q2(t)', 'q3(t)']
    # print(list_replace(l, old_list, new_list))
    q = ['q1','q2','q3','q4','q5', 'p1','p2','p3','p4']
    print(change_to_qt(replace_dict, q))

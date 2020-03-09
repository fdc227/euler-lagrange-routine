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

def string_replace(_string, old_list, new_list):
    if len(old_list) != len(new_list):
        raise Exception ('Length of two lists must equal')
    n = len(old_list)
    new_string = _string
    for i in range(n):
        new_string = new_string.replace(old_list[i], new_list[i])
    return new_string

if __name__ == "__main__":
    # fstr = 'q{1..10}_dot :: bash // p1, p2, p3 :: python'
    # print(format1_parsing(fstr))

    # fstr2 = 'S1=x**2\nS2=x*y*z'
    # print(format2_parsing(fstr2))

    # fstr3 = 'k1=q{1..10}::bash \nk2=p1, p2, p3, p4 :: python'
    # print(format3_parsing(fstr3))

    # fstr5 = '1,2,3, 4, 5 :: python \n arange(1,10) :: numpy'
    # print(format6_parsing(fstr5))

    string = 'abcdefg'
    old = ['a', 'b', 'c', 'd']
    new = ['1', '2', '3', '4']
    print(string_replace(string, old, new))
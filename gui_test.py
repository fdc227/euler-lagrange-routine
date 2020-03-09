import pickle

str_list_raw = open('str_list.pkl', 'rb')
str_list = pickle.load(str_list_raw)

T_replace_dict = str_list[5].split('\n')
print(T_replace_dict)
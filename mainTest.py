from logics import OL

result  = OL.model_checking('(<J3> G ((!r) | (r > (<J3> F a)))) & (<J5> (!r) W a)', '/home/angelo/Desktop/git/VITAMIN/examples/OL/OL_model.txt')
print(result)
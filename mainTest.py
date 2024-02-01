from logics import RABATL

result  = RABATL.model_checking('(<1,2,3><1>F g)', './examples/RABATL/RABATL_model.txt')
print(result)
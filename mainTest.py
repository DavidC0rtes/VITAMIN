from model_checker_interface import RABATL
from model_checker_interface import RBATL
import time

start = time.time()
# result  = RABATL.model_checking('(<1,2,3><2>F h)', './examples/RABATL/RABATL_model.txt')
result  = RBATL.model_checking('(<1,2,3><1>F h)', './examples/RBATL/RBATL_model.txt')
print(result)
print(f'TIME: {time.time()-start} seconds')

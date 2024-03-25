from model_checker_interface.explicit import RABATL
from model_checker_interface.explicit import RBATL
import time

start = time.time()
# result  = RABATL.model_checking('(<1,2,3><5,5>F h)', './examples/RABATL/RABATL_model.txt')
# result  = RBATL.model_checking('(<1,2,3><5,5>F h)', './examples/RBATL/RBATL_model.txt')
result  = RBATL.model_checking('(<1,2><3,1>F p)', './examples/RBATL/sensor_network.txt')
print(result)
print(f'TIME: {time.time()-start} seconds')

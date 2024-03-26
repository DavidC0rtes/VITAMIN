from model_checker_interface.explicit import RABATL
from model_checker_interface.explicit import RBATL
import time

start = time.time()
# result  = RABATL.model_checking('(<1,2,3><5,5>F h)', './examples/RABATL/RABATL_model.txt')
# result  = RBATL.model_checking('(<1,2,3><5,5>F h)', './examples/RBATL/RBATL_model.txt')
phi = '(<1,2><2,1>F p)'
result  = RBATL.model_checking(phi, './examples/RBATL/sensor_network.txt')
print('RBATL')
print(result)
print(f'TIME: {time.time()-start} seconds')

result  = RABATL.model_checking(phi, './examples/RABATL/sensor_network.txt')
print('RABATL')
print(result)
print(f'TIME: {time.time()-start} seconds')

result  = RABATL.model_checking(phi, './examples/RABATL/sensor_network_mod.txt')
print('RABATL mod')
print(result)
print(f'TIME: {time.time()-start} seconds')

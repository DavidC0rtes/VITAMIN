from model_checker_interface.explicit import RABATL
from model_checker_interface.explicit import RBATL
import time


# result  = RABATL.model_checking('(<1,2,3><6,6>F h)', './examples/RABATL/RABATL_model.txt')
result  = RABATL.model_checking('(<1,2><20,20>F p)', './examples/RABATL/sensor_network.txt')
# result  = RBATL.model_checking('(<1,2,3><5,5>F h)', './examples/RBATL/RBATL_model.txt')

# n = 10

# for energy in range(1, n):
#     # for memory in range(1, n):
#     print('Resource bound', energy)
#     # print('Memory resource bound', memory)
#     phi = f'(<1,2><{energy},{energy}>F p)'
#     start = time.time()
#     result  = RBATL.model_checking(phi, './examples/RBATL/sensor_network.txt')
#     print('RBATL')
#     # print(result)
#     print(f'TIME: {time.time()-start} seconds')
    
#     start = time.time()
#     result  = RABATL.model_checking(phi, './examples/RABATL/sensor_network.txt')
#     print('RABATL')
#     # print(result)
#     print(f'TIME: {time.time()-start} seconds')

    # result  = RABATL.model_checking(phi, './examples/RABATL/sensor_network_mod.txt')
    # print('RABATL mod')
    # print(result)
    # print(f'TIME: {time.time()-start} seconds')

from dict_server import *

try:
    dict_pro = ServerBase()
    dict_pro.run_server()
except KeyboardInterrupt:
    print("Bye~~")

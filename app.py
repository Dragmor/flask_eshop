from gevent.pywsgi import WSGIServer
import sys
import multiprocessing
#
from modules.engine import app
from modules.engine import parser_process





if __name__ == '__main__':
    token = None
    arguments = sys.argv
    if len(arguments) > 1:
        if "vk.1." in arguments[1]:
            token = sys.argv[1]
    parser = multiprocessing.Process(target=parser_process, args=(token,))
    parser.start()

    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()

'''
изменить
-в описании товаров сделать ментше текста (в группе)
-запустить сервер по правильному, а не в отладочном режиме
'''
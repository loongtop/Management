from collections import namedtuple

model_handler_tuple = namedtuple('model_handler_tuple', ('model', 'handler'))

name_tuple = namedtuple('name', ('namespace', 'app_name'))

return_url = namedtuple('return_url', ('url_name', 'func', 'cls_name'))



from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail,
                  func)


class CourseHandlerCFG(Retrieve):
    display_list = [func.detail, 'name']
    # pass


handler = get_handler(retrieve=CourseHandlerCFG)

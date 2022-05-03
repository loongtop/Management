from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail,
                  func)


class CourseHandlerCFG(Read):
    display_list = [func.detail, 'name']
    # pass


handler = get_handler(read=CourseHandlerCFG)



from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail,
                  func)


class DepartmentCFG(Read):
    display_list = [func.detail, 'title', func.update_delete]


handler = get_handler(read=DepartmentCFG)



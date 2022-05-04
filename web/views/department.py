from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail,
                  func)


class DepartmentCFG(Retrieve):
    display_list = [func.detail, 'title', func.update_delete]


handler = get_handler(retrieve=DepartmentCFG)

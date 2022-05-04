from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail,
                  func)


class SchoolConfig(Retrieve):
    display_list = [func.detail, 'title', func.update_delete, func.checkbox]

    # pass


handler = get_handler(read=SchoolConfig)



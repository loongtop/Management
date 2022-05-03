from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail,
                  func)


class SchoolConfig(Read):
    display_list = [func.detail, 'title', func.update_delete, func.checkbox]

    # pass


handler = get_handler(read=SchoolConfig)



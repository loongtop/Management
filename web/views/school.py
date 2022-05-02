from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail,
                  fun)


class SchoolConfig(Read):
    display_list = [fun.detail, 'title', fun.update, fun.delete, fun.checkbox]

    # pass


handler = get_handler(read=SchoolConfig)



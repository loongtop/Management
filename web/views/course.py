from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail,
                  fun)


class CourseConfig(Read):
    display_list = [fun.detail, 'name', fun.update_delete, fun.checkbox]
    # pass


handler = get_handler(read=CourseConfig)



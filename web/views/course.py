from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail)


class CourseConfig(Read):
    display_list = ['name']
    # pass


handler = get_handler(read=CourseConfig)



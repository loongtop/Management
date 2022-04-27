from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail)


class SchoolConfig(Read):
    display_list = ['title']


handler = get_handler(read=SchoolConfig)



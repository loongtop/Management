from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail)


class SchoolConfig(Read):
    pass


handler = get_handler(read=SchoolConfig)



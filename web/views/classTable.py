from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail)


class ClassConfig(Retrieve):
    pass


handler = get_handler(read=ClassConfig)



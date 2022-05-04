from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail)


class StudentConfig(Retrieve):
    pass


handler = get_handler(retrieve=StudentConfig)

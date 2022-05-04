from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail)


class CustomerConfig(Retrieve):
    pass


handler = get_handler(read=CustomerConfig)



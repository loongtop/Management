from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail)


class CustomerConfig(Read):
    pass


handler = get_handler(read=CustomerConfig)



from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail)


class EmployeeConfig(Read):
    pass


handler = get_handler(read=EmployeeConfig)



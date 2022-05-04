from crud import (get_site, get_handler,
                  Create, Retrieve, Update, Delete, Detail)


class StudentConfig(Retrieve):
    def show(self):
        print


handler = get_handler(read=StudentConfig)



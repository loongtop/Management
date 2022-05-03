from crud import (get_site, get_handler,
                  Create, Read, Update, Delete, Detail)


class StudentConfig(Read):
    def show(self):
        print


handler = get_handler(read=StudentConfig)



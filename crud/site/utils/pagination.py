"""
pagination component
"""


class Pagination(object):
    """
    pagination component
    """

    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11):
        """
         paging initialization
         :param current_page: current page number
         :param per_page: the number of data bars displayed per page
         :param all_count: The total number of records in the database
         :param base_url: base URL
         :param query_params: QueryDict object, which contains all the original conditions of the current URL
         :param pager_page_count: The maximum number of pages displayed on the page
        """
        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                raise Exception()
        except Exception as e:
            self.current_page = 1
        self.query_params = query_params
        self.per_page = per_page
        self.all_count = all_count
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):
        """
        Data acquisition value start index
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        data get value end index
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        Generate HTML page numbers
        :return:
        """
        # If data total pager_count<11 pager_page_count
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # The data page number has exceeded 11
            # if current page <= 5 half_pager_page_count
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:
                # If: current page+5 > total page number
                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_end = self.pager_count
                    pager_start = self.pager_count - self.pager_page_count + 1
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []

        if self.current_page <= 1:
            prev = '<li><a href="#">prev.</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev = '<li><a href="%s?%s">prev.</a></li>' % (self.base_url, self.query_params.urlencode())
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="active"><a href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            else:
                tpl = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.query_params.urlencode(), i,)
            page_list.append(tpl)

        if self.current_page >= self.pager_count:
            nex = '<li><a href="#">next</a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            nex = '<li><a href="%s?%s">next</a></li>' % (self.base_url, self.query_params.urlencode(),)
        page_list.append(nex)
        page_str = "".join(page_list)
        return page_str

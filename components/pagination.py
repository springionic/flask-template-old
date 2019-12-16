# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/16

class Pagination(object):
    def __init__(self, current_page, page_size, total, items):
        self.current_page = current_page
        if self.current_page < 1:
            self.current_page = 1

        self.page_size = page_size
        if self.page_size < 1:
            self.page_size = 1

        self.total = total
        self.list = items
        self.page_total = self._get_page_total()

        if current_page > self.page_total:
            self.current_page = self.page_total

    def _get_page_total(self):
        if self.total % self.page_size == 0:
            page_total = int(self.total / self.page_size)
        else:
            page_total = int(self.total / self.page_size) + 1

        return page_total if page_total > 1 else 1

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __str__(self):
        return str(self.__dict__)

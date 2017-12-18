# -*- coding: utf-8 -*-
from datetime import datetime as dt
from typing import List


class User(object):
    def __init__(
        self,
        id: int,
        username: str,
        display_name: str,
        company: str,
        email_address: str='',
        first_name: str='',
        last_name: str='',
    ) -> None:
        self.id = id
        self.username = username
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.company = company


class Pagination(object):
    def __init__(
        self,
        first_id: int,
        last_id: int,
        current_id: int,
    ) -> None:
        self.first_id = first_id
        self.last_id = last_id
        self.current_id = current_id


class APIinfos(object):
    def __init__(
        self,
        version: str,
        datetime: dt
    ) -> None:
        self.version = version
        self.datetime = datetime


class ListUser(object):
    def __init__(
        self,
        item_nb: int,
        items: List[User],
        pagination=Pagination,
    ) -> None:
        self.item_nb = item_nb
        self.items = items
        self.pagination = pagination

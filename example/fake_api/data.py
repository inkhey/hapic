from datetime import datetime

from example.fake_api.model import User, Pagination, APIinfos, ListUser

EXAMPLE_USER = User(
    id=4,
    username='some_user',
    display_name='Damien Accorsi',
    company='Algoo',
    email_address='some.user@hapic.com',
    first_name='Damien',
    last_name='Accorsi',
)
EXAMPLE_PAGINATION = Pagination(
    first_id=0,
    last_id=5,
    current_id=0,
)
EXAMPLE_API_INFOS = APIinfos(
    version='1.2.3',
    datetime= datetime(2017, 12, 7, 10, 55, 8, 488996),
)
EXAMPLE_LIST_USER = ListUser(
    item_nb=1,
    items=[EXAMPLE_USER,],
    pagination=EXAMPLE_PAGINATION,
)

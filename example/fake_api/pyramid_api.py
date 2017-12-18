# -*- coding: utf-8 -*-
import json
from http import HTTPStatus
from pyramid.response import Response
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
import time
from datetime import datetime

from example.fake_api.data import EXAMPLE_USER
from example.fake_api.data import EXAMPLE_API_INFOS
from example.fake_api.data import EXAMPLE_LIST_USER
from hapic import Hapic
from example.fake_api.schema import *

from hapic.data import HapicData
from hapic.ext.pyramid import PyramidContext

hapic = Hapic()


class PyramidController(object):
    @hapic.with_api_doc()
    @hapic.output_body(AboutResponseSchema())
    def about(self, context, request):
        """
        General information about this API.
        """
        return EXAMPLE_API_INFOS

    @hapic.with_api_doc()
    @hapic.output_body(ListsUserSchema())
    def get_users(self, context, request):
        """
        Obtain users list.
        """
        return EXAMPLE_LIST_USER

    @hapic.with_api_doc()
    @hapic.input_path(UserPathSchema())
    @hapic.output_body(UserSchema())
    def get_user(self, context, request, hapic_data: HapicData):
        """
        Obtain one user
        """
        return EXAMPLE_USER

    @hapic.with_api_doc()
    # TODO - G.M - 2017-12-5 - Support input_forms ?
    # TODO - G.M - 2017-12-5 - Support exclude, only ?
    # @hapic.input_body(UserSchema(exclude=('id',)))
    @hapic.input_body(UnumberedUserSchema())
    @hapic.output_body(UserSchema())
    def add_user(self, context, request, hapic_data: HapicData):
        """
        Add new user
        """
        return EXAMPLE_USER

    @hapic.with_api_doc()
    @hapic.output_body(NoContentSchema(),
                       default_http_code=204)
    @hapic.input_path(UserPathSchema())
    def del_user(self, context, request, hapic_data: HapicData):
        """
        delete user
        """
        return NoContentSchema()

    def bind(self, configurator: Configurator):
        configurator.add_route('about', '/about', request_method='GET')
        configurator.add_view(self.about, route_name='about', renderer='json')

        configurator.add_route('get_users', '/users', request_method='GET')  # nopep8
        configurator.add_view(self.get_users, route_name='get_users', renderer='json')  # nopep8

        configurator.add_route('get_user', '/users/{id}', request_method='GET')  # nopep8
        configurator.add_view(self.get_user, route_name='get_user', renderer='json')  # nopep8

        configurator.add_route('add_user', '/users/', request_method='POST')  # nopep8
        configurator.add_view(self.add_user, route_name='add_user', renderer='json')  # nopep8

        configurator.add_route('del_user', '/users/{id}', request_method='DELETE')  # nopep8
        configurator.add_view(self.del_user, route_name='del_user', renderer='json')  # nopep8

if __name__ == "__main__":
    configurator = Configurator(autocommit=True)
    controllers = PyramidController()
    controllers.bind(configurator)
    hapic.set_context(PyramidContext(configurator))
    time.sleep(1)
    s = json.dumps(
        hapic.generate_doc(
            title='Fake API',
            description='just an example of hapic API'
        )
    )
    time.sleep(1)
    # print swagger doc
    print(s)
    # Run app
    server = make_server('0.0.0.0', 8083, configurator.make_wsgi_app())
    server.serve_forever()

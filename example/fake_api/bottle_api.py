# -*- coding: utf-8 -*-
import json
from http import HTTPStatus

import bottle
import time

from example.fake_api.data import EXAMPLE_USER
from example.fake_api.data import EXAMPLE_API_INFOS
from example.fake_api.data import EXAMPLE_LIST_USER
from hapic import Hapic
from example.fake_api.schema import *
from hapic.data import HapicData
from hapic.ext.bottle import BottleContext

hapic = Hapic()


class BottleController(object):
    @hapic.with_api_doc()
    @hapic.output_body(AboutResponseSchema())
    def about(self):
        """
        General information about this API.
        """
        return EXAMPLE_API_INFOS

    @hapic.with_api_doc()
    @hapic.output_body(ListsUserSchema())
    def get_users(self):
        """
        Obtain users list.
        """
        return EXAMPLE_LIST_USER

    @hapic.with_api_doc()
    @hapic.input_path(UserPathSchema())
    @hapic.output_body(UserSchema())
    def get_user(self, id, hapic_data: HapicData):
        """
        Obtain one user
        """
        return EXAMPLE_USER

    @hapic.with_api_doc()
    # TODO - G.M - 2017-12-5 - Support input_forms ?
    # TODO - G.M - 2017-12-5 - Support exclude, only ?
    # @hapic.input_body(NumberedUserSchema(exclude=('id',)))
    @hapic.input_body(UnumberedUserSchema())
    @hapic.output_body(UserSchema())
    def add_user(self, hapic_data: HapicData):
        """
        Add new user
        """
        return EXAMPLE_USER

    @hapic.with_api_doc()
    @hapic.output_body(NoContentSchema(),
                       default_http_code=204)
    @hapic.input_path(UserPathSchema())
    def del_user(self, id, hapic_data: HapicData):
        """
        delete user
        """
        return NoContentSchema()

    def bind(self, app:bottle.Bottle):
        app.route('/about', callback=self.about)
        app.route('/users', callback=self.get_users)
        app.route('/users/<id>', callback=self.get_user)
        app.route('/users/', callback=self.add_user,  method='POST')
        app.route('/users/<id>', callback=self.del_user, method='DELETE')

if __name__ == "__main__":
    app = bottle.Bottle()
    controllers = BottleController()
    controllers.bind(app)
    hapic.set_context(BottleContext(app))
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
    app.run(host='localhost', port=8081, debug=True)

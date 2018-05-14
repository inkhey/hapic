# -*- coding: utf-8 -*-
import json
import re
import typing

try:  # Python 3.5+
    from http import HTTPStatus
except ImportError:
    from http import client as HTTPStatus

from hapic.context import BaseContext
from hapic.context import RouteRepresentation
from hapic.decorator import DecoratedController
from hapic.decorator import DECORATION_ATTRIBUTE_NAME
from hapic.exception import OutputValidationException
from hapic.processor import RequestParameters
from hapic.processor import ProcessValidationError
from hapic.error import DefaultErrorBuilder
from hapic.error import ErrorBuilderInterface
from flask import Flask
from flask import send_from_directory

if typing.TYPE_CHECKING:
    from flask import Response

# flask regular expression to locate url parameters
FLASK_RE_PATH_URL = re.compile(r'<(?:[^:<>]+:)?([^<>]+)>')


class FlaskContext(BaseContext):
    def __init__(
        self,
        app: Flask,
        default_error_builder: ErrorBuilderInterface=None,
    ):
        self._handled_exceptions = []  # type: typing.List[HandledException]  # nopep8
        self.app = app
        self.default_error_builder = \
            default_error_builder or DefaultErrorBuilder()  # FDV

    def get_request_parameters(self, *args, **kwargs) -> RequestParameters:
        from flask import request
        return RequestParameters(
            path_parameters=request.view_args,
            query_parameters=request.args,  # TODO: Check
            body_parameters=request.get_json(),  # TODO: Check
            form_parameters=request.form,
            header_parameters=request.headers,
            files_parameters=request.files,
        )

    def get_response(
        self,
        response: str,
        http_code: int,
        mimetype: str='application/json',
    ) -> 'Response':
        from flask import Response
        return Response(
            response=response,
            mimetype=mimetype,
            status=http_code,
        )

    def get_validation_error_response(
        self,
        error: ProcessValidationError,
        http_code: HTTPStatus=HTTPStatus.BAD_REQUEST,
    ) -> typing.Any:
        error_content = self.default_error_builder.build_from_validation_error(
            error,
        )

        # Check error
        dumped = self.default_error_builder.dump(error).data
        unmarshall = self.default_error_builder.load(dumped)

        if unmarshall.errors:
            raise OutputValidationException(
                'Validation error during dump of error response: {}'.format(
                    str(unmarshall.errors)
                )
            )
        from flask import Response
        return Response(
            response=json.dumps(error_content),
            mimetype='application/json',
            status=int(http_code),
        )

    def find_route(
        self,
        decorated_controller: 'DecoratedController',
    ):
        reference = decorated_controller.reference
        for route in self.app.url_map.iter_rules():
            if route.endpoint not in self.app.view_functions:
                continue
            route_callback = self.app.view_functions[route.endpoint]
            route_token = getattr(
                route_callback,
                DECORATION_ATTRIBUTE_NAME,
                None,
            )
            match_with_wrapper = route_callback == reference.wrapper
            match_with_wrapped = route_callback == reference.wrapped
            match_with_token = route_token == reference.token

            # FIXME - G.M - 2017-12-04 - return list instead of one method
            # This fix, return only 1 allowed method, change this when
            # RouteRepresentation is adapted to return multiples methods.
            method = [x for x in route.methods
                      if x not in ['OPTIONS', 'HEAD']][0]

            if match_with_wrapper or match_with_wrapped or match_with_token:
                return RouteRepresentation(
                    rule=self.get_swagger_path(route.rule),
                    method=method,
                    original_route_object=route,
                )

    def get_swagger_path(self, contextualised_rule: str) -> str:
        # TODO - G.M - 2017-12-05 Check if all route path are handled correctly
        return FLASK_RE_PATH_URL.sub(r'{\1}', contextualised_rule)

    def by_pass_output_wrapping(self, response: typing.Any) -> bool:
        from flask import Response
        return isinstance(response, Response)

    def add_view(
        self,
        route: str,
        http_method: str,
        view_func: typing.Callable[..., typing.Any],
    ) -> None:
        self.app.add_url_rule(
            methods=[http_method],
            rule=route,
            view_func=view_func,
        )

    def serve_directory(
        self,
        route_prefix: str,
        directory_path: str,
    ) -> None:
        if not route_prefix.endswith('/'):
            route_prefix = '{}/'.format(route_prefix)

        @self.app.route(
            route_prefix,
            defaults={
                'path': 'index.html',
            }
        )
        @self.app.route(
            '{}<path:path>'.format(route_prefix),
        )
        def api_doc(path):
            return send_from_directory(directory_path, path)

    def _add_exception_class_to_catch(
        self,
        exception_class: typing.Type[Exception],
        http_code: int,
    ) -> None:
        raise NotImplementedError('TODO')

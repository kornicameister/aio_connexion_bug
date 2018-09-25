import typing as t
import ujson

import connexion
from aiohttp import web


async def greeting_bug(
    name: str,
    query_a: str,
    query_b: t.Optional[str],
) -> web.Response:
    print(f'name is {name}')
    print(f'query_a is {query_a}')
    print(f'query_b is {query_b}')

    assert query_a == 'query_a', f'Bug here, query_a was suppose to equal "query_a", but it is "{query_a}"'
    assert query_b == 'query_b', f'Bug here, query_a was suppose to equal "query_b", but it is "{query_b}"'

    return web.Response(body=name)


@web.middleware
async def print_query_middleware(
    request: web.Request,
    handler: t.Callable[[web.Request], web.Response],
) -> web.Response:
    # this show that query params at aiohttp level are correct
    print(f'query_params_middleware={request.query}')
    resp = await handler(request)
    return resp


c_app = connexion.AioHttpApp(
    __name__,
    only_one_api=True,
    debug=True,
    options={
        'uri_parsing_class': connexion.decorators.uri_parsing.Swagger2URIParser,
    },
    middlewares=[print_query_middleware]
)
c_app.add_api(
    'swagger.yaml',
    strict_validation=True,
    validate_responses=True,
    pythonic_params=True,
)
c_app.run(host='0.0.0.0', port=3000)

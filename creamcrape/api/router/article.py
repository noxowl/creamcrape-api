from flask import Blueprint, current_app, make_response, request, g

from creamcrape.common import pack, status_code
from creamcrape.logic.article import create as article_create, get as article_get

article_app = Blueprint('article', __name__)


@article_app.route('/<api_version>/articles', methods=['GET'])
def get_articles_by_category(api_version: str) -> tuple:
    """
    get article by category

    :param api_version: api version for client control
    :return: response tuple
    """
    try:
        if 'category' in request.args:
            category = str(request.args.get('category'))
        else:
            category = str(0)
        result = article_get.get_latest_articles(category_id=category)
        return pack(result), 200
    except ValueError:
        current_app.abort(status_code.bad_request)


@article_app.route('/<api_version>/articles/<article_hash>', methods=['GET'])
def get_article(api_version: str, article_hash: str) -> tuple:
    """
    get article by id

    :param api_version: api version for client control
    :param article_hash: target article hash
    :return: response tuple
    """
    current_app.log.debug(article_hash)
    result = article_get.get_article(article_hash)
    return pack(result), 200


@article_app.route('/<api_version>/articles/<article_hash>/responses', methods=['GET'])
def get_responses(api_version: str, article_hash: str) -> tuple:
    """
    get responses in article

    :param api_version: api version for client control
    :param article_hash: target article id
    :return: response tuple
    """
    try:
        if 'offset' in request.args and 'limit' in request.args:
            offset = int(request.args.get('offset'))
            limit = int(request.args.get('limit'))
        else:
            offset = 0
            limit = 0
        result = article_get.get_response(article_hash=article_hash, offset=offset, limit=limit)
        return pack(result), 200
    except ValueError:
        current_app.abort(status_code.bad_request)


@article_app.route('/<api_version>/articles', methods=['POST'])
def create_article(api_version: str) -> tuple:
    """
    create article

    :param api_version: api version for client control
    :return: response tuple
    """
    if current_app.config['DEBUG']:
        payload = request.json
    else:
        payload = request.msgpack
    if not payload:
        current_app.abort(status_code.bad_request)
    result = article_create.create_article(payload)
    return pack(result), 200


@article_app.route('/<api_version>/articles/<article_hash>/responses', methods=['POST'])
def create_resposne(api_version: str, article_hash: str) -> tuple:
    """
    create response

    :param api_version: api version for client control
    :param article_id: target article id
    :return: response tuple
    """
    if current_app.config['DEBUG']:
        payload = request.json
    else:
        payload = request.msgpack
    if not payload:
        current_app.abort(status_code.bad_request)
    result = article_create.create_response(article_hash, payload)
    return pack(result), 200

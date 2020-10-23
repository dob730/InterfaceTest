import urllib.parse as urlparse
from urllib.parse import urlencode
from urllib.parse import unquote

class UrlParamPaser:

    def get_url(self, path, params):
        url_parts = list(urlparse.urlparse(path))  # 將 URL 解析六個组件，存放在list
        query = dict(urlparse.parse_qsl(url_parts[4]))  # 將query parameter to dict
        query.update(params)  # 將參數加入query的dict中
        url_parts[4] = urlencode(query)
        url_parts[4] = unquote(url_parts[4])
        url = urlparse.urlunparse(url_parts)
        return url

import json
import http.client
from http import HTTPStatus
from urllib.parse import urlparse

class CLOVAStudioExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request, endpoint):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        parsed_url = urlparse(self._host)
        conn = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)
        conn.request('POST', endpoint, json.dumps(completion_request), headers)
        response = conn.getresponse()
        status = response.status
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result, status

    def execute(self, completion_request, endpoint):
        res, status = self._send_request(completion_request, endpoint)
        if status == HTTPStatus.OK:
            return res, status
        else:
            error_message = res.get("status", {}).get("message", "Unknown error") if isinstance(res, dict) else "Unknown error"
            raise ValueError(f"오류 발생: HTTP {status}, 메시지: {error_message}")

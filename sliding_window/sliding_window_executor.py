import json
import http.client
from http import HTTPStatus
from urllib.parse import urlparse
from clovastudio_executor import CLOVAStudioExecutor

class SlidingWindowExecutor(CLOVAStudioExecutor):
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        super().__init__(host, api_key, api_key_primary_val, request_id)

    def execute(self, completion_request):
        # URL에서 호스트명과 포트를 분리
        parsed_url = urlparse(self._host)
        conn = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)

        endpoint = '/testapp/v1/api-tools/sliding/chat-messages/HCX-003/x56zk6qy'  # 이 부분을 올바르게 설정해야 함
        try:
            result, status = self._send_request(completion_request, endpoint)
            if status == 200:
                # 슬라이딩 윈도우 적용 후 메시지를 반환
                return result['result']['messages']
            else:
                error_message = result.get('status', {}).get('message', 'Unknown error')
                raise ValueError(f"오류 발생: HTTP {status}, 메시지: {error_message}")
        except Exception as e:
            print(f"Error in SlidingWindowExecutor: {e}")
            return 'Error'


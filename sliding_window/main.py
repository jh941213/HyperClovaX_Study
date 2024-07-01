from sliding_window_executor import SlidingWindowExecutor
from clova import LlmClovaStudio
import json

# 스트리밍 응답에서 content 부분만 추출
def parse_stream_response(response):
    content_parts = []
    for line in response.splitlines():
        if line.startswith('data:'):
            data = json.loads(line[5:])
            if 'message' in data and 'content' in data['message']:
                content_parts.append(data['message']['content'])
    content = content_parts[-1] if content_parts else ""
    return content.strip()

# 논스트리밍 응답에서 content 부분만 추출
def parse_non_stream_response(response):
    result = response.get('result', {})
    message = result.get('message', {})
    content = message.get('content', '')
    return content.strip()

def main():
    # 초기 시스템 프롬프트 설정
    system_prompt = "- HyperCLOVA X는 네이버 클라우드의 하이퍼스케일 AI입니다."
    messages = []

    sliding_window_executor = SlidingWindowExecutor(
        host='https://clovastudio.stream.ntruss.com/',
        api_key='NTA0MjU2MWZlZTcxNDJiY6yyY6Iahpvy/4bDhr2mfucbZv7a0mH3ZmXd45WiAT5+',
        api_key_primary_val='J300G5CdzwUakQQHTMBDjs7GP7buywJcqSOLGP47',
        request_id='bc5346c1-1ba7-41cb-921a-fdc0e3d64530'
    )

    clova_studio_llm = LlmClovaStudio(
        host='https://clovastudio.stream.ntruss.com/',
        api_key='NTA0MjU2MWZlZTcxNDJiY6yyY6Iahpvy/4bDhr2mfucbZv7a0mH3ZmXd45WiAT5+',
        api_key_primary_val='J300G5CdzwUakQQHTMBDjs7GP7buywJcqSOLGP47',
        request_id='bc5346c1-1ba7-41cb-921a-fdc0e3d64530'
    )

    while True:
        user_input = input("USER: ('exit'으로 종료): ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages.append({"role": "user", "content": user_input})

        request_data = {
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "maxTokens": 100
        }

        # SlidingWindowExecutor를 사용하여 조정된 메시지 가져오기
        try:
            adjusted_messages = sliding_window_executor.execute(request_data)
            if adjusted_messages == 'Error':
                print("Error adjusting messages with SlidingWindowExecutor")
                continue
        except Exception as e:
            print(f"Error adjusting messages: {e}")
            continue

        # Chat Completion 요청 데이터 생성
        completion_prompt = '\n'.join([msg['content'] for msg in adjusted_messages])
        
        try:
            response_text = clova_studio_llm._call(completion_prompt)

            messages.append({"role": "assistant", "content": response_text})

            # 대화 내역 표시
            print("\nAdjusted Messages:", adjusted_messages, "\n")
            print("System Prompt:", system_prompt)
            print("USER Input:", user_input)
            print("CLOVA Response:", response_text, "\n")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

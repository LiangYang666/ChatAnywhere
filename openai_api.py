import json

import requests


def get_response_stream_generate_from_ChatGPT_API(text, apikey, message_history,
                                                  model="gpt-3.5-turbo", temperature=0.9, presence_penalty=0, max_tokens=2000):
    """
    从ChatGPT API获取回复
    :param apikey:
    :param text: 用户输入的文本
    :param message_history: 消息历史
    :param model: 模型
    :param temperature: 温度
    :param presence_penalty: 惩罚
    :param max_tokens: 最大token数量
    :return: 回复生成器
    """
    if apikey is None:
        print("apikey is None")
        return

    message_prompt = [{"role": "system", "content": "你是一个AI文本补全助手，用户输入一段文字，你需要对文字内容进行补全，补全150字以内"}]
    message_context = message_prompt + [{"role": "user", "content": text}]

    header = {"Content-Type": "application/json",
              "Authorization": "Bearer " + apikey}

    data = {
        "model": model,
        "temperature": temperature,
        "presence_penalty": presence_penalty,
        "max_tokens": max_tokens,
        "messages": message_context,
        "stream": True
    }
    print("开始流式请求")
    url = "https://api.openai.com/v1/chat/completions"
    # 请求接收流式数据 动态print
    try:
        response = requests.request("POST", url, headers=header, json=data, stream=True)

        def generate():
            stream_content = str()
            one_message = {"role": "assistant", "content": stream_content}
            message_history.append(one_message)
            i = 0
            for line in response.iter_lines():
                # print(str(line))
                line_str = str(line, encoding='utf-8')
                if line_str.startswith("data:"):
                    if line_str.startswith("data: [DONE]"):
                        return
                    line_json = json.loads(line_str[5:])
                    if 'choices' in line_json:
                        if len(line_json['choices']) > 0:
                            choice = line_json['choices'][0]
                            if 'delta' in choice:
                                delta = choice['delta']
                                if 'role' in delta:
                                    role = delta['role']
                                elif 'content' in delta:
                                    delta_content = delta['content']
                                    i += 1
                                    if i < 40:
                                        print(delta_content, end="")
                                    elif i == 40:
                                        print("......")
                                    one_message['content'] = one_message['content'] + delta_content
                                    yield delta_content

                elif len(line_str.strip()) > 0:
                    print(line_str)
                    yield line_str

    except Exception as e:
        ee = e
        def generate():
            yield "request error:\n" + str(ee)

    return generate


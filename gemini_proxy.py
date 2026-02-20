#!/usr/bin/env python3
"""
Gemini OpenAI 兼容中转服务
在本地运行，将 OpenAI 格式的请求转发给 Google Gemini API
解决国内网络访问问题（如果运行在能访问外网的环境）
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Gemini API 配置
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAcbuXFpSrVtWRHK7cnUgZlmuzOkFgSPNU")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "gemini-proxy"})

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """OpenAI 兼容的聊天完成端点"""

    # 获取请求数据
    data = request.get_json()

    # 构建 Gemini 请求
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': GEMINI_API_KEY
    }

    # 将 OpenAI 格式转换为 Gemini 格式
    gemini_request = {
        'model': data.get('model', 'gemini-2.0-flash'),
        'messages': data.get('messages', []),
    }

    # 添加可选参数
    if 'temperature' in data:
        gemini_request['temperature'] = data['temperature']
    if 'max_tokens' in data:
        gemini_request['max_tokens'] = data['max_tokens']
    if 'stream' in data:
        gemini_request['stream'] = data['stream']

    # 发送到 Gemini API
    url = f"{GEMINI_BASE_URL}/chat/completions"

    try:
        response = requests.post(
            url,
            headers=headers,
            json=gemini_request,
            timeout=60
        )

        # 返回 Gemini 的响应
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": {
                "message": f"代理请求失败: {str(e)}",
                "type": "proxy_error",
                "code": "proxy_error"
            }
        }), 500

@app.route('/v1/models', methods=['GET'])
def list_models():
    """列出可用模型"""
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "gemini-2.0-flash",
                "object": "model",
                "owned_by": "google"
            },
            {
                "id": "gemini-2.5-flash",
                "object": "model",
                "owned_by": "google"
            },
            {
                "id": "gemini-1.5-pro",
                "object": "model",
                "owned_by": "google"
            }
        ]
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Gemini API 中转服务启动")
    print("=" * 50)
    print(f"API Key: {GEMINI_API_KEY[:20]}...")
    print(f"监听地址: http://127.0.0.1:8888")
    print(f"聊天端点: http://127.0.0.1:8888/v1/chat/completions")
    print("=" * 50)
    print("\n配置肥牛.exe 使用:")
    print("  API URL: http://127.0.0.1:8888/v1")
    print("  API Key: {任意值，留空也可}")
    print("=" * 50)

    app.run(host='0.0.0.0', port=8888, debug=False)

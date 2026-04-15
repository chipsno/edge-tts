import requests
import json
import os

# --- 配置项 ---
# 替换为您部署后的域名，例如: https://your-worker.workers.dev
BASE_URL = "http://localhost:8787" 
# 输入我刚才为您生成的 API Key
API_KEY = "sk-v2f8nm9k4j2p7q5rw3x1z6t8b0y9m5n1"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def text_to_speech(text, output_file="output.mp3", voice="zh-CN-XiaoxiaoNeural"):
    """
    文字转语音示例 (TTS)
    """
    print(f"正在转换文字: {text[:20]}...")
    url = f"{BASE_URL}/v1/audio/speech"
    
    payload = {
        "input": text,
        "voice": voice,
        "speed": 1.0,
        "pitch": 0,
        "style": "general"
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"✅ 转换成功！音频已保存至: {output_file}")
        else:
            print(f"❌ 转换失败 ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ 请求发生异常: {e}")

def transcribe_audio(audio_file_path):
    """
    语音转文字示例 (Transcription)
    """
    if not os.path.exists(audio_file_path):
        print(f"❌ 文件不存在: {audio_file_path}")
        return

    print(f"正在转录音频: {audio_file_path}...")
    url = f"{BASE_URL}/v1/audio/transcriptions"
    
    # 鉴权头（Multipart 请求由 requests 自动处理 Content-Type）
    auth_headers = {"x-api-key": API_KEY}
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {"file": audio_file}
            response = requests.post(url, headers=auth_headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 转录成功！结果: \n{result[0]['text']}") # 针对 SiliconFlow 的返回格式适配
        else:
            print(f"❌ 转录失败 ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ 请求发生异常: {e}")

if __name__ == "__main__":
    # --- 测试流程 ---
    print("=== Edge TTS API 鉴权测试 ===")
    
    # 1. 测试 TTS
    text_to_speech("你好，这是一个带有 API Key 认证的接口调用测试。")
    
    # 2. 测试 STT (如果本地有文件，填入路径尝试)
    # transcribe_audio("test.mp3")

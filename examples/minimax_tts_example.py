"""
MiniMax 同步语音合成 HTTP API 调用示例
文档：https://platform.minimaxi.com/docs/api-reference/speech-t2a-http
"""
import requests
import json
import base64
from pathlib import Path


def text_to_speech(
    api_key: str,
    text: str,
    model: str = "speech-2.6-hd",
    voice_id: str = "Chinese (Mandarin)_Warm_Girl",
    emotion: str = "calm",
    pronunciation_dict: dict = None,
    output_file: str = "output.mp3"
):
    """
    调用 MiniMax 同步语音合成 API
    
    参数:
        api_key: MiniMax API Key
        text: 要合成的文本（长度 < 10000 字符）
        model: 模型版本（speech-2.6-hd, speech-2.6-turbo 等）
        voice_id: 音色ID（如 Chinese (Mandarin)_Warm_Girl）
        emotion: 情感（calm, happy, sad, angry, fear, surprise, neutral）
        pronunciation_dict: 发音字典，格式：{"tone": ["处理/(chu3)(li3)", "危险/dangerous"]}
        output_file: 输出音频文件名
    """
    url = "https://api.minimaxi.com/v1/t2a_v2"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1,      # 语速：0.5-2.0
            "vol": 1,        # 音量：0.0-2.0
            "pitch": 0,      # 音调：-12 到 12
            "emotion": emotion  # 情感：calm, happy, sad, angry, fear, surprise, neutral
        },
        "audio_setting": {
            "sample_rate": 32000,  # 采样率：16000, 24000, 32000, 44100, 48000
            "bitrate": 128000,     # 比特率
            "format": "mp3",       # 格式：mp3, wav, flac
            "channel": 1           # 声道：1(单声道), 2(立体声)
        },
        "subtitle_enable": False,
        "output_format": "hex"  # hex 或 url
    }
    
    # 添加发音字典（如果提供）
    if pronunciation_dict:
        payload["pronunciation_dict"] = pronunciation_dict
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # 检查响应状态
        if result.get("base_resp", {}).get("status_code") != 0:
            error_msg = result.get("base_resp", {}).get("status_msg", "Unknown error")
            raise Exception(f"API Error: {error_msg}")
        
        # 获取音频数据（hex编码）
        audio_hex = result.get("data", {}).get("audio")
        if not audio_hex:
            raise Exception("No audio data in response")
        
        # 将 hex 编码转换为二进制
        audio_bytes = bytes.fromhex(audio_hex)
        
        # 保存音频文件
        output_path = Path(output_file)
        output_path.write_bytes(audio_bytes)
        
        # 打印额外信息
        extra_info = result.get("extra_info", {})
        print(f"✅ 语音合成成功！")
        print(f"📁 保存位置: {output_path.absolute()}")
        print(f"📊 音频信息:")
        print(f"   - 时长: {extra_info.get('audio_length', 0) / 1000:.2f} 秒")
        print(f"   - 大小: {extra_info.get('audio_size', 0) / 1024:.2f} KB")
        print(f"   - 格式: {extra_info.get('audio_format', 'unknown')}")
        print(f"   - 采样率: {extra_info.get('audio_sample_rate', 0)} Hz")
        print(f"   - 字数: {extra_info.get('word_count', 0)}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应内容: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        raise


def text_to_speech_with_url(
    api_key: str,
    text: str,
    model: str = "speech-2.6-hd",
    voice_id: str = "Chinese (Mandarin)_Warm_Girl",
    emotion: str = "calm",
    pronunciation_dict: dict = None
):
    """
    使用 URL 格式返回（返回音频URL，有效期24小时）
    """
    url = "https://api.minimaxi.com/v1/t2a_v2"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1,
            "vol": 1,
            "pitch": 0,
            "emotion": emotion
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        },
        "subtitle_enable": False,
        "output_format": "url"  # 返回 URL 而不是 hex
    }
    
    # 添加发音字典（如果提供）
    if pronunciation_dict:
        payload["pronunciation_dict"] = pronunciation_dict
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    
    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API Error: {result.get('base_resp', {}).get('status_msg')}")
    
    # 返回音频 URL
    audio_url = result.get("data", {}).get("audio")
    print(f"✅ 语音合成成功！")
    print(f"🔗 音频URL: {audio_url}")
    print(f"⏰ URL有效期: 24小时")
    
    return audio_url


if __name__ == "__main__":
    # 配置你的 API Key（从 curl 命令中获取）
    API_KEY = "sk-cp-O9pxeWFOgMup86FTpmgukzxOmDdMsX6CqR_60OPkaHyc1scZ8aRHDOsRkxYNGW3HqKj4sx-_sQMxzfoJiKleFGvyI3DAC2OKfOLwbCKMslA4d5ENPVXgA28"
    
    # 示例1：基本调用（使用 curl 中的配置）
    text_to_speech(
        api_key=API_KEY,
        text="今天是不是很开心呀，当然了！",
        voice_id="Chinese (Mandarin)_Warm_Girl",
        emotion="calm",
        pronunciation_dict={
            "tone": [
                "处理/(chu3)(li3)",
                "危险/dangerous"
            ]
        },
        output_file="output.mp3"
    )
    
    # 示例2：使用 URL 格式返回
    # audio_url = text_to_speech_with_url(
    #     api_key=API_KEY,
    #     text="Hello, this is a test.",
    #     voice_id="Chinese (Mandarin)_Warm_Girl",
    #     emotion="calm"
    # )
    
    # 示例3：自定义音色和参数
    # text_to_speech(
    #     api_key=API_KEY,
    #     text="这是一段测试文本",
    #     model="speech-2.6-turbo",  # 使用 turbo 模型（更快）
    #     voice_id="Chinese (Mandarin)_Warm_Girl",
    #     emotion="happy",
    #     output_file="custom_voice.mp3"
    # )


from utils import settings
def set_tiktok_tts_config():
    # Update TikTok TTS settings in the configuration
    settings.config["settings"]["tts"]["voice_choice"] = "tiktok"
    settings.config["settings"]["tts"]["random_voice"] = True
    settings.config["settings"]["tts"]["tiktok_voice"] = ""
    settings.config["settings"]["tts"]["tiktok_sessionid"] = ""# Add your TikTok session ID
    settings.config["settings"]["tts"]["silence_duration"] = 0.3
    settings.config["settings"]["tts"]["no_emojis"] = False

    # Save the updated configuration
    settings.save_settings()
config = {
    "tts": {
        "voice_choice": "tiktok",
        "random_voice": True,
        "tiktok_voice": "",
        "tiktok_sessionid": "",# Add your TikTok session ID
        "silence_duration": 0.3,
        "no_emojis": False
    }
}

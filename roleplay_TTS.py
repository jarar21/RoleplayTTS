import base64
import random
import time
from typing import Final
from utils.settings import config
import requests
from pydub import AudioSegment
import os
from utils.utils import check_ratelimit, sleep_until, sanitize_text  # Importing functions from utils.py
from utils.tiktok_voices import disney_voices, eng_voices, non_eng_voices

class TikTokTTSException(Exception):
    def __init__(self, code: int, message: str):
        self._code = code
        self._message = message

    def __str__(self) -> str:
        if self._code == 1:
            return f"Code: {self._code}, reason: probably the aid value isn't correct, message: {self._message}"
        if self._code == 2:
            return f"Code: {self._code}, reason: the text is too long, message: {self._message}"
        if self._code == 4:
            return f"Code: {self._code}, reason: the speaker doesn't exist, message: {self._message}"
        return f"Code: {self._message}, reason: unknown, message: {self._message}"

session_id = config["tts"]["tiktok_sessionid"]

class TikTok:
    """TikTok Text-to-Speech Wrapper"""
    def __init__(self):
        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)",
            "Cookie": f"sessionid={session_id}",
        }
        self.URI_BASE = "https://api16-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"
        self.max_chars = 200
        self._session = requests.Session()
        # set the headers to the session, so we don't have to do it for every request
        self._session.headers = headers

    def run(self, text: str, filepath: str, voice_name: str):
        # Get the voice from the provided name
        voice = self.get_voice_by_name(voice_name)
        # Sanitize text
        text = sanitize_text(text)  # Using sanitize_text from utils.py
        # Prepare url request
        params = {"req_text": text, "speaker_map_type": 0, "aid": 1233}
        if voice is not None:
            params["text_speaker"] = voice
        # Send request
        try:
            response = self._session.post(self.URI_BASE, params=params)
            if not check_ratelimit(response):  # Check and handle ratelimit
                return
        except ConnectionError:
            time.sleep(random.randrange(1, 7))
            response = self._session.post(self.URI_BASE, params=params)
        # Check if there was an error in the request
        data = response.json()
        status_code = data["status_code"]
        if status_code != 0:
            raise TikTokTTSException(status_code, data["message"])
        # Decode data from base64 to binary
        try:
            raw_voices = data["data"]["v_str"]
        except:
            print("The TikTok TTS returned an invalid response. Please try again later, and report this bug.")
            raise TikTokTTSException(0, "Invalid response")
        decoded_voices = base64.b64decode(raw_voices)
        # Write voices to specified filepath
        with open(filepath, "wb") as out:
            out.write(decoded_voices)

    def get_voice_by_name(self, voice_name: str) -> str:
    # Check if the voice name matches any of the predefined voices
     if voice_name.lower() == "dan":
        if config["tts"]["random_voice"]:
            return random.choice(disney_voices + eng_voices + non_eng_voices)
        else:
            return config["tts"]["dan_voice"]  # Ghost Host for DAN
     elif voice_name.lower() == "gpt":
        if config["tts"]["random_voice"]:
            return random.choice(disney_voices + eng_voices + non_eng_voices)
        else:
            return config["tts"]["gpt_voice"]  # Rocket for GPT
     else:
        if config["tts"]["random_voice"]:
            return random.choice(disney_voices + eng_voices + non_eng_voices)
        else:
            return config["tts"]["ending_vocals"]  # Rocket for GPT
        

# Read input file and process each line
def process_file(input_file, dan_folder, gpt_folder):
    tiktok = TikTok()
    dan_index = 1
    gpt_index = 1
    with open(input_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if not line.strip():
            continue  # Skip empty lines
        if line.startswith('DAN'):
            voice_input = 'dan'
            text_input = line.strip('DAN:').strip()  # Remove 'DAN:' and leading/trailing whitespaces
            dan_output_file = f"{dan_folder}/DAN{dan_index}.mp3"
            try:
                tiktok.run(text_input, dan_output_file, voice_input)
                print(f"Generated DAN audio {dan_output_file}")
                dan_index += 1
            except TikTokTTSException as e:
                print(f"Error generating DAN audio: {e}")
        elif line.startswith('GPT'):
            voice_input = 'gpt'
            text_input = line.strip('GPT:').strip()  # Remove 'GPT:' and leading/trailing whitespaces
            gpt_output_file = f"{gpt_folder}/GPT{gpt_index}.mp3"
            try:
                tiktok.run(text_input, gpt_output_file, voice_input)
                print(f"Generated GPT audio {gpt_output_file}")
                gpt_index += 1
            except TikTokTTSException as e:
                print(f"Error generating GPT audio: {e}")
        else:
            voice_input = 'en_female_ht_f08_wonderful_world'
            text_input = line.strip()  # Remove leading/trailing whitespaces
            other_output_file = f"{gpt_folder}/Other{gpt_index}.mp3"
            try:
                tiktok.run(text_input, other_output_file, voice_input)
                print(f"Generated other audio {other_output_file}")
                gpt_index += 1
            except TikTokTTSException as e:
                print(f"Error generating other audio: {e}")

# Merge DAN and GPT audios
def merge_audios(dan_folder, gpt_folder, output_file):
    merged_audio = None
    for dan_file, gpt_file in zip(sorted(os.listdir(dan_folder)), sorted(os.listdir(gpt_folder))):
        dan_audio = AudioSegment.from_file(f"{dan_folder}/{dan_file}", format="mp3")
        gpt_audio = AudioSegment.from_file(f"{gpt_folder}/{gpt_file}", format="mp3")
        if merged_audio is None:
            merged_audio = dan_audio + gpt_audio
        else:
            merged_audio += dan_audio + gpt_audio
    # Export merged audio
    if merged_audio:
        merged_audio.export(output_file, format="mp3")
        print(f"Merged audio exported successfully to {output_file}")

# Example usage
if __name__ == "__main__":
    scene_name = input("Enter the scene name: ")
    scene_folder_path = f"{scene_name} Scene"
    dan_folder_path = f"{scene_folder_path}/dan_voice"
    gpt_folder_path = f"{scene_folder_path}/gpt_voice"
    output_file_path = f"{scene_folder_path}/{scene_name}_merged_audio.mp3"

    # Create scene folder if it doesn't exist
    os.makedirs(scene_folder_path, exist_ok=True)
    os.makedirs(dan_folder_path, exist_ok=True)
    os.makedirs(gpt_folder_path, exist_ok=True)

    # Process input file
    input_file_path = 'dialogues.txt'
    process_file(input_file_path, dan_folder_path, gpt_folder_path)

    # Merge DAN and GPT audios
    merge_audios(dan_folder_path, gpt_folder_path, output_file_path)

    print("File processing completed.")

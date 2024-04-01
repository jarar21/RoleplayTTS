# RoleplayTTS

RoleplayTTS is a Python script that leverages TikTok's Text-to-Speech (TTS) API to convert dialogues stored in a text document into audio files using various voices available on TikTok. This script facilitates the creation of immersive role-playing scenarios or story narratives by generating audio dialogues.

## Installation;

1. Clone this repository to your local machine:

2. Install the required Python packages:

   ```bash;
   pip install -r requirements.txt

## Usage

1. Prepare an input text file named `dialogues.txt` containing the dialogues you want to convert to audio. Each dialogue should start with either "DAN:" or "GPT:" followed by the text. line should be seperated by;

   Example dialogues.txt

2. Run the Python script `roleplay_TTS.py`:

   ```bash
   python roleplay_TTS.py

3. The script will process the input file, generate audio files for each dialogue using the specified voices (DAN or GPT), and merge them into a single output file named `merged_audio.mp3`.;

## Folder Structure;

- `DAN_VOICES`: Contains audio files generated using DAN voices.;
- `GPT_VOICES`: Contains audio files generated using GPT voices.;

## Additional Notes;

- The script utilizes TikTok's TTS API to generate audio files. Make sure you have a valid TikTok session ID configured in the `settings.py` file.;

## Credits;

- This script utilizes the [pydub](https://github.com/jiaaro/pydub) library for audio manipulation.;
- Special thanks to TikTok for providing the Text-to-Speech API.;

## License;

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.;


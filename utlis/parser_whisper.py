from pathlib import Path
from datetime import datetime
from zhconv import convert
import stable_whisper as whisper

from settings.constant import FILEPATH

class WhisperTranscriber(object):

    def __init__(self, model_name):
        self.model = whisper.load_model(model_name)

    def whisper_transcribe(self, audio_path, file_type=None):
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        basename = audio_path.rsplit('.', 1)[0]

        filename = f"{FILEPATH}{wono}{basename}.txt"

        audio = self.model.transcribe(audio_path, fp16=False, language='Chinese')
        whisper.results_to_sentence_srt(audio, 'audio')
        with open('audio.srt', 'r') as input_file: # 打开原始文件  读取原始文件的内容
            content = input_file.read()

        with open(filename, 'w') as output_file: # 打开目标文件   将读取的内容写入目标文件
            output_file.write(content)



if __name__ == '__main__':

    transcriber = WhisperTranscriber("base")
    audio_path = "8f95d.mp3"
    text = transcriber.whisper_transcribe(audio_path)

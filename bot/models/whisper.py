from io import BytesIO

from faster_whisper import WhisperModel


class WhisperWrapper:
    """Сlass wrapper over Whisper model"""

    def __init__(self, model_size: str = "medium.en", device: str = "cpu"):
        self._model = WhisperModel(model_size, device=device, compute_type="int8")

    def __call__(self, audio_file: BytesIO) -> str:
        segments, info = self._model.transcribe(audio_file, beam_size=5, language="en")
        return " ".join([segment.text for segment in segments])

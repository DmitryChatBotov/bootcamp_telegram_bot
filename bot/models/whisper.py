from pathlib import Path

import torch
import whisper


class WhisperWrapper:
    def __init__(
        self, model_type: str = "tiny", device: torch.device = torch.device("cpu")
    ):
        self._model = whisper.load_model(model_type, device=device)

    def __call__(self, audio_filepath: str | Path):
        return self._model.transcribe(audio_filepath)["text"]

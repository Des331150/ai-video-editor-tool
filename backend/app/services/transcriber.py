from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class WordTimestamp:
    word: str
    start_time: float
    end_time: float


class Transcriber(ABC):
    @abstractmethod
    async def transcribe(self, file_path: str) -> list[WordTimestamp]:
        ...


class FakeTranscriber(Transcriber):
    async def transcribe(self, file_path: str) -> list[WordTimestamp]:
        return [
            WordTimestamp("Hello", 0.0, 0.3),
            WordTimestamp("and", 0.3, 0.45),
            WordTimestamp("welcome", 0.45, 0.8),
            WordTimestamp("to", 0.8, 0.9),
            WordTimestamp("this", 0.9, 1.0),
            WordTimestamp("video", 1.0, 1.3),
            WordTimestamp("Today", 1.3, 1.6),
            WordTimestamp("we", 1.6, 1.7),
            WordTimestamp("are", 1.7, 1.8),
            WordTimestamp("talking", 1.8, 2.1),
            WordTimestamp("about", 2.1, 2.2),
            WordTimestamp("AI", 2.2, 2.4),
            WordTimestamp("video", 2.4, 2.6),
            WordTimestamp("editing", 2.6, 2.9),
        ]


class WhisperTranscriber(Transcriber):
    async def transcribe(self, file_path: str) -> list[WordTimestamp]:
        msg = (
            "WhisperTranscriber is not implemented yet. "
            "Install openai-whisper and implement the transcribe method."
        )
        raise NotImplementedError(msg)

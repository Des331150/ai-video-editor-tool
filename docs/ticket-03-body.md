## Parent

#1

## What to build

Auto-transcribe uploaded Source Media via Whisper (or Whisper API) on import. Store word-level timestamps (word -> start_time, end_time). Display the transcript as read-only text in the project editor UI. Non-speech sources show no transcript.

## Acceptance criteria

- [ ] Transcription starts automatically after upload completes
- [ ] User sees the transcript rendered as text in the editor
- [ ] Each word in the transcript maps back to its timestamp range
- [ ] Non-speech sources show empty/no transcript
- [ ] API serves transcript data with word timestamps
- [ ] Tests with mocked transcriber

## Blocked by

- #3 (Source Media Upload)

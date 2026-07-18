## Parent

#1

## What to build

Two synchronous NL commands delivered via a Command Bar UI in the editor.

1. "Remove all filler words": Scan the Transcript for known filler words ("um", "ah", "like", "you know"). Look up their timestamps. Create EditOperations to remove each. Apply via the Instruction system (undoable).

2. "Remove pauses longer than X seconds": Analyze the audio waveform for silence gaps exceeding the user-specified threshold (default 500ms). Create EditOperations to remove each pause. Apply via the Instruction system. User specifies threshold in the command.

The Command Bar is a text input at the top of the editor. User types a command, hits enter, it executes synchronously, and the result appears in the Instruction History.

## Acceptance criteria

- [ ] User can type "remove all filler words" in the command bar
- [ ] Filler words are detected and removed from transcript/timeline
- [ ] The removal appears as an undoable instruction in history
- [ ] User can type "remove pauses longer than 1 second"
- [ ] Pauses exceeding the threshold are removed
- [ ] Threshold parameter can vary (default 500ms)
- [ ] Both commands work on the full project or a Selection (if one is active)
- [ ] Tests with mocked audio analysis

## Blocked by

- #7 (Instruction System)
- #4 (Transcription Pipeline)

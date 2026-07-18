## Parent

#1

## What to build

The "shorten to duration" command - the most complex NL instruction. User types "shorten this to 60 seconds" or "shorten by 30%". Runs as an async ProcessingJob with three phases:

1. **Filler removal**: Same as ticket 8 - remove filler words
2. **Pause tightening**: Same as ticket 8 - tighten pauses
3. **LLM sentence ranking**: Send the transcript sentences to OpenRouter with a prompt asking which contribute least to the core message. Remove low-ranked sentences until the target duration is met (or within tolerance).

If a Selection is active, shortening is scoped to that selection. The job status is shown with phase-level progress. On completion, the instruction appears in history and can be undone.

## Acceptance criteria

- [ ] User types "shorten this to 60 seconds" in the command bar
- [ ] A ProcessingJob starts and shows progress (phase 1/2/3)
- [ ] User can continue editing while job runs
- [ ] On completion, filler words are removed, pauses tightened, low-value sentences cut
- [ ] Final duration is at or under the target
- [ ] The operation is undoable via instruction history
- [ ] "shorten by 30%" works proportionally
- [ ] Works on active Selection if one is set
- [ ] Tests with mocked LLM and audio analysis

## Blocked by

- #9 (Processing Job System)
- #10 (Sync NL Commands - filler/pause detection reused)
- #8 (Selections)

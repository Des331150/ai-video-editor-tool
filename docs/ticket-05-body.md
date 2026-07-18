## Parent

#1

## What to build

Make the Transcript editable as a text document and the Timeline interactive. Delete a word or phrase from the transcript -> corresponding video is removed, timeline closes the gap smoothly. Rearrange sentences in the transcript by drag-and-drop -> segments reorder on the timeline. Drag segments on the timeline to reorder -> transcript text reorders. Drag segment edges to trim -> transcript reflects trimmed range. All changes auto-save.

The "Editing Instruction" system is not involved yet - these edits apply directly to the model (undo/redo via instruction system comes in ticket 6).

## Acceptance criteria

- [ ] User can delete words in the transcript and timeline updates
- [ ] User can drag sentences in the transcript to reorder segments
- [ ] User can drag segments on the timeline to reorder
- [ ] User can drag segment edges to trim
- [ ] All timeline changes reflected in transcript immediately
- [ ] Changes persist on reload (auto-save)

## Blocked by

- #5 (Timeline Engine + Sync)

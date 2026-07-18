## Parent

#1

## What to build

Named, persistable Selections on the Timeline or Transcript. A Selection is a named range (start_segment_id, end_segment_id, or word range). API: create selection (POST), list selections (GET), delete selection (DELETE). UI: select a range on the timeline or highlight text in the transcript, name it, save it. Reuse a selection by picking it from a list. When a command is issued with an active selection, it only applies within that range.

Selections are the mechanism by which users scope commands to part of their project (e.g., "remove pauses in the intro").

## Acceptance criteria

- [ ] User can select a range on the timeline and save it with a name
- [ ] User can select text in the transcript and save it with a name
- [ ] Saved selections appear in a list
- [ ] User can apply a command to a selection (scope the command)
- [ ] User can delete a selection
- [ ] Selections persist across page reloads

## Blocked by

- #5 (Timeline Engine + Sync)

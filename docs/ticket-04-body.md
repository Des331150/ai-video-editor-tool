## Parent

#1

## What to build

The core bidirectional sync engine between Transcript and Timeline. Segment model (source_id, start_time, end_time, position). Build initial Timeline from Transcript (one Segment per sentence or fixed-length chunk). Timeline API: read segments, split a segment, merge adjacent segments, reorder segments. Transcript-Timeline sync logic: changes to one propagate to the other. Visual Timeline component showing segments as blocks.

After this ticket: the user opens a project, sees the transcript AND a visual timeline side by side. Both show the same data. No editing yet - just viewing.

## Acceptance criteria

- [ ] Initial Timeline is auto-built from Transcript on first load
- [ ] Timeline API returns ordered segments with source references
- [ ] User sees visual timeline blocks matching transcript content
- [ ] Transcript and Timeline are in sync (two views, one model)
- [ ] Domain unit tests cover sync logic (split, merge, reorder)

## Blocked by

- #4 (Transcription Pipeline)

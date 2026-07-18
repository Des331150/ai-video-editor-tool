## Parent

#1

## What to build

Render the final video from the current Timeline state. Export API endpoint that takes the ordered Segments, concatenates the corresponding source media slices via FFmpeg, and produces a single video file. Download endpoint for the rendered file. Export button in the UI that triggers rendering and shows progress.

## Acceptance criteria

- [ ] User clicks "Export" and rendering starts
- [ ] Rendered video matches the current Timeline (order, trimmed ranges)
- [ ] User can download the final video file
- [ ] Export progress is shown in the UI
- [ ] User can export again after making more edits

## Blocked by

- #5 (Timeline Engine + Sync)

# Spec: AI Video Editor — MVP

## Problem Statement

Solo content creators (YouTubers, podcasters) spend hours in traditional video editors trimming pauses, removing filler words, and rearranging footage. The tools are designed for professional editors with multi-track timelines and hundreds of buttons — overkill for someone who just wants to "remove the ums and shorten this to 60 seconds." Existing AI-assisted tools like Descript exist but are SaaS-only, expensive at scale, and don't let the creator own their infrastructure.

## Solution

A web application where creators upload video or audio, receive an auto-generated editable transcript, and edit their content through three interlocking mechanisms:

1. **Transcript-as-text**: Edit the transcript like a document — delete words to remove them from the video, rearrange sentences to reorder clips, type new text to add voiceover (TTS). The AI finds clean edit points automatically.
2. **Natural-language commands**: Type or speak instructions like "remove all pauses longer than 1 second" or "shorten this selection to 30 seconds." The AI interprets the intent and modifies the timeline.
3. **Timeline view**: A visual, single-sequence timeline for drag-and-drop reordering and precise trimming when text-level control isn't enough.

All edits are persistent, undoable, and stored as discrete instructions. Complex processing runs asynchronously — the user keeps working while the AI processes.

## User Stories

1. As a content creator, I want to upload a video or audio file, so that I can start editing it.
2. As a content creator, I want the tool to auto-generate a transcript with word-level timestamps on import, so that I can start editing by text immediately.
3. As a content creator, I want to see and edit the transcript as a text document, so that I can work with my content the same way I edit a script.
4. As a content creator, I want to delete a word or phrase from the transcript, so that the corresponding video/audio is removed and the timeline closes the gap smoothly.
5. As a content creator, I want to rearrange sentences in the transcript by drag-and-drop, so that the corresponding video segments are reordered on the timeline.
6. As a content creator, I want to type a natural-language instruction in a command bar, so that the AI interprets it and modifies my project accordingly.
7. As a content creator, I want to say "remove all pauses longer than 1 second", so that the AI tightens dead air across the entire project.
8. As a content creator, I want to say "remove all filler words", so that the AI removes "um", "ah", "like", and "you know" from the project.
9. As a content creator, I want to say "shorten this to 60 seconds", so that the AI removes filler words, tightens pauses, and cuts low-value sentences to hit the target duration.
10. As a content creator, I want to say "shorten this by 30%", so that the AI applies a proportional reduction to the selected content.
11. As a content creator, I want to select a portion of the transcript or timeline before issuing a command, so that the AI only operates on that selection.
12. As a content creator, I want to save a selection with a name, so that I can reuse it across multiple commands.
13. As a content creator, I want to see a visual timeline of my segments, so that I can understand the structure of my project at a glance.
14. As a content creator, I want to reorder segments on the timeline by drag-and-drop, so that the transcript updates to match the new order.
15. As a content creator, I want to trim the start or end of a segment on the timeline, so that the transcript reflects the trimmed content.
16. As a content creator, I want to see the transcript update in real-time when I make timeline changes, so that both views stay in sync.
17. As a content creator, I want to undo the last editing instruction, so that I can revert a mistake.
18. As a content creator, I want to redo an undone instruction, so that I can restore a change I reconsidered.
19. As a content creator, I want to see a history of my editing instructions, so that I can review what changes I've made.
20. As a content creator, I want to jump back to any point in my instruction history, so that I can revert the project to an earlier state.
21. As a content creator, I want complex instructions to show processing progress, so that I know the AI is working and can estimate when it will complete.
22. As a content creator, I want to continue editing other parts of my project while a complex instruction is processing, so that I'm not blocked by AI wait times.
23. As a content creator, I want to preview the effect of an editing instruction before committing it, so that I can verify the AI's changes meet my expectations.
24. As a content creator, I want to export my project as a video file, so that I can publish or share the final result.
25. As a content creator, I want my project to auto-save, so that I don't lose work if I close the browser or lose connection.
26. As a content creator, I want to close my project and reopen it later with all edits intact, so that I can work across multiple sessions.

## Implementation Decisions

### Stack
- **Backend**: Python (FastAPI) — serves the API and runs AI processing in-process.
- **Frontend**: React + Vite SPA — serves the editor UI (transcript view, timeline, command bar).
- **Database**: Postgres — stores Projects, Source Media records, Segments, Transcripts, Editing Instructions, Processing Jobs.
- **AI**: In-process Python. OpenRouter API for LLM-based NL instruction parsing. Whisper (or Whisper API) for transcription. Custom audio analysis (librosa or similar) for pause/filler detection.
- **Deployment**: Single Python service + Postgres. Frontend built as static assets served by the Python service or CDN.

### API Modules

```
/api/projects          — CRUD and listing
/api/projects/{id}/sources       — Source Media upload and management
/api/projects/{id}/timeline      — Timeline read and segment manipulation
/api/projects/{id}/transcript    — Transcript read and text edits
/api/projects/{id}/instructions  — Editing Instruction creation, history, undo/redo
/api/projects/{id}/selections    — Named Selection CRUD
/api/projects/{id}/export        — Export triggering and status
/api/jobs/{id}                   — Processing Job status polling
```

### Domain Model

The domain model is defined in `CONTEXT.md` at the repo root. Key entities:

- **Project** — top-level container. Holds sources, timeline segments, instruction history, selections, export settings.
- **SourceMedia** — immutable reference to an uploaded file. Managed copy in tool's storage. Optional Transcript.
- **Timeline** — ordered sequence of Segments. Single-sequence (designed for multi-track later). Bidirectional mirror of Transcript.
- **Segment** — slice of a SourceMedia. Defined by source_id, start_time, end_time, timeline_position.
- **Transcript** — word-to-timestamp mapping for a SourceMedia. Auto-generated on import. Editable text — changes mutate the Timeline.
- **Selection** — named, persisted range on Timeline or Transcript. Reusable across instructions.
- **EditingInstruction** — persistent NL command. Member of a linear history stack. May spawn a ProcessingJob.
- **ProcessingJob** — async AI task. States: pending → processing → completed | failed. User can continue working during processing.
- **EditOperation** — concrete timeline change produced by an instruction. One instruction → many operations.

### Key Workflows

**Transcript edit**: User deletes word X in transcript → server looks up word's timestamp range → removes corresponding time range from the Segment (or splits Segment and removes the middle) → broadcasts updated Timeline to the frontend.

**NL command**: User types "remove all pauses longer than 1s" → instruction saved as `pending` → if simple, process synchronously: detect all Pauses > 1s across selected Segments, create EditOperations for each, update Timeline, mark instruction `applied` → if complex (needs LLM), spawn ProcessingJob, instruction moves to `processing`, user polls job status.

**Undo**: User clicks undo → server pops top instruction from history → reverses all EditOperations produced by that instruction → restores prior Timeline state → marks instruction as `undone`. Redo pushes it forward again.

### Audio Analysis (Shorten/Compress)

Shorten operates in three phases:
1. **Filler detection**: Scan transcript for known filler words ("um", "ah", "like", "you know") with their timestamps.
2. **Pause detection**: Analyze audio waveform for silence gaps exceeding the user-specified threshold (default 500ms).
3. **Sentence importance** (LLM-assisted): For target-duration shortening, the LLM ranks sentences by relevance to the core message; low-ranked sentences are candidates for removal.

### Processing Job States and Architecture

```
pending → processing → completed
                   → failed
```

Jobs are stored in Postgres with a state field. The FastAPI server runs background tasks (via `BackgroundTasks` or a simple in-process task queue like ARQ). When a job completes, it writes the resulting EditOperations and updates the instruction's history entry. The frontend polls `GET /api/jobs/{id}` or the instruction's status.

### UI Layout (Conceptual)

```
┌─────────────────────────────────────────────┐
│  [Project Name]    [Command Bar]    [Export] │
├──────────────────────┬──────────────────────┤
│                      │                      │
│  Transcript View     │  Timeline View       │
│  (editable text)     │  (segment blocks)    │
│                      │                      │
│  [word] [word]       │  [seg1] [seg2] [sg3] │
│  [word] [word]       │                      │
│                      │                      │
├──────────────────────┴──────────────────────┤
│  [Preview Player]                           │
├─────────────────────────────────────────────┤
│  Instruction History                        │
│  • Shorten to 60s  [undo][redo]            │
│  • Remove filler words                      │
│  • Manual trim seg2                   [✔]  │
└─────────────────────────────────────────────┘
```

## Testing Decisions

- **Primary seam**: The FastAPI API layer. All behavior is tested by sending HTTP requests to the API and asserting the response state and resulting database state. This tests the system as a black box from the client's perspective.
- **Domain logic tests**: Unit tests on the core editing engine (applying EditOperations to a Timeline, undo/redo stack behavior, Transcript→Timeline sync calculations) without HTTP. These test the pure logic that the API layer wraps.
- **What makes a good test**: Tests should describe the external behavior the user experiences, not the internal implementation. For example: "when I delete word X from the transcript, the timeline removes the corresponding segment range" — not "when I call timeline.removeRange(), it calls segment.split()."
- **AI-dependent tests**: The LLM and transcription calls should be mocked/faked in tests. A fake LLM returns a deterministic "remove segments 3 and 5" response. A fake transcriber returns a known word-timestamp map.
- **Prior art**: None exists yet (greenfield project). Testing patterns follow standard FastAPI test practices using `httpx.AsyncClient` and pytest fixtures with a test Postgres database.
- **Module test targets**:
  - `tests/api/` — integration tests for each endpoint group
  - `tests/domain/` — unit tests for core editing logic
  - `tests/ai/` — tests for AI service wrappers with mocked models

## Out of Scope

- Multi-track timeline (designed for future addition, not built now)
- Branching edit history (linear undo/redo only)
- Multiple exports per project (one-shot export, future multi-render)
- Real-time collaboration or multi-user projects
- Mobile or tablet support (desktop web only)
- Speed-up sections or highlight-reel generation (shorten techniques limited to: remove filler words, tighten pauses, remove low-value sentences)
- Direct recording/voiceover capture inside the tool
- Image or overlay support (video + audio only)
- Desktop app or offline mode (web-only, internet required for AI)
- Template or preset system for edit instructions
- API for third-party integrations

## Further Notes

- The OpenRouter API choice means the LLM provider can be swapped without code changes — just the API endpoint and key.
- The tool's managed storage for Source Media means the original file can be deleted after import without breaking the project. This also means storage costs scale with usage.
- The bidirectional sync between Transcript and Timeline is the most architecturally sensitive part of the system. Any edit in one view must produce equivalent changes in the other. The Segment model is the single source of truth — both views are projections.
- The MVP should prioritize getting the transcript-edit → timeline-update loop working and the "remove all pauses" command. Everything else (shorten-to-duration, saved selections, preview-before-commit) can be layered on incrementally.

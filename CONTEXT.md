# AI Video Editor

An AI-powered video editing tool that lets solo content creators edit video and audio through natural language instructions, with optional transcript-based editing and high-level intent commands.

## Language

**Project**:
The top-level container for a single editing session. Holds source media, a timeline of segments, a collection of editing instructions, and export settings.
_Avoid_: Video, file, session

**Source Media**:
Raw video or audio files imported into a project. On import, the file is copied into the tool's managed storage, making the project independent of the original file location. Immutable once imported; all editing operations reference the source by ID with a time range. If a Source Media item has no detectable speech, it exists only as a Timeline Segment with no Transcript — editable via timeline operations only.
_Avoid_: Footage, raw file, asset

**Timeline**:
A single ordered sequence of Segments that determines the final output. Audio and video are locked together within each Segment. The Timeline and the Transcript are bidirectional mirrors — editing either one updates the other. Designed to accommodate multi-track in the future, but the initial model is one sequence.
_Avoid_: Storyboard, sequence

**Segment**:
A contiguous slice of a Source Media item placed on the Timeline. Defined by a source reference, a start time, an end time, and a position in the timeline order.
_Avoid_: Clip, cut, piece

**Transcript**:
The speech-to-text output for a Source Media item. A mapping from words to their timestamp ranges within that source. Auto-generated on import. Editable as a text document — adding, deleting, or rearranging text triggers corresponding Timeline modifications. The primary editing interface.
_Avoid_: Captions, subtitles, text track

**Selection**:
A named, persistable range on the Timeline (or within a Transcript). Users can save selections, apply Editing Instructions to them, and reuse them. A first-class domain concept, not ephemeral UI state.
_Avoid_: Highlight, range, region, clip selection

**Editing Instruction**:
A discrete, persistent, undoable natural-language command applied to a Project. Each instruction is stored as a first-class entity, viewable in a history stack, and can be undone or reordered. Simple instructions apply instantly; complex instructions spawn a Processing Job.
_Avoid_: Command, action, edit

**Processing Job**:
An asynchronous AI task spawned by an Editing Instruction. Has states: pending, processing, completed, failed. The user can continue working on other parts of the project while a Job runs. Produces one or more Edit Operations upon completion.
_Avoid_: Task, process, AI job, worker

**Edit Operation**:
The concrete effect produced on the Timeline by an Editing Instruction. One instruction may produce multiple operations (e.g., "remove all pauses" creates one operation per pause removed).
_Avoid_: Edit, change, modification

**Edit Instruction History**:
A linear stack of Editing Instructions supporting undo and redo. Future versions may support branching (experimental edits on a fork).
_Avoid_: Undo stack, command history, changes list

**Export**:
The action of producing a final video file from a Project. Initially a simple one-shot operation; designed to accommodate multiple renders per project in the future.
_Avoid_: Render, publish, output

## Shorten / Compress

**Filler Word**:
A word ("um", "ah", "like", "you know") that can be removed to tighten speech without changing meaning.
_Avoid_: Filler, hesitation, disfluency

**Pause**:
A silence or gap in speech within a Source Media item or Segment. Measured in milliseconds. A common target for removal or tightening during compression.
_Avoid_: Silence, gap, dead air

**Target Duration**:
The desired length of the output after a Shorten instruction, expressed either as an absolute time ("60 seconds") or a percentage of original ("reduce by 20%").
_Avoid_: Goal time, length target

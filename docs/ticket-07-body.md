## Parent

#1

## What to build

Async ProcessingJob infrastructure for complex AI instructions. Job entity with states: pending, processing, completed, failed. API: get job status (GET /api/jobs/{id}), list jobs for an instruction. Background task execution in FastAPI (BackgroundTasks or lightweight queue). When a job completes, it writes EditOperations and updates the instruction's history entry. The frontend polls the instruction status or job endpoint and shows a progress indicator.

No concrete async commands yet - just the infrastructure. Ticket 10 will use this.

## Acceptance criteria

- [ ] Creating an instruction with async=true spawns a ProcessingJob
- [ ] Job progresses through pending -> processing -> completed
- [ ] User can poll job status and see progress in the UI
- [ ] Failed jobs report an error message
- [ ] User can continue editing while job runs
- [ ] Tests with fake async processor

## Blocked by

- #7 (Instruction System + Undo/Redo)

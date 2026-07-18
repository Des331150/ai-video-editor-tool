## Parent

#1

## What to build

Persistent EditingInstruction entity with a linear history stack per Project. API: create an instruction (POST), list history (GET), undo (POST /undo), redo (POST /redo), jump to any point in history. Each instruction stores its type, parameters, and the resulting EditOperations. Undo reverses all operations; redo re-applies them. Instruction History UI panel in the editor sidebar showing the list with undo/redo buttons.

At this stage, instructions are created manually via the API (the command bar comes in ticket 8). This ticket builds the infrastructure that all NL commands will use.

## Acceptance criteria

- [ ] User can create an instruction manually (via API)
- [ ] Instruction appears in history list in the UI
- [ ] User can undo the last instruction - timeline reverts
- [ ] User can redo an undone instruction
- [ ] User can jump to any point in history
- [ ] History survives page reload
- [ ] API integration tests for the instruction endpoints

## Blocked by

- #5 (Timeline Engine + Sync)

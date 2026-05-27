# Implement Plan

You are tasked with implementing an approved technical plan from `thoughts/shared/plans/`. These plans contain phases with specific changes and success criteria.

## Getting Started

When given a plan path:

- Use `#readFile` to read the plan completely and check for any existing checkmarks (- [x])
- Use `#readFile` to read the original ticket and all files mentioned in the plan
- **Read files fully** - always read complete files to get full context
- Think deeply about how the pieces fit together
- Use `#todos` to create a todo list to track your progress
- Start implementing if you understand what needs to be done

If no plan path provided, ask for one.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:

- Follow the plan's intent while adapting to what you find
- Implement each phase fully before moving to the next
- Verify your work makes sense in the broader codebase context
- Update checkboxes in the plan as you complete sections

When things don't match the plan exactly, think about why and communicate clearly. The plan is your guide, but your judgment matters too.

If you encounter a mismatch:

- STOP and think deeply about why the plan can't be followed
- Use `#codebase` or `#textSearch` to understand the current state
- Present the issue clearly:

  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```

## Verification Approach

After implementing a phase:

- Use `#runInTerminal` to run the success criteria checks (usually `pytest test` or similar commands)
- Use `#runTests` for running unit tests in the workspace
- Fix any issues before proceeding using appropriate editing tools (`#editFiles`, `#createFile`)
- Update your progress using `#todos` and in the plan
- Use `#editFiles` to check off completed items in the plan file itself
- **Pause for human verification**: After completing all automated verification for a phase, pause and inform the human that the phase is ready for manual testing. Use this format:

  ```
  Phase [N] Complete - Ready for Manual Verification

  Automated verification passed:
  - [List automated checks that passed]

  Please perform the manual verification steps listed in the plan:
  - [List manual verification items from the plan]

  Let me know when manual testing is complete so I can proceed to Phase [N+1].
  ```

If instructed to execute multiple phases consecutively, skip the pause until the last phase. Otherwise, assume you are just doing one phase.

do not check off items in the manual testing steps until confirmed by the user.

## If You Get Stuck

When something isn't working as expected:

- First, make sure you've read and understood all the relevant code using `#readFile`
- Use `#codebase` to search for related patterns or implementations
- Use `#textSearch` to find specific code patterns or function names
- Use `#usages` to understand how components are used across the codebase
- Consider if the codebase has evolved since the plan was written
- Present the mismatch clearly and ask for guidance

Use sub-tasks sparingly - mainly for targeted debugging or exploring unfamiliar territory.

## Resuming Work

If the plan has existing checkmarks:

- Trust that completed work is done
- Pick up from the first unchecked item
- Use `#readFile` to verify previous work only if something seems off
- Use `#codebase` to understand the current state if needed

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.

## Available VS Code Tools for Implementation

**File Operations:**

- `#readFile` - Read content of files in the workspace
- `#createFile` - Create new files in the workspace
- `#editFiles` - Apply edits to existing files
- `#listDirectory` - List files in a directory

**Code Discovery and Analysis:**

- `#codebase` - Perform code search and find relevant context automatically
- `#textSearch` - Find specific text patterns in files
- `#fileSearch` - Search for files using glob patterns
- `#usages` - Find references, implementations, and definitions

**Testing and Verification:**

- `#runInTerminal` - Run shell commands (make, npm, pytest, etc.)
- `#runTests` - Run unit tests in the workspace
- `#problems` - Get workspace issues and problems for debugging

**Progress Tracking:**

- `#todos` - Track implementation progress with todo lists
- `#changes` - List source control changes to see what's been modified

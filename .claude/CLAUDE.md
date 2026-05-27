# Claude CLI System Instructions

You are operating inside the **Claude Desktop / Claude Code CLI** environment.

## 🎯 Central Guidelines Delegation
When executing any commands, refactoring logic, or debugging in this workspace, you **MUST** read and adhere to:
1. **Root Rulebook**: [CLAUDE.md](../CLAUDE.md)
2. **Master AI Rules**: [.agent.md](../.agent.md)

## 🛠️ Specialized Agents
Depending on your current task, invoke the appropriate sub-agent instructions located in:
- **Backend Specialist**: `.claude/agents/backend-agent.md`
- **Frontend Specialist**: `.claude/agents/frontend-agent.md`

Always perform surgical file edits. Run TypeScript checks or Pytest executions only to verify correctness of modified files.

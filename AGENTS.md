# humanise

Claude Code skill for auditing and rewriting prose that carries common AI-writing tells.

## Git closeout and worktree visibility

- `git push` updates the remote branch only. It does not update other local checkouts, worktrees, or running agent sessions. Do not imply Claude, Codex, or another agent will see pushed or merged changes until that checkout fetches, pulls, or is otherwise updated.
- After any push or merge, run `git status --short --branch` in the checkout you changed and report the branch, cleanliness, and upstream state.
- After a PR merge, explicitly say whether this checkout was updated to the merge commit.
- If Claude or another agent is expected to continue in a different checkout, update that named checkout only when it is clean and safe to fast-forward. If it is dirty, detached, or on another branch, report that instead of changing it.
- When a different checkout needs manual sync, give the exact commands:

```bash
git fetch --prune
git switch main
git pull --ff-only
```

- Never rely on the remote merge alone as proof that local Claude/Codex sessions have the new files. Worktrees are separate local filesystems.

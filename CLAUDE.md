# Project Instructions for Claude Code

## Internship Pages

Before adding or changing an internship page (RoBIM, Toyota, or a new one), read `_docs/internship-layout.md`. For where the RoBIM and Toyota pages stand, read `_docs/handoff-robim-toyota.md`.

## Sync With GitHub at the Start of a Session

Sync the local repository with GitHub before your first edit in a session. After that, keep working without re-syncing until one of these happens:

- A new session starts, including when I resume an old one.
- About an hour or more has passed since you last worked in this repo.
- I mention I pushed changes from somewhere else.

### Required steps (in order)

1. **Check the current state of the repo:**
   ```bash
   git status
   git branch --show-current
   ```

2. **If there are uncommitted local changes**, do NOT discard them. Stop and ask me whether to commit them, stash them, or discard them before proceeding.

3. **Fetch and merge the latest changes from the remote:**
   ```bash
   git fetch origin
   git merge origin/<current-branch>
   ```
   (Or `git pull` on the current branch — but always know which branch you're on first.)

4. **If there are merge conflicts:**
   - Do not blindly resolve them by picking one side.
   - List the conflicting files and summarize what each side changed.
   - Ask me how to resolve any conflict where the correct resolution isn't obvious.

5. **Confirm the sync succeeded** (`git status` shows the branch is up to date with `origin/<branch>`) before making any edits.

### Notes

- Never use `git push --force`, `git reset --hard origin/...`, or anything else that could destroy local or remote work without my explicit approval.
- If the remote is unreachable (no network, auth failure), tell me and ask whether to proceed with edits anyway rather than silently continuing.

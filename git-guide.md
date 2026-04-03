# Git Guide for Non-Developers

Git is a tool that tracks changes to files over time. Think of it like a detailed undo history
for an entire project — one that multiple people can share and contribute to at the same time.

This guide covers the core concepts you'll encounter when using the **Source Control panel** in
VS Code (the icon that looks like a branching tree in the left sidebar).

---

## The Big Picture

Imagine a project folder where every change is logged — who changed what, when, and why. Git
is that log. Instead of saving over files and losing old versions, Git lets you save
**snapshots** of your work and go back to any of them.

---

## Key Concepts

### Repository (Repo)

A **repository** is just a folder that Git is tracking. It looks like a normal folder on your
computer, but Git quietly records every change made inside it.

> In VS Code, when you open a folder that has a repo, the Source Control panel will show you
> what has changed.

---

### Commit

A **commit** is a saved snapshot of your changes. When you commit, you're telling Git:
*"Remember the project exactly as it is right now."*

Each commit has:
- A **message** describing what changed (e.g. "Updated client notes for April")
- A record of exactly which lines were added or removed

**In VS Code:**
1. Make changes to your files and save them.
2. Open the **Source Control** panel (Ctrl+Shift+G).
3. You'll see a list of changed files. Hover over a file and click **+** to stage it.
4. Type a short message in the box at the top.
5. Click the **checkmark (✓) Commit** button.

---

### Staging

Before you commit, you choose *which* changes to include. This step is called **staging**.

Think of it like packing a box before shipping it — you decide what goes in before you seal
and send it.

**In VS Code:** The **+** icon next to a file adds it to the staging area. The **−** icon
removes it. Only staged files are included in your next commit.

---

### Branch

A **branch** is a separate version of the project where you can make changes without affecting
the main version.

Think of it like making a copy of a document to try out edits — if you like the changes, you
merge them back. If not, you discard the copy.

The main branch is usually called **main** (or sometimes **master**).

**In VS Code:** The current branch name is shown in the **bottom-left corner** of the window.
Click it to switch branches or create a new one.

---

### Push and Pull

Your local repo (on your computer) and a remote repo (stored online, e.g. on GitHub) stay in
sync through pushing and pulling.

| Action | What it does |
|--------|--------------|
| **Pull** | Downloads the latest changes from the online repo to your computer |
| **Push** | Uploads your committed changes to the online repo |

**In VS Code:** Use the **... (More Actions)** menu in the Source Control panel, or the
sync icon (↕) in the bottom-left status bar to pull and push.

> Always **pull before you start working** so you have the latest version.

---

### Merge and Conflicts

When two people edit the same part of the same file, Git can't automatically decide which
version to keep. This is called a **merge conflict**.

VS Code highlights conflicts directly in the file and gives you buttons to choose:
- **Accept Current Change** — keep your version
- **Accept Incoming Change** — take the other person's version
- **Accept Both Changes** — keep both

After resolving all conflicts, stage and commit the file as normal.

---

## Common Workflow

Here's a typical day-to-day flow:

1. **Pull** to get the latest changes.
2. Make your edits and save files.
3. **Stage** the files you want to include.
4. Write a clear **commit message** and commit.
5. **Push** your changes so others can see them.

---

## Quick Reference

| Term | Plain English |
|------|--------------|
| Repository | A folder Git is tracking |
| Commit | A saved snapshot with a description |
| Stage | Selecting which changes to include in a commit |
| Branch | A separate copy of the project for trying out changes |
| Pull | Download the latest version from the shared repo |
| Push | Upload your commits to the shared repo |
| Merge conflict | Two people edited the same spot — needs a decision |

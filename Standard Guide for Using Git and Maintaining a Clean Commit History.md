## 1. Purpose

The purpose of this guide is to establish a unified process for managing project changes with Git, so that the commit history is readable, traceable, and maintainable.

All team members must follow the principles in this document when recording changes, so that each commit represents a specific and understandable change.

## 2. Core Principles

- Each commit must have a specific purpose.
- Files related to a single change must be included in one commit.
- Unrelated changes must be recorded in separate commits.
- The commit message must be short, precise, and express the purpose of the change.
- Before committing, the changed files and the content of the changes must be reviewed.
- Temporary files, generated outputs, confidential information, and unintended changes must not be included in commits.
- Avoid recording broad and unclear changes in a single commit.

## 3. Selecting Files for a Commit

### 3.1. Do Not Use `git add .`

Using the following command to record changes in this project is not permitted:

`git add .`

This command adds all visible changes in the current path and its subdirectories to the Staging area. As a result, unrelated files, temporary changes, or files that are not yet ready to be recorded may unintentionally enter the commit.

Instead, files must be selected explicitly and purposefully.

### 3.2. Adding Specific Files

To add a specific file:

`git add path/to/file.py`

To add multiple specific files:

`git add path/to/file.py path/to/related_file.py`

To add changes in a specific directory, if all changes in that directory are related to a single purpose:

`git add path/to/module/`

Note: Adding a directory can also bring all tracked changes within it into Staging; therefore, its contents must be reviewed first.

### 3.3. Grouping Related Files

Files must be grouped based on the purpose of the change, not merely based on their location.

For example, if a new feature includes the following:

- The model for the feature
- The service for processing data
- The serializer for the same feature
- The view for the same feature
- The tests related to it

If these files together form a complete and logical change, they must be included in one commit.

However, if other changes have been made at the same time to fix documentation or resolve an independent bug, those changes must be committed separately.

**Main rule:** Each commit must contain a set of related changes with a common purpose.

## 4. Standard Commit Process

For each commit, the following steps must be performed in order.

### Step One: Check Repository Status

`git status`

This command displays changed files, new files, and the Staging status.

### Step Two: Review Change Details

`git diff`

This command displays changes not yet staged.

To review changes in a specific file:

`git diff -- path/to/file.py`

### Step Three: Add Related Files

Explicitly add the files related to a specific change:

`git add path/to/file1.py path/to/file2.py`

### Step Four: Review Staging

`git diff --staged`

This step is mandatory. Before committing, it must be exactly clear what changes are going to be recorded.

To review the list of files ready to be committed:

`git diff --staged --name-only`

If an unrelated file has entered Staging, remove it:

`git restore --staged path/to/unrelated_file.py`

This command only removes the file from Staging and does not discard its changes.

### Step Five: Record the Commit

After ensuring the changes are correct:

`git commit -m "feat: add exhibitor registration validation"`

The commit message must match the type of change.

### Step Six: Verify the Result

`git status`

After committing, check the repository status to identify any remaining changes or unrecorded files.

## 5. Commit Message Writing Standard

The Conventional Commits pattern is used for commit messages.

### 5.1. Message Structure

`<type>(<scope>): <description>`

The components of this structure are:

- **type:** The type of change
- **scope:** The part or module affected by the change; optional.
- **description:** A short and precise description of the change

Example:

`feat(exhibitors): add eligibility approval`

In this example, a new feature for approving exhibitor eligibility has been added.

### 5.2. Allowed Commit Types

| Type | Usage | Example |
|---|---|---|
| `feat` | Adding a new feature | `feat(news): add article tagging` |
| `fix` | Fixing a bug | `fix(auth): resolve login validation error` |
| `refactor` | Restructuring code without changing expected behavior | `refactor(orders): simplify order service` |
| `docs` | Documentation changes | `docs(api): update endpoint documentation` |
| `test` | Adding or modifying tests | `test(exhibitors): cover booth reservation` |
| `style` | Code style changes without logic changes | `style(frontend): format component files` |
| `perf` | Performance improvements | `perf(products): optimize product queries` |
| `build` | Build system or dependency changes | `build(deps): update frontend dependencies` |
| `ci` | CI/CD configuration changes | `ci(github): update test workflow` |
| `chore` | General maintenance tasks | `chore(repo): update gitignore rules` |

The commit type must be chosen based on the main purpose of the change, not merely the type of file changed.

### 5.3. Description Writing Rules

- Messages must be written in English.
- The main description must be short, clear, and preferably in imperative form.
- The first word of the description must be written in lowercase.
- No period at the end of the description line.
- Avoid vague descriptions or those lacking useful information.
- The description must state what has changed; not merely announce that something has been done.

Inappropriate examples:

- `fix bug`
- `update files`
- `changes`
- `final update`
- `new changes`
- `fix stuff`

Appropriate examples:

- `fix(auth): handle expired access tokens`
- `feat(booths): prevent duplicate reservations`
- `docs(setup): document local development steps`
- `refactor(users): extract profile validation logic`

### 5.4. Using Scope

Scope is the name of the part of the project that the change relates to.

Appropriate examples:

- `auth`
- `users`
- `news`
- `exhibitors`
- `booths`
- `payments`
- `frontend`
- `api`

Scope must be specific and short. Using it is not mandatory for all commits, but in multi-module projects it helps with history readability.

## 6. Size and Scope of Each Commit

Commits must be small, independent, and meaningful; however, being small does not mean recording each file in a separate commit.

### An Appropriate Commit

Suppose a feature for booth reservation has been developed and the following changes are needed to complete it:

- Implementing reservation validation
- Connecting validation to the reservation service
- Adding tests related to this behavior

If these changes form a logical unit, they can be recorded in one commit.

Suggested message:

`feat(booths): validate booth reservation requests`

### Separate Commits

Suppose three tasks have been done at the same time:

1. Adding the news tagging feature

`feat(news): add article tagging`

2. Fixing the user login error

`fix(auth): handle invalid login credentials`

3. Correcting the project installation guide

`docs(setup): clarify installation instructions`

These changes must be recorded in three independent commits because they do not share a common purpose.

## 7. Managing New, Deleted, and Renamed Files

New, deleted, and renamed files must also be reviewed consciously.

To view their status:

`git status --short`

To remove a file from the repository and record its deletion in a commit:

`git add -u path/to/file.py`

This command stages changes and deletions of files already tracked by Git in the specified path; it does not add new files.

To rename a file, the following command can be used:

`git mv old_name.py new_name.py`

File renaming must be related to the purpose of the change, and combining extensive renames with unrelated modifications in one commit must be avoided.

## 8. Preventing Inappropriate Files from Entering the Repository

The following files must not enter the Git repository without a specific reason:

- Files containing passwords, API keys, and confidential information
- Environment files such as `.env` that contain private information
- Temporary and cache files
- Unnecessary program outputs
- Files generated by development tools that must remain in the local environment
- Large files or dependencies whose management must be handled another way

Unnecessary files must be defined in `.gitignore`.

Example:

```gitignore
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
node_modules/
```

The rules in `.gitignore` must be consistent with the project structure and technologies. For example, dependency files or outputs that must be recorded in the repository according to project convention must not be ignored.

**Note:** Adding a file to `.gitignore` does not remove it from Git if it has already been tracked by the repository. Also, confidential information that has already been committed is not removed from history merely by excluding the file from subsequent commits.

## 9. Managing Incomplete or Mistaken Commits

If a file has been mistakenly staged, use the following command:

`git restore --staged path/to/file.py`

If a commit has not yet been made and the changes to a file need to be reverted to the last commit, after careful review the following command can be used:

`git restore path/to/file.py`

This command discards the unstaged changes to the file; therefore, it must not be executed without certainty.

If the last commit has not yet been pushed and another file merely needs to be added to the same commit, `git commit --amend` can be used; provided that the new changes belong to the same purpose.

Avoid rewriting the history of shared and already-pushed commits without coordinating with the team.

## 10. Pre-Commit Checklist

Before running `git commit`, the following must be reviewed:

- [ ] The purpose of the commit is clear.
- [ ] Only files related to the same purpose have been staged.
- [ ] `git add .` has not been used.
- [ ] Changes have been reviewed with `git diff --staged`.
- [ ] No confidential, temporary, or unnecessary file has entered the commit.
- [ ] Related tests have been run, if necessary.
- [ ] The commit message has been written according to the established standard.
- [ ] Independent and unrelated changes have been placed in separate commits.

## 11. Example of a Complete Workflow

Suppose two files related to the news module have changed, and an unrelated file has also changed in the repository.

First, check the repository status:

```bash
git status
```

Review the changes:

```bash
git diff
```

Stage only the files related to the news module:

```bash
git add apps/news/services.py apps/news/views.py
```

Review the content ready to be committed:

```bash
git diff --staged
```

After confirmation, record the commit:

```bash
git commit -m "feat(news): add article publication workflow"
```

Finally, check the repository status again:

```bash
git status
```

The unrelated file has not been recorded in this commit and can be placed in a separate commit after being completed and independently reviewed.

## 12. Summary

Having a clean Git repository does not mean having few commits; rather, it means they are purposeful, understandable, and traceable.

The main rules of this guide are:

1. Each commit must have a single, specific purpose.

2. Files related to one change must be staged and committed together.

3. Do not use `git add .`; files must be selected explicitly and in a controlled manner.

4. The Staging content must be reviewed before every commit.

5. The commit message must be written using the Conventional Commits structure.

6. Independent changes, even if made within the same time frame, must be placed in separate commits.

7. Confidential, temporary, and unnecessary files must not enter the repository.
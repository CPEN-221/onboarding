# Git and GitHub

You repair a transit-classification method and then discover that another edit,
made yesterday, broke an unrelated case. Without recorded checkpoints, the two
changes are tangled together. Git lets you inspect the difference, save a coherent
snapshot, and compare it with earlier snapshots. GitHub gives that repository a
remote home for sharing and collaboration.

By the end, you should be able to:

- distinguish Git from GitHub and a working tree from a commit;
- clone a repository and identify its local and remote locations;
- inspect, stage, and commit one coherent change;
- synchronize with a remote using pull and push;
- create and merge a short-lived branch; and
- recover an unstaged edit without using destructive history-rewriting commands.

## 1. Git Is Local; GitHub Is a Host

**Git** is a version-control program. A Git **repository** stores a history of
snapshots called commits. Most Git operations—viewing differences, making commits,
and switching branches—work locally without contacting a server.

**GitHub** hosts remote Git repositories and adds accounts, access control, pull
requests, issues, and web views. A local commit is not automatically on GitHub.
Likewise, editing a file on GitHub does not silently update an existing local copy.

Use the repository visibility specified by the course activity. A public
repository exposes its history, including assignment code, to anyone. Changing a
repository from public to private later does not guarantee that earlier public
copies disappeared.

> **Design principle: make each commit a small, coherent, reproducible explanation
> of one change.**

## 2. Configure Your Author Identity

After installing Git, configure the name and email recorded in new commits:

```sh
git config --global user.name "Alex Student"
git config --global user.email "alex@example.com"
```

Inspect the result:

```sh
git config --global --list
```

These values label commits; they are not a GitHub password. Use an email connected
to your GitHub account if you want GitHub to associate command-line commits with
that account. GitHub also supports a private `noreply` address.

For authentication, choose either HTTPS or SSH. GitHub does not accept an account
password as the Git password for command-line HTTPS operations. GitHub recommends
GitHub CLI or Git Credential Manager for storing HTTPS credentials; Git for Windows
includes Git Credential Manager. SSH uses a key registered with your GitHub
account. Follow GitHub's current setup instructions rather than placing a token in
a remote URL or text file.

## 3. Clone the Repository Once

On the GitHub repository page, choose **Code**, select HTTPS or SSH according to
your configured authentication, and copy the URL. In the directory that should
contain your projects, run:

```sh
git clone https://github.com/ORGANIZATION/REPOSITORY.git
cd REPOSITORY
git status
git remote -v
```

Cloning creates a new project directory, downloads the repository history, checks
out its default branch, and records the source as a remote named `origin`.

Do not clone the same repository before every work session. Reuse the local clone
and synchronize it. Multiple clones with nearly identical names are a common cause
of editing one directory while building or committing another.

`git status` reports the current branch and working-tree state. `git remote -v`
reports the fetch and push URLs. Neither command changes anything.

<form class="quick-check" data-quick-check data-answer="local-only">
<fieldset>
<legend>You create a commit while disconnected from the network. Where does that commit exist?</legend>
<label><input type="radio" name="commit-location" value="github-only"> Only on GitHub</label>
<label><input type="radio" name="commit-location" value="local-only"> In the local Git repository until you push it</label>
<label><input type="radio" name="commit-location" value="working-file"> Only in the edited source file, outside Git</label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>Commit creation is local. A later <code>git push</code> sends commits to the configured remote.</p>
</details>
</form>

## 4. Understand the Three Local States

Git asks you to distinguish three views:

```text
working tree  --git add-->  staging area  --git commit-->  repository history
```

The **working tree** contains the files you edit. The **staging area**, also called
the index, specifies the exact content proposed for the next commit. The local
repository stores completed commits.

Suppose you change `TransitSummary.java` and add a test. Inspect before staging:

```sh
git status
git diff
```

`git diff` shows unstaged changes. Stage the two intended paths:

```sh
git add src/main/java/ca/ubc/ece/cpen221/prep/TransitSummary.java
git add src/test/java/ca/ubc/ece/cpen221/prep/TransitSummaryTest.java
```

Now inspect both views:

```sh
git diff
git diff --staged
git status
```

The ordinary diff is now empty for those paths because their current content is
staged. `git diff --staged` shows what the next commit would record. Staging does
not copy files to GitHub and does not make a backup commit.

<form class="quick-check" data-quick-check data-answer="staged-diff">
<fieldset>
<legend>After <code>git add TransitSummary.java</code>, which command reviews the version proposed for the next commit?</legend>
<label><input type="radio" name="review-stage" value="plain-diff"> <code>git diff</code></label>
<label><input type="radio" name="review-stage" value="staged-diff"> <code>git diff --staged</code></label>
<label><input type="radio" name="review-stage" value="remote"> <code>git remote -v</code></label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p>The staged diff compares the index with the current commit. The ordinary diff compares the working tree with the index.</p>
</details>
</form>

## 5. Commit a Tested Change

Before committing, run the project's checks and review the staged diff. Then:

```sh
git commit -m "Handle on-time transit predictions"
```

A useful message states what the change accomplishes. “Changes,” “work,” or
“assignment” provides little help when reading history. Use the imperative form:
“Handle…”, “Reject…”, “Document…”, or “Add…”.

Inspect the result:

```sh
git status
git log --oneline --decorate -5
```

The commit records only staged content. If you edited a staged file again before
committing, the new unstaged edit remains in the working tree and is not part of
that commit. This is a feature: the staging area allows a coherent snapshot even
when other work is present.

Generated directories such as `build/` should be named in `.gitignore` before
they are staged. Ignoring a path does not remove a file already tracked by Git.
Check `git status` after each build and investigate unexpected files rather than
blindly adding everything.

## 6. Pull and Push Deliberately

At the start of a work session, from a clean working tree, synchronize the current
branch:

```sh
git pull --ff-only
```

This fetches remote changes and advances the local branch only when no merge commit
is required. If Git refuses, read why before choosing a different command. You may
have local work to commit, a branch divergence to reconcile, or no upstream branch.

After local commits pass the build:

```sh
git push
```

Push transfers commits, not arbitrary uncommitted file changes. Verify on GitHub
that the expected branch shows the new commit. A successful local commit followed
by a failed push still leaves the commit safely in the local repository.

For a newly created branch, the first push may need:

```sh
git push -u origin branch-name
```

The `-u` option records the upstream relationship so later `git push` and `git
pull` know which remote branch corresponds to the local one.

### Common misconception

“GitHub is my backup” is incomplete. Git records only committed content, and
GitHub receives only pushed commits. An uncommitted file is absent from both Git
history and the remote. Use frequent coherent commits and verify pushes, while
still following an appropriate backup practice for work outside repositories.

## 7. Use a Branch for One Line of Work

A branch is a movable name for a line of commits. Before starting a focused change:

```sh
git switch main
git pull --ff-only
git switch -c improve-arrival-message
```

Edit, test, stage, and commit on that branch. Push it if it should be shared:

```sh
git push -u origin improve-arrival-message
```

On GitHub, a pull request presents the branch's commits and diff for review. A pull
request is a GitHub collaboration object, not a Git commit. When the change is
approved and merged, update the local `main`:

```sh
git switch main
git pull --ff-only
```

For a simple local exercise with no pull request, you can merge locally after
testing:

```sh
git switch main
git merge --ff-only improve-arrival-message
```

`--ff-only` is suitable when `main` has not diverged. Real collaboration sometimes
requires a merge or rebase decision. Do not choose one mechanically when Git says
the branches diverged; inspect the commit graph and follow the team's workflow.

## 8. Recover an Unstaged Edit

Git can restore tracked content, but the safety depends on what has been recorded.
Suppose you made an unwanted unstaged edit to one file. First inspect it:

```sh
git diff -- src/main/java/ca/ubc/ece/cpen221/prep/TransitSummary.java
```

If you are certain the entire unstaged change should be discarded:

```sh
git restore src/main/java/ca/ubc/ece/cpen221/prep/TransitSummary.java
```

This replaces the working-tree version with the staged version. An unstaged edit
that exists nowhere else can be lost. Name the path explicitly and inspect the diff
first.

To remove a file from the staging area while keeping the working edit:

```sh
git restore --staged path/to/file
```

These two commands solve different problems. Neither communicates with GitHub.
Avoid `git reset --hard` and forced pushes in an introductory workflow: they act on
broader state and can discard or rewrite work. Ask for help with the status, log,
and intended outcome before using them.

<form class="quick-check" data-quick-check data-answer="unstage">
<fieldset>
<legend>You staged the wrong file but want to keep its edits. Which command fits that intention?</legend>
<label><input type="radio" name="restore-choice" value="discard"> <code>git restore path/to/file</code></label>
<label><input type="radio" name="restore-choice" value="unstage"> <code>git restore --staged path/to/file</code></label>
<label><input type="radio" name="restore-choice" value="hard"> <code>git reset --hard</code></label>
</fieldset>
<details class="quick-check-explanation">
<summary>Show the explanation</summary>
<p><code>--staged</code> changes what is proposed for the next commit while leaving the working-tree edit in place. Restoring the working-tree path would discard that unstaged content.</p>
</details>
</form>

## 9. Handle a Merge Conflict as a Decision

A conflict occurs when Git cannot combine competing changes automatically. Git
marks the affected paths and `git status` reports an unmerged state. Open each
conflicted file and decide what the final program should say. Git places the
current branch text between a line beginning `<<<<<<< HEAD` and a line containing
`=======`. The incoming text follows, ending at a line beginning `>>>>>>>` and the
other branch name.

Do not keep both halves blindly. Remove the markers, create the intended valid
content, compile and test it, then stage the resolved file. Complete the merge only
after all conflicts are resolved and the combined behaviour is verified.

VS Code's merge editor can present the same choices graphically. It operates on the
same files and Git index as the terminal. Whatever interface you use, the key work
is a software decision about the combined result.

## 10. A Complete Daily Loop

Use this loop for a small assignment change:

```sh
git status
git switch main
git pull --ff-only
git switch -c classify-early-arrivals

# edit and run the project build

git status
git diff
git add path/to/source path/to/test
git diff --staged
git commit -m "Classify early arrivals"
git push -u origin classify-early-arrivals
```

Before copying it, explain what state each Git command reads and changes. Then
answer:

1. Which command proves that the build passes? (It is not a Git command.)
2. Which diff shows the exact proposed commit?
3. At what point does the new commit first exist?
4. At what point can a collaborator retrieve it from GitHub?
5. Which command would keep an edit but remove it from the proposed commit?

A command list is not a substitute for `git status`. Use status between transitions
until you can predict its output.

## 11. Summary

Git records local commits; GitHub hosts remote repositories and collaboration
features. The working tree, staging area, and commit history are distinct states.
Inspect with status and diff, stage only the intended content, test it, commit one
coherent change, and push the commit. Branches separate lines of work. Recovery
commands are safest when they name an exact path and you first understand which
recorded version will replace it.

## References

- [Pro Git: Recording Changes to the Repository](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
- [Git Reference: `git switch`](https://git-scm.com/docs/git-switch)
- [Git Reference: `git restore`](https://git-scm.com/docs/git-restore)
- [GitHub Docs: Set up Git](https://docs.github.com/en/get-started/git-basics/set-up-git)
- [GitHub Docs: Caching your GitHub credentials in Git](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git)
- [GitHub Docs: Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- [GitHub Docs: Pushing commits to a remote repository](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)

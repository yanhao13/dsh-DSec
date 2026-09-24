# Code-Change Tracking — 5 Tools Applied to `master@{10day}...master@{7day}`

**Window resolved:** GitHub's `master@{10day}` = commit `c291e796` (2026-09-10T22:17:09+08:00, the `release-0.1.5-sync-master` merge; root version `0.1.5-rc.2`); `master@{7day}` = `ddefc45f` (2026-09-17T21:19:19+08:00, `Merge pull request #4469 … release-dsh-0.1.6-alpha.2`; root version `0.1.6-alpha.2`).
**Verified counts:** 1,548 commits · 4,851 files changed (GitHub) — matches the stated "Commits 1,548". Local git merge-base diff resolves 4,788 files (rename-aware) / 4,879 (no-renames); GitHub's 4,851 sits between them, i.e. GitHub collapses ~28 add/delete pairs into renames vs git `-M`'s 91.
**Contributors:** GitHub reports 18 contributors (distinct accounts); the raw log resolves 32 distinct author name+email pairs (no bots).
**Source data:** blobless clone `dsh-upstream/` (fetched to `477b4f42`); blobs fetched on demand for the diff.

## Applied matrix

| Tool | Input Source (this run) | Primary Function Applied | Ideal Lifecycle Step | Artifact |
|------|-------------------------|--------------------------|----------------------|----------|
| `pr-reference` | Local git history: `c291e796..ddefc45f` | Generated `<commit_history>` XML with 1,548 commits (subject + body CDATA) and the full unified diff of 4,788 files; companion changed-file table + chunk index | Development — preparing a submission | [`pr-reference/pr-reference.xml`](pr-reference/pr-reference.xml) |
| `change` | Workspace delta: 4,879 committed paths (no-renames) → 310 changed packages | Classified each changed package `minor`/`patch` and emitted a beachball-schema change file + repo-native `change-scope.json` | Commit — categorizing semantic per-package changes | [`change/`](change/) (scope + report + sample change file) |
| `wiki-changelog` | Historical git log lines: 1,548 commits (1,033 kept after noise-merge filtering) | Grouped by day into the 7 emoji categories with linked commit hashes | Tracking — monitoring development updates | [`wiki-changelog/wiki-changelog.md`](wiki-changelog/wiki-changelog.md) |
| `write-changelog` | First-parent PR chain of the window (143 fp commits → 143 deduped PR/direct entries) | Aggregated merged PR titles into Changes (80) / Fixes (45) / Thank You (0 — all internal) / Skip (18) draft for `## 0.1.6-alpha.2` | Release — building early release draft outlines | [`write-changelog/CHANGELOG.draft.md`](write-changelog/CHANGELOG.draft.md) |
| `docs-changelog` | Automated release strings: `v0.1.6-alpha.2` + processed What's Changed body | Path B.2 (alpha preview, non-`.0`): 5 stripped bold highlights, `preview.md`, `index.md` announcement with PR links, Full Changelog = this compare URL | Deployment — publishing public announcements | [`docs-changelog/preview.md`](docs-changelog/preview.md), [`docs-changelog/index.md`](docs-changelog/index.md) |

## Artifact inventory

| Artifact | Contents |
|----------|----------|
| `pr-reference/pr-reference.xml` | `<commit_history>` XML: 1,548 `<commit>` elements (with message bodies), `<full_diff>` of the 4,788-file window (39 MB) |
| `pr-reference/list-changed-files.md` | Markdown table of all 4,788 files with change type (`added`/`modified`/`deleted`/`renamed`) |
| `pr-reference/chunk-info.txt` | Base/head SHAs + commit/file/author counts |
| `change/change-scope.json` | Repo-native `ChangeScopeReport` schema: base/head/mergeBase + 4,879 committed paths |
| `change/CHANGE-REPORT.md` | Classification summary, 31 new packages, per-package sample evidence |
| `change/deepseek-ai-dsh-2026-09-17-21-19.json` | Representative beachball-schema change file `{type, comment, packageName, email}` |
| `wiki-changelog/wiki-changelog.md` | Daily sections with category bullets, merged duplicates, linked commit hashes, per-day overview line |
| `write-changelog/CHANGELOG.draft.md` | `## 0.1.6-alpha.2` entry in the skill's exact format (Changes / Fixes / Thank You / Skip) |
| `docs-changelog/preview.md` | `# Preview release: v0.1.6-alpha.2`, 5 bold-titled highlights (no PR numbers/authors), What's Changed with `[#N](url)` links, Full Changelog |
| `docs-changelog/index.md` | Announcement entry with PR links + Full Changelog link |

## Tool-to-tool handoffs (lifecycle pipeline)

```
pr-reference ──(4,879 paths)──▶ change ──(1,548 commits)──▶ wiki-changelog
                                   │
                                   └──(PR buckets)──▶ write-changelog ──(v0.1.6-alpha.2 + body)──▶ docs-changelog
```

## Adaptation notes (verified against each skill's SKILL.md)

- **pr-reference** (hve-core): output lands in `pr-reference/`; `list-changed-files` and chunk-info companions applied. Commit bodies are included so merge commits carry their PR titles.
- **change** (fluentui): the repo has no beachball; used the repo-native `change-scope.ts` report plus beachball-schema change files. `major` is never assigned without explicit approval; 31 packages new in this window are classified `minor`. 310 total changed packages = 302 product (`@deepseek-ai/dsh-*` / `node-addon-system*`) + 8 vendor/other.
- **wiki-changelog** (microsoft/skills deep-wiki): `REPO_URL` from the git remote; noise merges (`Merge …`) dropped and duplicate descriptions merged; commit hashes linked.
- **write-changelog** (vscode-pull-request-github): milestone queries replaced by the equivalent first-parent chain over the window. All PRs merge from `deepseek-harness/*` (internal), so Thank You is empty and omitted. PR titles come from merge-commit bodies.
- **docs-changelog** (gemini-cli): `alpha` version → Path B.2 preview; highlights strip PR numbers, links, and author names; What's Changed keeps `[#N](url)` formatting; Full Changelog is the requested compare URL.

## Notes on this run

- The window is a 7-day mainline window (Sep 10 → Sep 17) but the commit graph carries author dates back to Aug 19 (long-lived feature branches merged in-window), so `wiki-changelog` spans 23 calendar days.
- 31 new packages landed, led by the **SSH family** (`fs-ssh`, `sandbox-ssh`, `ssh`, `subprocess-ssh`), the **PTC runtime family** (`ptc-runtime`, `-node`, `workflow-ptc`, `experimental/ptc-runtime-python`), the **browser/computer-use family** (`browser-use`, `computer-use`, `experimental/browser-use-{chrome-devtools-mcp,playwright-mcp,runtime,stagehand-native}`, `experimental/computer-use-cua-driver-{mcp,native}`), plus `document/office-to-pdf`, `skill/skill-office`, `deliverables/{tool-present,workspace-changes}`, `compaction/compaction-image-offload`, and `mcp/mcp-resources`.
- Notable direction: DeepSeek LLM moves to the **Messages protocol** by default with Files parity ([#3682](https://github.com/deepseek-ai/deepseek-harness/pull/3682), [#4089](https://github.com/deepseek-ai/deepseek-harness/pull/4089)) and drops the V4 Flash default models ([#4313](https://github.com/deepseek-ai/deepseek-harness/pull/4313)).
- The head commit is a squashed release-sync merge; the underlying window head resolves to root version `0.1.6-alpha.2`.

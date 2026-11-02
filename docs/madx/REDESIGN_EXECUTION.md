# Redesign native validation procedure

Status: **executed at `88d970167a9eb743a224a839491ec2631247f401`** after explicit user
authorization for `codex/madx-desktop-redesign` and the single stale CLI test correction.
Repository `MadXLeo/MadX-Agent-OS`: CI 41400903428, unpublished image 41413455726 and installer
41438712212 passed. Evidence and remaining interactive/performance gates are in ASTRA_PROGRESS.md.
The commands below are the retained procedure, not a request to rerun or publish this build.
Keep validated source revisions separate from later documentation-only commits.

## Preflight and single-branch push

From the redesign worktree, compare the full SHA printed here with the user's approval. If it
differs, stop before pushing. Review outgoing history/diff and credential scan again if changed.

```powershell
$repo = 'MadXLeo/MadX-Agent-OS'
$branch = 'codex/madx-desktop-redesign'
if ((git branch --show-current).Trim() -ne $branch) { throw 'Wrong branch' }
if (git status --porcelain) { throw 'Uncommitted changes' }
$expected = (git rev-parse HEAD).Trim()
git log --oneline 2e844ca74b87b04395bb6232b368edc5b8bea451..HEAD
git diff --stat 2e844ca74b87b04395bb6232b368edc5b8bea451..HEAD
git remote get-url origin
$expected
# Proceed only when this full SHA and origin match the authorization.
git push origin "HEAD:refs/heads/$branch"
if ($LASTEXITCODE) { throw 'Push failed; do not force-push' }
gh run list --repo $repo --workflow ci.yml --branch $branch --commit $expected --limit 5 --json databaseId,headSha,status,conclusion,url
```

That push triggers CI only. The image workflow does not listen for feature-branch pushes.
Read the CI run's `headSha`, jobs, skips and artifact reports. Unexpected Linux skips are failures;
do not count a cancelled job as passed. Stop waiting and return the run link to the user.
After the user reports completion, inspect actual results. If a fix changes the SHA, rerun CI
and use the new authorized revision consistently for all following steps.

## Unpublished image and ISO

The image and installer workflows were registered and manually executed during the prior OS
milestone. Confirm they are still active through the API; the default-branch web UI need not
offer a Run button for a workflow registered on the validation branch. If absent/disabled, stop;
do not merge to main or push another branch as a workaround.

```powershell
gh api "repos/$repo/actions/workflows/image.yml" --jq '{id,state,path}'
gh api "repos/$repo/actions/workflows/installer-test.yml" --jq '{id,state,path}'
$remoteHead = (gh api "repos/$repo/git/ref/heads/$branch" --jq '.object.sha').Trim()
if ($LASTEXITCODE -or $remoteHead -ne $expected) { throw 'Source changed' }
gh workflow run image.yml --repo $repo --ref $branch -f publish=false -f disks=true
if ($LASTEXITCODE) { throw 'Image dispatch failed' }
gh run list --repo $repo --workflow image.yml --branch $branch --commit $expected --event workflow_dispatch --limit 5 --json databaseId,headSha,status,conclusion,url
```

Select the newly dispatched run by event/time/full SHA, record its ID and link, then stop waiting.
Do not dispatch if a CI job failed or has unexplained skips. This branch's PUBLISH expression
forces false even if the input were accidentally true. No registry publication, release or tag.

On completion, inspect every default architecture and NVIDIA job rather than only the aggregate
conclusion (NVIDIA is continue-on-error). Download validation reports and ISO parts, verify ZIP
integrity, reconstruct only inside the artifact directory and verify the manifest SHA-256.
Check image labels/source revision, package contents, symlinks and actual Hermes commit; record
any pin drift without silently changing it. `disks=true` produces the validation ISO on the
unpublished path, not every published-release VM format. Never call an artifact bootable until
the UEFI job actually boots it. No ISO means no installer dispatch.

## Isolated UEFI installation

Set imageRun to the verified successful image run ID from the preceding stage. Keep tag blank
so no release path is used. The workflow checks repository/workflow/source provenance and ISO
checksums; all three tests run only inside disposable hosted VMs with synthetic disks.

```powershell
$imageRun = Read-Host 'Verified image run ID'
if ($imageRun -notmatch '^\d+$') { throw 'Invalid run ID' }
$built = gh run view $imageRun --repo $repo --json headSha,conclusion | ConvertFrom-Json
if ($LASTEXITCODE -or $built.headSha -ne $expected -or $built.conclusion -ne 'success') { throw 'Image source or result mismatch' }
if ((gh api "repos/$repo/git/ref/heads/$branch" --jq '.object.sha').Trim() -ne $expected) { throw 'Source changed' }
gh workflow run installer-test.yml --repo $repo --ref $branch -f "image_run=$imageRun" -f tag= -f account=madx-test
if ($LASTEXITCODE) { throw 'Installer dispatch failed' }
gh run list --repo $repo --workflow installer-test.yml --branch $branch --commit $expected --event workflow_dispatch --limit 5 --json databaseId,headSha,status,conclusion,url
```

Return the link and stop waiting. On completion collect installation/reboot/unlock logs,
graphical screenshots, service evidence and protected synthetic-disk hashes. Investigate real
errors before changing installer code; do not assume GRUB failed. Then perform interactive guest
acceptance and performance measurement described in REMAINING_ISSUES.md. Credentials and private
model output must not be uploaded to logs or screenshots. Host disks/EFI/firmware, physical
installation, paid infrastructure and new host software remain outside authorization.

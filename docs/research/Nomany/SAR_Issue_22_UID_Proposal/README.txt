SAR ISSUE 22: SENSOR UID DEFINITION PROPOSAL
Prepared October 28, 2026, for Kazi Tamim Nomany with AI assistance.

READ FIRST
Open PROPOSAL_FOR_REVIEW.md. Section 1 gives the recommendation.
Section 10 lists the decisions for Professor Smith.
The research/proposal work is prepared. Policy approval and implementation are separate.

CONTENTS
PROPOSAL_FOR_REVIEW.md: standalone review copy with pinned source links.
docs/sensors/: three proposed repository files, with their original relative paths.
changes.patch: complete change against the baseline in source_and_scope.json.
verification.json: checks performed and their limits.
PULL_REQUEST_DRAFT.md: title and description ready for a later submission.
source_and_scope.json: source version, local commit, and file hashes.

ADD TO YOUR LOCAL REPOSITORY
Use a separate review branch in your SAR clone.
Copy the three files from docs/sensors/ into the matching folder in your clone.
Review the changes in GitHub Desktop before committing.
If your files have changed since the baseline, reconcile them instead of overwriting.
Alternatively, from a clean compatible checkout, check and apply the patch:
git apply --check /full/path/to/changes.patch
git apply /full/path/to/changes.patch

SUBMISSION STATUS
This package has not been uploaded to GitHub. The connected account has read access,
but no push access to CHI-CityTech/Self-Aware-Room. No pull request or issue comment
was posted. Issue 22 remains open. Publishing requires an authorized writable branch
or fork. The draft does not change real inventory IDs or runtime code.

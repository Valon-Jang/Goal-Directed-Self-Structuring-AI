# Exact operational observations

## github/actions-read/named-workflow-runs-url

2026-09-13. State: VERIFIED_FAST_PATH, scope: the current ChatGPT GitHub connector's `fetch` action, not GitHub REST generally.

Observed failure: `/repos/{owner}/{repo}/actions/workflows/{workflow-name}.yml/runs?...` returned connector `INVALID_ARGUMENT / HTTP 400 / URL is not an allowed public GitHub repository or search endpoint`. This URL family was also rejected during E0.1. It is a connector surface limitation, not a workflow/model/research failure.

Verified fallback: `/repos/{owner}/{repo}/actions/runs?branch={encoded-branch}&per_page=3` returned the requested E002 run 34758574472, head commit 5fd5052b7aa30cc979775d78d5f994734f4fbbca and completed status. Match branch, exact commit and workflow path; then use dedicated `fetch_workflow_run_jobs`, `fetch_workflow_job_logs`, `fetch_workflow_run_artifacts` and `download_workflow_artifact` for the observed IDs. Do not retry the rejected named-workflow URL unchanged.

## local/public-repository-materialization/dns

2026-09-13. The present container's direct `git clone` of the public research repository failed with `Could not resolve host: github.com`, before source materialization or any remote write. This is an environment transport result, not a repository visibility or authentication conclusion. Do not repeat direct cloning in this unchanged runtime. Use the connected GitHub reader/writer and supported artifact reference flow; local code files are working copies, not the project authority. No credential search or network restriction bypass is warranted.

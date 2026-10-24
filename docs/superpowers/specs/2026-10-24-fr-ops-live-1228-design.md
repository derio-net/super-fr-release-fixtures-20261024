# Disposable fr-ops live acceptance fixture

## Requirements

R1. An operator can observe the DevOps gate apply one harmless pre-merge op,
merge a real disposable PR, satisfy a post-merge ready check, apply one harmless
post-merge op, pass the recorded DevOps gate, and see both op states from a
fresh checkout using the shared fixture-only state volume.

## Verification

strategy: candidate
gate: developer
gate: fixture-devops-live=devops
- fixture-devops-live: live — requires the released fr in the real disposable
  ops profile and a real disposable PR merge; candidate/fake-forge scenarios do
  not prove this.

## Test Plan

- [devops] Confirm the local pre-merge op, real disposable PR merge, post-merge
  readiness and local post-merge op; record the outcome as `ran` with the
  fixture PR URL and observed marker names (no credentials or host paths).

## Implementation Plans

| Plan | Repo | File | Depends on |
|------|------|------|------------|
| 2026-10-24-fr-ops-live-1228 | `derio-net/super-fr-release-fixtures-20261024` | `2026-10-24-fr-ops-live-1228` | — |

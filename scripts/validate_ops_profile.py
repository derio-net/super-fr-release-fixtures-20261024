#!/usr/bin/env python3
"""Validate the disposable fixture's static ops-profile trust boundary."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / ".devcontainer" / "ops" / "devcontainer.json"
PROFILES = ROOT / ".devcontainer" / "fr-profiles.yaml"
TRUST_SOURCE = "${localEnv:HOME}/.local/state/fr/ops-trust"
TRUST_TARGET = "/run/fr-ops-trust"


def main() -> None:
    config = json.loads(PROFILE.read_text())
    env = config.get("containerEnv", {})
    mounts = config.get("mounts", [])
    profile_lines = PROFILES.read_text().splitlines()

    if profile_lines.count("profiles:") != 1:
        raise SystemExit("profile registry must contain exactly one top-level profiles key")
    expected_profile = ["profiles:", "  ops:"]
    try:
        start = profile_lines.index(expected_profile[0])
    except ValueError as exc:
        raise SystemExit("profile registry lacks top-level profiles mapping") from exc
    profiles_end = next(
        (index for index in range(start + 1, len(profile_lines))
         if profile_lines[index] and not profile_lines[index][0].isspace()),
        len(profile_lines),
    )
    profiles_section = profile_lines[start:profiles_end]
    if profiles_section[:2] != expected_profile or profiles_section.count("  ops:") != 1:
        raise SystemExit("ops profile is not declared under profiles")
    ops_end = next(
        (index for index in range(2, len(profiles_section))
         if profiles_section[index].startswith("  ")
         and not profiles_section[index].startswith("    ")),
        len(profiles_section),
    )
    ops_section = profiles_section[1:ops_end]
    ops_flags = [line for line in ops_section if line.startswith("    ops:")]
    if ops_flags != ["    ops: true"]:
        raise SystemExit("ops profile is not declared with ops: true")
    if env.get("FR_PROFILE") != "ops":
        raise SystemExit("FR_PROFILE must be ops")
    if env.get("FR_OPS_TRUST_DIR") != TRUST_TARGET:
        raise SystemExit("FR_OPS_TRUST_DIR must point to /run/fr-ops-trust")

    trust_mounts = [mount for mount in mounts if f"target={TRUST_TARGET}" in mount.split(",")]
    if len(trust_mounts) != 1:
        raise SystemExit("expected exactly one mount targeting /run/fr-ops-trust")
    mount = trust_mounts[0]
    fields = set(mount.split(","))
    expected_mount = {f"source={TRUST_SOURCE}", f"target={TRUST_TARGET}", "type=bind", "readonly"}
    if fields != expected_mount:
        raise SystemExit("ops-trust mount must be exactly the expected read-only host bind")

    print("ops profile static trust-boundary validation passed")


if __name__ == "__main__":
    main()

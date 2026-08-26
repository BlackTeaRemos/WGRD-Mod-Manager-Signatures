import subprocess

from validation.paths import KEYS_DIRECTORY, PLACEHOLDER_NAME, REVOKED_DIRECTORY

KEY_ADDITION_LIMIT = 1
REVOCATION_ADDITION_LIMIT = 1


def ChangedPaths(baseRef, selector, directory, problems):
    command = [
        "git",
        "diff",
        f"--diff-filter={selector}",
        "--name-only",
        f"{baseRef}...HEAD",
        "--",
        str(directory),
    ]

    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        problems.append("diff read failed")
        return None

    entries = []
    for line in completed.stdout.splitlines():
        entry = line.strip()
        if not entry:
            continue
        if entry.endswith(PLACEHOLDER_NAME):
            continue
        entries.append(entry)

    return entries


def CheckAppendOnly(baseRef, problems):
    for directory in (KEYS_DIRECTORY, REVOKED_DIRECTORY):
        rewritten = ChangedPaths(baseRef, "DM", directory, problems)
        if rewritten is None:
            continue

        for entry in rewritten:
            problems.append(f"{entry} rewritten not appended")


def CheckChangeBudget(baseRef, problems):
    addedKeys = ChangedPaths(baseRef, "A", KEYS_DIRECTORY, problems)
    if addedKeys is not None and len(addedKeys) > KEY_ADDITION_LIMIT:
        problems.append("too many keys added")

    addedRevocations = ChangedPaths(baseRef, "A", REVOKED_DIRECTORY, problems)
    if addedRevocations is not None and len(addedRevocations) > REVOCATION_ADDITION_LIMIT:
        problems.append("too many revocations added")

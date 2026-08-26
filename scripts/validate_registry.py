import argparse
import sys

from validation.changes import CheckAppendOnly, CheckChangeBudget
from validation.keys import CollectKeys
from validation.revocations import CollectRevocations

MAINTAINER_ASSOCIATIONS = ("OWNER", "MEMBER", "COLLABORATOR")


def RequiresSignature(authorAssociation):
    if authorAssociation is None:
        return False

    return authorAssociation not in MAINTAINER_ASSOCIATIONS


def Main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--base", default=None)
    parser.add_argument("--author-association", dest="authorAssociation", default=None)
    arguments = parser.parse_args()

    problems = []

    registered = CollectKeys(problems)
    CollectRevocations(registered, RequiresSignature(arguments.authorAssociation), problems)

    if arguments.base:
        CheckAppendOnly(arguments.base, problems)
        CheckChangeBudget(arguments.base, problems)

    if problems:
        for problem in problems:
            print(problem)
        return 1

    print(f"registry valid {len(registered)} keys")
    return 0


if __name__ == "__main__":
    sys.exit(Main())

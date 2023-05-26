import logging
import subprocess
from typing import List

from .consts import MAX_CHAR


def getBranches() -> List[str]:
    ret = []
    try:
        ret.extend(subprocess.run(
            "git branch -a --format \"%(refname)\"", stdout=subprocess.PIPE, shell=True).stdout.decode('UTF-8').splitlines())
    except:
        logging.error("Unable to retreive branches")
    try:
        ret.extend(subprocess.run(
            "git log --pretty=%H -n 10", stdout=subprocess.PIPE, shell=True).stdout.decode('UTF-8').splitlines())
    except:
        logging.error("Unable to retreive commits")
    return ret

def getCommitMessages(new_commit: str, old_commit: str) -> str:
    return subprocess.run(f'git log --format="(%s)" {old_commit}...{new_commit}', stdout=subprocess.PIPE, shell=True).stdout.decode('UTF-8')

def getDiff(newCommit: str, oldCommit: str) -> List[str]:
    out = subprocess.run(
        f'git diff {oldCommit}...{newCommit}', stdout=subprocess.PIPE, shell=True).stdout.decode('UTF-8')
    split = out.strip().split("diff --git")
    split = [i for i in split if i and len(i) <= MAX_CHAR]
    return split

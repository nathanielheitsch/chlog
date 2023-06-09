import asyncio
import logging
import sys
from typing import Optional
import inquirer
import typer
from typing_extensions import Annotated
from rich.progress import Progress
from common.ai_service import AIService
from common.git import getBranches, getCommitMessages, getDiff
from lib.writer import Writer

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s - %(message)s')

loader_total = 0

def selectBranch(base=True) -> str:
    branches = getBranches()
    questions = [
        inquirer.List('branch',
                      message="Which branch/commit would you like to compare {} ({})".format(
                          "with" if not base else "against", "newer" if not base else "older"),
                      choices=branches,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers["branch"]


def gen(new_commit: Annotated[Optional[str], typer.Argument()] = None, old_commit: Annotated[Optional[str], typer.Argument()] = None, token: Annotated[str, typer.Option(help="API Token for AI Services")] = None, title: Annotated[str, typer.Option(help="Title of the changelog")] = None):
    if new_commit == None:
        new_commit = selectBranch(False)
    if old_commit == None:
        old_commit = selectBranch()
    diffs = getDiff(new_commit, old_commit)
    if diffs == None:
        logging.info(
            f'There is no difference between {old_commit} and {new_commit}')
        return
    commit_messages = getCommitMessages(new_commit, old_commit)
    logging.info("Processing {} diffs over {} commits".format(len(diffs), len(commit_messages.splitlines())))
    asyncio.run(pursue(diffs, commit_messages, token, title if title else f"{old_commit} to {new_commit}"))


def writeDiff(result):
    logging.debug(result)
    return Writer.writeDiff(result)


async def pursue(diffs, commit_messages, token: str, title: str):
    ai_service = AIService(token)
    Writer.init()
    with Progress(
        transient=True,
    ) as progress:
        diff_len = len(diffs)
        task = progress.add_task(description="Processing...", total=diff_len)
        chlog = ""
        i=0
        def inc(s: str):
            nonlocal chlog
            nonlocal i
            i += 1
            progress.update(task, advance=1, description="Processing {}/{}".format(str(i).rjust(len(str(diff_len)) - len(str(i)), " "), diff_len))
            chlog += s
        await ai_service.ai.chlog(diffs, commit_messages, inc)
        progress.update(task, description="Finalizing Summary...")
        summary = await ai_service.ai.summarize(chlog, commit_messages)
        while summary.startswith("\n"):
            summary = summary[1:]
        while summary.endswith("\n"):
            summary = summary[:-1]
        progress.update(task, advance=1)
        writeDiff(f"{title}\n{summary}")
        logging.info("Success! See the CHANGELOG")


if __name__ == "__main__":
    typer.run(gen)

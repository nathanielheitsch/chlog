import asyncio
import logging
import sys
from typing import Optional
import inquirer
import typer
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn
from lib.ai_service import AIService
from lib.git import getBranches, getDiff
from lib.writer import Writer

from lib.consts import TOKEN_ENV_NAME

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s - %(message)s')

wr = Writer()
loader_total = 0


def selectBranch(base=True) -> str:
    branches = getBranches()
    questions = [
        inquirer.List('branch',
                      message="Which branch/commit would you like to compare {}".format(
                          "against" if base else "with"),
                      choices=branches,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers["branch"]


def gen(new_commit: Annotated[Optional[str], typer.Argument()] = None, old_commit: Annotated[Optional[str], typer.Argument()] = None):
    if new_commit == None:
        new_commit = selectBranch(False)
    if old_commit == None:
        old_commit = selectBranch()
    diffs = getDiff(new_commit, old_commit)

    if diffs == None:
        logging.info(
            f'There is no difference between {old_commit} and {new_commit}')
        return
    asyncio.run(pursue(diffs))


def writeDiff(result):
    logging.debug(result)
    return wr.writeDiff(result)


async def pursue(diffs):
    ai_service = AIService()
    with Progress(
        transient=True,
    ) as progress:
        task = progress.add_task(description="Processing...", total=len(diffs))
        def inc(s: str):
            progress.update(task, advance=1)
            writeDiff(s)
        await ai_service.processDiffs(diffs, inc)


if __name__ == "__main__":
    typer.run(gen)

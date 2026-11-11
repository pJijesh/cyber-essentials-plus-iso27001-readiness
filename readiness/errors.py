"""Error type used for problems the user can fix, such as bad input files."""

from __future__ import annotations


class ReadinessError(Exception):
    """Raised with one or more readable problem descriptions.

    The command line prints every problem and exits with status 2.
    """

    def __init__(self, problems: list[str] | str):
        if isinstance(problems, str):
            problems = [problems]
        self.problems = list(problems)
        super().__init__("; ".join(self.problems))

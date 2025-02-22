"""Implementation of TaskPath.

Functions:
_block -- wrap multiple statements into a single block.

Classes:
GeneratorList -- implementation of generator list wrappers.

TODO
"""

# used for delayed evaluation of typing until python 3.11 becomes mainstream
from __future__ import annotations
from typing import Optional, Union, List


class PathStringMalformed(Exception):
    """Implementation of path string exceptions."""

    def __init__(self, *args):
        """Create a new PathStringMalformed exception."""
        Exception.__init__(self, *args)


class TaskPathNode:
    def __init__(self, name: str, n: Optional[int] = 0):
        self.name: str = name
        self.n: int = n


class TaskPath:
    def __init__(self, path: Union[str, List]):
        if type(path) is str:
            if path == "":
                raise PathStringMalformed("No empty paths allowed.")
            self.path = []
            for part in path.split("/"):
                if part == "":
                    print("WARN: Paths don't end on an '/' and only support single '/'.")  # TODO: Make this nicer?
                    continue
                name_and_n = part.split(".")
                if len(name_and_n) == 1:
                    self.path.append(TaskPathNode(name_and_n[0], 0))
                elif len(name_and_n) == 2:
                    if not name_and_n[1].isnumeric():
                        raise PathStringMalformed("The indicator after the '.' needs to be a number.")
                    self.path.append(TaskPathNode(name_and_n[0], int(name_and_n[1])))
                else:
                    raise PathStringMalformed("Only one '.' after the node's name.")
        else:
            self.path = path

    def __len__(self):
        return len(self.path)

    # TODO: Implement accessors with slice support?
    def cut_off_head(self) -> TaskPath:
        return TaskPath(self.path[1:])


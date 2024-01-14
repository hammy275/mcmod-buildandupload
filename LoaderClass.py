from dataclasses import dataclass
from typing import List, Union

from DependencyClass import Dependency


@dataclass
class Loader:
    folder_name: str
    loader_tags: List[str]
    dependencies: List[Dependency]
    minecraft_versions: Union[List[str], None]

    def __str__(self):
        return "Folder name {} for loaders {}".format(self.folder_name, ", ".join(self.loader_tags))

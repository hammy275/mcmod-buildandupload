from dataclasses import dataclass
from typing import Union

@dataclass
class Version:
    branch_name: str
    minecraft_version: str
    java_home: Union[str, None]

    def __str__(self):
        if self.java_home is None:
            return "Branch {} for MC version {}".format(self.branch_name, self.minecraft_version)
        else:
            return "Branch {} for MC version {} using JAVA_HOME {}".format(self.branch_name,
                                                                           self.minecraft_version, self.java_home)

from dataclasses import dataclass

@dataclass
class Version:
    branch_name: str
    minecraft_version: str

    def __str__(self):
        return "Branch {} for MC version {}".format(self.branch_name, self.minecraft_version)

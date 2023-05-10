from dataclasses import dataclass


@dataclass
class Dependency:
    modrinth_project_id: str
    curseforge_project_slug: str
    dependency_type: str

    def to_modrinth_dict(self):
        return {
            "version_id": None,
            "project_id": self.modrinth_project_id,
            "file_name": None,
            "dependency_type": self.dependency_type
        }

    def to_curseforge_dict(self):
        dep_type = self.dependency_type
        if self.dependency_type in ["required", "optional"]:
            dep_type = self.dependency_type + "Dependency"
        elif self.dependency_type == "embedded":
            dep_type = self.dependency_type + "Library"
        return {
            "slug": self.curseforge_project_slug,
            "type": dep_type
        }

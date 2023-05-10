import tempfile
from os import getenv, path
from typing import List

from DependencyClass import Dependency
from LoaderClass import Loader
from VersionClass import Version

"""=-=-=-= Basic Configuration =-=-=-="""

# All loaders to build for.
# folder_name is the folder which contains the outputs of that build
# loader_tags is a list of lowercase modloaders that this build supports
# dependencies is a list of Dependency objects with a modrinth_project_id, curseforge_project_id, and a dependency type
# (required, optional, incompatible, or embedded)
LOADERS: List[Loader] = [
    Loader(folder_name="fabric", loader_tags=["fabric", "quilt"],
           dependencies=[Dependency(modrinth_project_id="lhGA9TYQ", dependency_type="required",
                                    curseforge_project_slug="architectury-api"),
                         Dependency(modrinth_project_id="B3INNxum", dependency_type="optional",
                                    curseforge_project_slug="mc-vr-api"),
                         Dependency(modrinth_project_id="ohNO6lps", dependency_type="required",
                                    curseforge_project_slug="forge-config-api-port-fabric")]),
    Loader(folder_name="forge", loader_tags=["forge"],
           dependencies=[Dependency(modrinth_project_id="lhGA9TYQ", dependency_type="required",
                                    curseforge_project_slug="architectury-api"),
                         Dependency(modrinth_project_id="B3INNxum", dependency_type="optional",
                                    curseforge_project_slug="mc-vr-api")])
]
# Version number for this mod release
VERSION: str = "1.3.3"
# Version type. Must be "release", "beta", or "alpha"
VERSION_TYPE: str = "release"
# Whether to publish to CurseForge
PUBLISH_CURSEFORGE: bool = True
# Whether to publish to Modrinth
PUBLISH_MODRINTH: bool = True
# Root path for project location
PROJECT_PATH: str = "."
# Path to changelog
CHANGELOG_PATH: str = "changelog.md"

# All versions to build your mod for.
# branch_name is the name of the Git branch and minecraft_version is the Minecraft version this
# should be published under.
BUILD_VERSIONS: List[Version] = [
    Version(branch_name="1.18.x-multiloader", minecraft_version="1.18.2"),
    Version(branch_name="1.19.x", minecraft_version="1.19.2"),
    Version(branch_name="1.19.3", minecraft_version="1.19.3"),
    Version(branch_name="1.19.4", minecraft_version="1.19.4"),
]

# Project ID for Modrinth uploads
MODRINTH_PROJECT_ID: str = "XJ9is6vj"
# Project ID for CurseForge uploads as a string
CURSEFORGE_PROJECT_ID: str = "607017"

# Name format for JARs. {mod_version} will be replaced by the mod version, {mc_version} will be replaced
# by the Minecraft version, and {loader} will be replaced by the loader. Don't forget the .jar file extension!
# NOTE: {loader} and {mc_version} MUST be in the filename!
JAR_NAME_FORMAT: str = "immersivemc-{mod_version}-{mc_version}-{loader}.jar"

# Version format for names. Same as JAR_NAME_FORMAT, however the loader is made all-uppercase.
VERSION_NAME_FORMAT: str = "{mod_version} [{loader} {mc_version}]"

# Retrieved tokens from environment variables for publishing to CurseForge and Modrinth.
CURSEFORGE_TOKEN: str = getenv("CURSEFORGE_TOKEN", None) if PUBLISH_CURSEFORGE else None
MODRINTH_TOKEN: str = getenv("MODRINTH_TOKEN", None) if PUBLISH_MODRINTH else None

"""=-=-=-= Advanced Configuration =-=-=-="""

# Path to git executable. If set to None, will default to default git executable
GIT_PATH = None

"""=-=-=-= No More Configuration! =-=-=-="""

# Expand PROJECT_PATH variables
PROJECT_PATH = path.expanduser(path.expandvars(PROJECT_PATH))

# Expand CHANGELOG_PATH variables
CHANGELOG_PATH = path.expanduser(path.expandvars(CHANGELOG_PATH))

# Create temp directory for work
BUILDS_DIR = tempfile.mkdtemp()

# Set GIT_PATH if not already
GIT_PATH = GIT_PATH if GIT_PATH is not None else "git"

# Read changelog data
with open(CHANGELOG_PATH, "r") as f:
    CHANGELOG_TEXT: str = f.read()

# User Agent
USER_AGENT = "hammy275/mcmod-buildandupload (hammy275@gmail.com)"

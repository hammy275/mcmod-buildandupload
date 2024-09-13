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
# minecraft_versions is a list of all Minecraft versions to build for that loader, or None to build for all loaders.
# (required, optional, incompatible, or embedded)
LOADERS: List[Loader] = [
    Loader(folder_name="fabric", loader_tags=["fabric", "quilt"],
           dependencies=[Dependency(modrinth_project_id="P7dR8mSH", dependency_type="required",
                                    curseforge_project_slug="fabric-api")], minecraft_versions=None),
    Loader(folder_name="forge", loader_tags=["forge"],
           dependencies=[], minecraft_versions=None),
    Loader(folder_name="neoforge", loader_tags=["neoforge"],
           dependencies=[], minecraft_versions=["1.20.2", "1.20.4", "1.20.6", "1.21.1"]),                                
]
# Version number for this mod release
VERSION: str = "3.0.10"
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
# Whether the version should be featured on Modrinth. If no featured versions are set, Modrinth determines
# the featured versions automatically.
FEATURED_VERSION = False

# All versions to build your mod for.
# branch_name is the name of the Git branch, minecraft_version is the Minecraft version this
# should be published under, and java_home is a path to the JAVA_HOME to use when building this version, or None
# to leave determining the JDK path up to gradle.
BUILD_VERSIONS: List[Version] = [
    Version(branch_name="1.18.x-multiloader", minecraft_version="1.18.2", java_home=None),
    Version(branch_name="1.19.x", minecraft_version="1.19.2", java_home=None),
    Version(branch_name="1.19.3", minecraft_version="1.19.3", java_home=None),
    Version(branch_name="1.19.4", minecraft_version="1.19.4", java_home=None),
    Version(branch_name="1.20.x", minecraft_version="1.20.1", java_home=None),
    Version(branch_name="1.20.2", minecraft_version="1.20.2", java_home=None),
    Version(branch_name="1.20.4", minecraft_version="1.20.4", java_home=None),
    Version(branch_name="1.20.6", minecraft_version="1.20.6", java_home="C:\Program Files\Eclipse Adoptium\jdk-21.0.4.7-hotspot"),
    Version(branch_name="1.21.1", minecraft_version="1.21.1", java_home="C:\Program Files\Eclipse Adoptium\jdk-21.0.4.7-hotspot"),
]

# Project ID for Modrinth uploads
MODRINTH_PROJECT_ID: str = "B3INNxum"
# Project ID for CurseForge uploads as a string
CURSEFORGE_PROJECT_ID: str = "591092"

# Name format for JARs. {mod_version} will be replaced by the mod version, {mc_version} will be replaced
# by the Minecraft version, and {loader} will be replaced by the loader. Don't forget the .jar file extension!
# NOTE: {loader} and {mc_version} MUST be in the filename!
JAR_NAME_FORMAT: str = "vrapi-{mod_version}-{mc_version}-{loader}.jar"

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

# Expand java_home variables in BUILD_VERSIONS that aren't None
for version in BUILD_VERSIONS:
    version.java_home = path.expanduser(path.expandvars(version.java_home)) if version.java_home is not None else None

# Create temp directory for work
BUILDS_DIR = tempfile.mkdtemp()

# Set GIT_PATH if not already
GIT_PATH = GIT_PATH if GIT_PATH is not None else "git"

# Read changelog data
with open(CHANGELOG_PATH, "r") as f:
    CHANGELOG_TEXT: str = f.read()

# User Agent
USER_AGENT = "hammy275/mcmod-buildandupload (hammy275@gmail.com)"

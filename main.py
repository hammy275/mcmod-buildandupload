import atexit
import json
import os
from typing import Union

import requests
import shutil
import sys

from subprocess import run, CalledProcessError

import config
from LoaderClass import Loader
from VersionClass import Version


def log(msg):
    print("[MCMOD-BUILDANDUPLOAD] " + str(msg))


def get_file_to_upload(version: Version, loader: Loader) -> Union[str, None]:
    """Get File to Upload.

    Returns:
        A string of the filename or None if one couldn't be found
    """
    log("Uploading for loader {} and Minecraft version {}".format(loader.folder_name,
                                                                  version.minecraft_version))
    # Get file to upload
    files = os.listdir()
    fil = None
    for f in files:
        if loader.folder_name in f and version.minecraft_version in f:
            fil = f
            break
    if fil is None:
        log("Could not find mod file for loader {} and Minecraft version {}!".format(loader.folder_name,
                                                                                     version.minecraft_version))
    return fil


def upload_curseforge() -> bool:
    """Upload Mod JARs to CurseForge.

    Returns:
        Whether the uploading succeeded.
    """
    log("Retrieving game versions from CurseForge API")
    r = requests.get("https://minecraft.curseforge.com/api/game/version-types?token={}".format(config.CURSEFORGE_TOKEN),
                     headers={"User-Agent": config.USER_AGENT})
    major_versions = r.json()
    r = requests.get("https://minecraft.curseforge.com/api/game/versions?token={}".format(config.CURSEFORGE_TOKEN),
                     headers={"User-Agent": config.USER_AGENT})
    all_versions = r.json()

    os.chdir(config.BUILDS_DIR)
    for version in config.BUILD_VERSIONS:
        for loader in config.LOADERS:
            # Skip if we don't build for this loader
            if loader.minecraft_versions is not None and version.minecraft_version not in loader.minecraft_versions:
                continue
            # Get version ID from Minecraft version
            major_minor_patch = version.minecraft_version.split(".")
            version_name = "Minecraft " + ".".join([major_minor_patch[0], major_minor_patch[1]])
            major_version_id = None
            for m in major_versions:
                if "name" in m and m["name"] == version_name:
                    major_version_id = m["id"]
                    break
            if major_version_id is None:
                log("Could not get major version ID for Minecraft major version {}".format(version_name))
                return False

            version_id = None
            modloader_ids = []
            for v in all_versions:
                if v["name"] == version.minecraft_version and v["gameVersionTypeID"] == major_version_id:
                    version_id = v["id"]
                for loader_name in loader.loader_tags:
                    if v["slug"] == loader_name:
                        modloader_ids.append(v["id"])
                        break

                if version_id is not None and len(modloader_ids) == len(loader.loader_tags):
                    break
            if version_id is None:
                log("Could not get version ID for Minecraft version ID {}".format(str(version_id)))
                return False

            if len(modloader_ids) < len(loader.loader_tags):
                log("Could not get version ID for all supported modloaders!")
                return False

            fil = get_file_to_upload(version, loader)

            with open(fil, "rb") as file_data:
                log("Uploading {} to CurseForge".format(fil))
                payload = {
                    "changelog": config.CHANGELOG_TEXT,
                    "changelogType": "markdown",
                    "displayName": config.VERSION_NAME_FORMAT.format(mod_version=config.VERSION,
                                                                     loader=loader.folder_name.upper(),
                                                                     mc_version=version.minecraft_version),
                    "gameVersions": [version_id] + modloader_ids,
                    "releaseType": config.VERSION_TYPE,
                    "relations": {
                        "projects": [d.to_curseforge_dict() for d in loader.dependencies]
                    }
                }

                r = requests.post("https://minecraft.curseforge.com/api/projects/{}/upload-file"
                                  .format(config.CURSEFORGE_PROJECT_ID),
                                  files={
                                      "metadata": (None, json.dumps(payload)),
                                      "file": (fil, file_data)
                                  },
                                  headers={
                                      "User-Agent": config.USER_AGENT,
                                      "X-Api-Token": config.CURSEFORGE_TOKEN,
                                  })
                if not r.ok:
                    log("Failed to upload file to CurseForge! Logging response from server and returning...")
                    log(r.text)
                    return False

    return True


def upload_modrinth() -> bool:
    """Uploads Mod JARs to Modrinth

    Returns:
        Whether the uploading succeeded.
    """
    os.chdir(config.BUILDS_DIR)
    for version in config.BUILD_VERSIONS:
        for loader in config.LOADERS:
            # Skip if we don't build for this loader
            if loader.minecraft_versions is not None and version.minecraft_version not in loader.minecraft_versions:
                continue

            fil = get_file_to_upload(version, loader)

            with open(fil, "rb") as file_data:

                log("Uploading {} to Modrinth".format(fil))
                payload = {
                    "name": config.VERSION_NAME_FORMAT.format(mod_version=config.VERSION,
                                                              loader=loader.folder_name.upper(),
                                                              mc_version=version.minecraft_version),
                    "version_number": config.VERSION,
                    "changelog": config.CHANGELOG_TEXT,
                    "dependencies": [d.to_modrinth_dict() for d in loader.dependencies],
                    "game_versions": [version.minecraft_version],
                    "version_type": config.VERSION_TYPE,
                    "loaders": loader.loader_tags,
                    "featured": config.FEATURED_VERSION,
                    "status": "listed",
                    "requested_status": "listed",
                    "project_id": config.MODRINTH_PROJECT_ID,
                    "file_parts": [fil],
                    "primary_file": fil
                }

                r = requests.post("https://api.modrinth.com/v2/version",
                                  files={"data": (None, json.dumps(payload)), fil: (fil, file_data)},
                                  headers={
                                      "User-Agent": config.USER_AGENT,
                                      "Authorization": config.MODRINTH_TOKEN,
                                  })
                if not r.ok:
                    log("Failed to upload file to Modrinth! Logging response from server and returning...")
                    log(r.text)
                    return False
    return True


def do_builds() -> bool:
    """Builds Mod JARs.

    Builds JAR files

    Returns:
        bool: Whether the build process was successful
    """
    gradle_exec = "gradlew.bat" if sys.platform == "win32" else "./gradlew"

    for build_config in config.BUILD_VERSIONS:
        try:
            log("Building for " + str(build_config))

            # Move directory and checkout branch
            os.chdir(config.PROJECT_PATH)
            run([config.GIT_PATH, "checkout", build_config.branch_name], check=True)

            # Wipe old builds.
            for loader in config.LOADERS:
                # Skip if we don't build for this loader
                if loader.minecraft_versions is not None and build_config.minecraft_version not in loader.minecraft_versions:
                    continue
                
                try:
                    shutil.rmtree(os.path.join(config.PROJECT_PATH, loader.folder_name, "build", "libs"))
                except FileNotFoundError:
                    pass

            # Build JARs
            run([gradle_exec, "build"], check=True)

            # Move built JARs to temporary working directory
            for loader in config.LOADERS:
                # Skip if we don't build for this loader
                if loader.minecraft_versions is not None and build_config.minecraft_version not in loader.minecraft_versions:
                    continue
                os.chdir(os.path.join(config.PROJECT_PATH, loader.folder_name, "build", "libs"))
                files = [fil for fil in os.listdir() if "dev-shadow" not in fil and "sources" not in fil]
                if len(files) == 0:
                    log("Could not find build JAR! Here are all of the files in the build/libs directory:")
                    for f in os.listdir():
                        log(f)
                    return False
                build_jar = files[0]
                jar_name = config.JAR_NAME_FORMAT.format(mod_version=config.VERSION,
                                                         mc_version=build_config.minecraft_version,
                                                         loader=loader.folder_name)
                shutil.move(build_jar, os.path.join(config.BUILDS_DIR, jar_name))

        except CalledProcessError:
            log("Process exited with non-zero exit code!")
            return False  # Build failed, bail!

    return True


def validate_config() -> str:
    """Validate Config Inputs.

    Some light validation on the inputs in the config and from environment variables.

    Returns:
        str: An empty string if the config is valid. A non-empty string containing an error message otherwise.
    """
    if config.PUBLISH_MODRINTH and config.MODRINTH_TOKEN is None:
        return "Token for publishing to Modrinth is not defined, even though publishing to Modrinth is enabled!"

    if config.PUBLISH_CURSEFORGE and config.CURSEFORGE_TOKEN is None:
        return "Token for publishing to CurseForge is not defined, even though publishing to CurseForge is enabled!"

    if config.VERSION_TYPE not in ["release", "beta", "alpha"]:
        return "VERSION_TYPE must be 'release', 'beta', or 'alpha'!"

    return ""


def cleanup_and_exit(exit_code=0):
    atexit.register(shutil.rmtree, config.BUILDS_DIR)
    sys.exit(exit_code)


def main():
    # Config validation
    log("Validating config...")
    config_err = validate_config()
    if config_err != "":
        log(config_err)
        cleanup_and_exit(1)

    log("Config validated! Building JARs...")
    log("Builds will be temporarily saved to " + config.BUILDS_DIR)
    # Do builds
    if not do_builds():
        log("Failed to build mod JARs! Please see the output log!")
        cleanup_and_exit(1)

    log("Building done!")
    if config.PUBLISH_MODRINTH or config.PUBLISH_CURSEFORGE:
        log("Now beginning build uploading...")

    # Do uploads
    if config.PUBLISH_MODRINTH:
        log("Uploading to Modrinth")
        if not upload_modrinth():
            log("Failed to upload all files to Modrinth!")
            cleanup_and_exit(1)

    if config.PUBLISH_CURSEFORGE:
        log("Uploading to CurseForge")
        if not upload_curseforge():
            log("Failed to upload all files to CurseForge!")
            cleanup_and_exit(1)

    log("All tasks complete! Builds are located at the following file path: " + config.BUILDS_DIR)
    input("Press ENTER to delete builds locally and exit...")
    cleanup_and_exit(0)


if __name__ == "__main__":
    main()

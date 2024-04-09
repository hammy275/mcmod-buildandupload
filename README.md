# MC Mod Build and Upload

A small utility to handle uploading mods to CurseForge and Modrinth for several Minecraft versions across several modloaders. This is intended for use with Architectury Templates with the default build locations (`MODLOADER/build/libs`).

## Usage Instructions

1. Create a file named `changelog.md`, and add changelog data to it.
2. Edit `config.py` with the information asked for. It contains by default, a mostly-complete version of ImmersiveMC's or MC VR API's configuration as an example, with more details below.
3. Set CURSEFORGE_TOKEN and/or MODRINTH_TOKEN as environment variables to their API tokens.
4. Run `main.py`. Note that the temporary directory where your builds are put is printed to the console, in case you want to keep them or upload to other platforms. Note that this will be deleted after pressing the `ENTER` key once everything is done, so be sure to copy these somewhere safe if you want to keep them.

## Configuration

`config.py` is where all your configuration should go. Below is everything you should fill out with detailed explanations. You can also simply look at `config.py` directly, if you want to read examples, which also contain comments to explain everything.

- `LOADERS`: This holds a list of all loaders you're building for, for what Minecraft versions, and what dependencies are needed. An example item in the list could look something like: `Loader(folder_name="fabric", loader_tags=["fabric", "quilt"], dependencies=[Dependency(modrinth_project_id="P7dR8mSH", dependency_type="required" curseforge_project_slug="fabric-api")], minecraft_versions=["1.19.2", "1.20.1"])`. Let's break down each part of this:
  - `folder_name`: This is the name of the folder within your project where your `build` folder is located at build-time. For example, on Fabric, this would be named `fabric`, as builds are stored in `fabric/build/libs`.
  - `loader_tags`: This is the name of every modloader these builds are supported on. For example, you can use `["fabric", "quilt"]` to specify that this build works on both Fabric and Quilt.
  - `dependencies`: This is a list of all dependencies for your mod on the modloaders specified in `loader_tags`. Each dependency contains the following data:
    - `modrinth_project_id`: The Modrinth Project ID of the dependency. This can be found on the mod's project page under "Technical information" as "Project ID".
    - `curseforge_project_slug`: The slug of the dependency on CurseForge. This is the end of the URL on the project's homepage on CurseForge.
    - `dependency_type`: This can be any of the following: `"required"`, `"optional"`, or `"embedded"`. This means that the dependency is required to run the game with your mod, optional when running the game with your mod, or included with your mod respectively.
  - `minecraft_versions`: A list of Minecraft version strings your mod supports. This can be left as `None` if you want to support every Minecraft version specified in `BUILD_VERSIONS` below.

That was a lot, but don't worry! This is the most complicated part of the configuration! The rest is much easier.

- `VERSION`: The version number for your mod release.
- `VERSION_TYPE`: The version type for your mod release. This can either be `"release"`, `"beta"`, or `"alpha"`.
- `PUBLISH_CURSEFORGE`: Whether you want to publish to CurseForge.
- `PUBLISH_MODRINTH`: Whether you want to publish to Modrinth.
- `PROJECT_PATH`: The path to your project. An example of this would be something like `"C:\\Users\\my_user\\MyMod"` on Windows. Note that two `\`'s are used instead of one so that one `\` escapes the other.
- `CHANGELOG_PATH`: The path to your changelog file. Assuming you follow the Usage Instructions above, you can leave this as `changelog.md`.
- `FEATURED_VERSION`: Modrinth has a feature where it allows you to determine what versions are featured on the side. If no versions are set to be featured, Modrinth will automatically determine which versions to feature for you. I recommend leaving this disabled to let Modrinth pick for you unless you want verisons to be featured via a method other than what Modrinth uses.
- `BUILD_VERSIONS`: This is the list of all Git branch names to the Minecraft versions they correspond to. For example, `[Version(branch_name="main" minecraft_version="1.19.2"), Version(branch_name="1.18.2" minecraft_version="1.18.2")]` means the Git branch `main` should be used to build the mod for Minecraft version `1.19.2` and the Git branch `1.18.2` should be used to build the mod for Minecraft version `1.18.2`.
- `MODRINTH_PROJECT_ID`: The project ID for your mod on Modrinth to publish to. This can be found on your mod's project page under "Technical information" as "Project ID".
- `CURSEFORGE_PROJECT_ID`: The project ID for your mod on CurseForge to publish to. This can be found on your mod's project page in the "About Project" area as "Project ID".
- `JAR_NAME_FORMAT`: The name your uploaded mod files should use. The string MUST contain `{mc_version}` and `{loader}`, which will be replaced by the Minecraft version and the mod loader respectively. The string may also contain `{mod_version}`, which will be replaced by the `VERSION` of your mod specified above. An example of this would be `"mymod-{mod_version}-{mc_version}-{loader}.jar"`, which would become, for example, `mymod-1.0.0-1.19.2-fabric.jar`.
- `VERSION_NAME_FORMAT`: The name of the version as shown on CurseForge and Modrinth. This follows the same format as `JAR_NAME_FORMAT` above, however does not have any requirements and the `{loader}` will be made all-uppercase. An example of this would be `"{mod_version} [{loader} {mc_version}]"`, which would become, for example, `1.0.0 [FABRIC 1.19.2]`.

That was a lot, but now you're mostly done! Just make sure to follow steps 3 and 4 in the "Usage Instructions" above, and you'll be good to go! There are a few extra things you can configure, which I'll explain for completeness:

- `CURSEFORGE_TOKEN` and `MODRINTH_TOKEN`: These are your API tokens for uploading to CurseForge and Modrinth respectively. It is *highly* recommend to NOT change these, and instead set environment variables on your operating system with them, as specified in step 3. This way, you can't accidentally commit your token changes to Git.
- `GIT_PATH`: Allows you to specify the exact path to your Git executable. Otherwise, your system's `git` will be used.

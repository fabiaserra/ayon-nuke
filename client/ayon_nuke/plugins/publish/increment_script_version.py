import nuke
import pyblish.api


class IncrementScriptVersion(pyblish.api.ContextPlugin):
    """Increment current script version."""

    order = pyblish.api.IntegratorOrder + 0.9
    label = "Increment Script Version"
    optional = True
    ### Starts Alkemy-X Override ###
    # Add other families as well so script version gets incremented also
    # when doing a publish of those
    families = [
        # "workfile", # commenting it out for now as we don't want to bump it if publishing prerender + workfile
        "render",
        "render.farm",
        "render.frames_farm",
    ]
    ### Ends Alkemy-X Override ###
    hosts = ["nuke"]

    settings_category = "nuke"

    def process(self, context):
        if not context.data.get("increment_script_version", True):
            return

        assert all(result["success"] for result in context.data["results"]), (
            "Publishing not successful so version is not increased.")

        from ayon_core.lib import version_up, get_version_from_path
        path = context.data["currentFile"]
        script_version = int(get_version_from_path(path))

        # Find the lowest version being published
        publish_version = script_version
        for instance in context:
            publish_version = min(
                publish_version, instance.data.get("version")
            )

        # If the highest version is lower than the script version
        # it means we are publishing old versions that don't match the
        # script and thus we shouldn't be incrementing the script version
        if publish_version < script_version:
            self.log.info(
                "Skipping incrementing script version as we are publishing old versions"
            )
            return

        nuke.scriptSaveAs(version_up(path))
        self.log.info('Incrementing script version')

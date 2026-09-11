ALLOWED_ACTIONS = {
    "open_app",
    "close_app",
    "volume_up",
    "volume_down",
    "mute"
}


def validate_action(action):

    if not isinstance(action, dict):
        return False

    action_type = action.get("type")

    if action_type not in ALLOWED_ACTIONS:
        return False

    if action_type in {
        "open_app",
        "close_app"
    }:

        apps = action.get("apps")

        if not isinstance(apps, list):
            return False

        if not apps:
            return False

        if not all(
            isinstance(app, str) and app.strip()
            for app in apps
        ):
            return False

    return True
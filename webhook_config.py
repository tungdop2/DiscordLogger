from json import load

supported_webhooks = ["discord"]


def check_discord_webhook_config(config: dict) -> bool:
    if "webhook_type" not in config or config["webhook_type"] != "discord":
        return
    if "webhook_url" not in config:
        raise ValueError("Discord webhook config is missing 'webhook_url' value.")
    return True


class WebhookConfig:
    def __init__(
            self, 
            config_path: str,
            webhook_url: str = None,
            webhook_type: str = "discord",
            message_prefix: str = None,
            log_level: str = "info",
        ):
        if config_path:
            self.values = self.load_config_from_file(config_path)
        else:
            self.values = {
                "webhook_url": webhook_url,
                "webhook_type": webhook_type,
                "message_prefix": message_prefix,
                "log_level": log_level,
            }
        if (
            "webhook_type" not in self.values
            or self.values["webhook_type"] not in supported_webhooks
        ):
            raise ValueError(
                f"Invalid webhook type specified in config. Supported values: {supported_webhooks}"
            )
        check_discord_webhook_config(self.values)

    def load_config_from_file(self, config_path: str = None):
        with open(config_path, "r") as f:
            return load(f)

    def get_config(self):
        return self.values

    def __getattr__(self, name):
        return self.values.get(name, None)

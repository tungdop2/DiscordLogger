from .webhook_config import WebhookConfig
import requests
import logging
from io import BytesIO

log_levels = {"critical": 0, "error": 1, "warning": 2, "info": 3, "debug": 4}

logger = logging.getLogger("WebhookLogger")
logger.setLevel("INFO")


class WebhookLogger:
    def __init__(
        self,
        config_path: str = None,
        webhook_url: str = None,
        webhook_type: str = "discord",
        message_prefix: str = None,
        log_level: str = None,
    ):
        self.config = WebhookConfig(
            config_path=config_path,
            webhook_url=webhook_url,
            webhook_type=webhook_type,
            message_prefix=message_prefix,
            log_level=log_level,
        )
            
        self.webhook_url = self.config.webhook_url
        self.message_prefix = (
            f"`({self.config.message_prefix})` "
            if self.config.message_prefix is not None
            else "A message from Logger: "
        )
        self.log_level = log_levels.get(
            self.config.log_level or "info", log_levels["info"]
        )
        self.stored_response = None

    def _check_level(self, level: str) -> bool:
        return log_levels.get(level, "info") <= self.log_level

    def _send_request(
        self, message: str, images: list = None, store_response: bool = False
    ):
        # Prepare the request data
        data = {"content": f"{self.message_prefix}{message}"}
        files = {}

        if images:
            # Convert PIL images to BytesIO and add to files dictionary
            for index, img in enumerate(images):
                img_byte_array = BytesIO()
                img.save(img_byte_array, format="PNG")
                img_byte_array.seek(0)
                files[f"file{index}"] = (
                    f"image{index}.png",
                    img_byte_array,
                    "image/png",
                )

        # Send request to webhook URL with images if present
        try:
            post_result = requests.post(self.webhook_url, data=data, files=files)
        except Exception as e:
            logger.error("Could not send webhook request: %s", e)
            return
        if store_response:
            self.stored_response = post_result.headers

    def send(
        self,
        message: str,
        images: list = None,
        message_level: str = "info",
        store_response: bool = False,
    ):
        if not self._check_level(message_level):
            return
        if images is not None and not isinstance(images, list):
            images = [images]
            
        # Send webhook message
        if images and len(images) <= 10:
            self._send_request(message, images, store_response=store_response)
        elif images and len(images) > 10:
            for i in range(0, len(images), 9):
                self._send_request(
                    message, images[i : i + 9], store_response=store_response
                )
        else:
            self._send_request(message, store_response=store_response)
            
    def log(self, message: str, message_level: str = "info"):
        self.send(message, message_level=message_level)


if __name__ == "__main__":
    # Example usage of the WebhookHandler class
    handler = WebhookLogger(
        config_path="./webhook.json"
    )
    
    # Send a test message
    handler.send("Initial test message", message_level="info")

# Discord Logger
Discord logger is a simple script that helps you log messages or Pillow images to a discord channel.

## Usage
0. Make sure you have python installed, and a discord webhook created.
1. Clone the repository
2. Install `requests` using `pip install -U requests`
3. Edit the `webhook.json` file with your webhook url and other settings, or override the settings in the constructor. After that, you can use the logger as shown below.
```
from webhook_logger import WebhookLogger

logger = WebhookLogger(
        webhook_url: str = None,
        webhook_type: str = None,
        message_prefix: str = None,
        log_level: str = None
    )

logger.log("Hello, World!")
logger.log("This is a image!", images=<Pillow image>)
logger.log("This is a list of images!", images=[<Pillow image>, <Pillow image>])
```

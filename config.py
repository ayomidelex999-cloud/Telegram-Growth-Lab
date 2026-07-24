import os


class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")

    def validate(self):
        if not self.BOT_TOKEN:
            raise RuntimeError(
                "BOT_TOKEN environment variable is not set. "
                "Set it in Railway's Variables tab (get the token from @BotFather), "
                "or in a local .env file for development."
            )


config = Config()

import os
from datetime import datetime


class ScreenshotUtil:
    @staticmethod
    def take_screenshot(page, name):
        os.makedirs("screenshots", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"

        page.screenshot(path=path, full_page=True)

        return path
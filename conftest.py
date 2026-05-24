import shutil

import pytest
from dash.testing.composite import DashComposite
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DashCompositeWithManagedDriver(DashComposite):
    def _get_chrome(self):
        options = self._get_wd_options()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True,
            },
        )
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=0")
        options.set_capability("goog:loggingPrefs", {"browser": "SEVERE"})

        driver_path = shutil.which("chromedriver") or ChromeDriverManager().install()
        return webdriver.Chrome(service=Service(driver_path), options=options)


@pytest.fixture
def dash_duo(request, dash_thread_server, tmpdir):
    with DashCompositeWithManagedDriver(
        server=dash_thread_server,
        browser=request.config.getoption("webdriver"),
        remote=request.config.getoption("remote"),
        remote_url=request.config.getoption("remote_url"),
        headless=request.config.getoption("headless"),
        options=request.config.hook.pytest_setup_options(),
        download_path=tmpdir.mkdir("download").strpath,
        percy_assets_root=request.config.getoption("percy_assets"),
        percy_finalize=request.config.getoption("nopercyfinalize"),
        pause=request.config.getoption("pause"),
    ) as dc:
        yield dc

"""PyTest Configuration."""
from datetime import datetime
import logging
import os
from pathlib import Path
import re
from typing import Callable
import pytest

LOG = logging.getLogger(__name__)


class LogManager:
    """Manage per-test case logging.

    The root log directory is:
    1. The `ESMETEST_LOG` environment variable value.
    2. The `/var/log/esmetest` volume, if it exists.
    3. The `log` sub-directory of the project.

    Each test run will create a new timestamped sub-directory, under
    the root log directory.
    """
    
    FORMAT = r'%(asctime)s|%(name)s|%(levelname)s - %(message)s'
    UNIX_LOG = Path('/var/log/apitest')

    def __init__(self):
        """Instante an object."""
        if 'UNIX_LOG' in os.environ:
            self.root_dir = Path(os.environ['UNIX_LOG'])
        elif self.UNIX_LOG.is_dir():
            self.root_dir = self.UNIX_LOG
        else:
            self.root_dir = Path(
                __file__).parent.parent.joinpath('log')

        self.run_stamp = datetime.now().strftime(r'%Y-%m-%d.%H-%M-%S')
        self.run_dir = Path(self.root_dir, self.run_stamp)
        if not self.run_dir.exists():
            self.run_dir.mkdir(parents=True)

        self.formatter = logging.Formatter(self.FORMAT)

        self.log_dir: Path = None
        self.handler: logging.FileHandler = None

    def purge_logs(self):
        """Clear prior test run log directories.

        Returns:
            bool: True value for psuedo-assertion
        """
        def _rmpath(path: Path):
            for child in path.iterdir():
                if child.is_dir():
                    _rmpath(child)
                else:
                    child.unlink()
            path.rmdir()
        LOG.info('Purging prior test run logs...')
        for child in self.root_dir.iterdir():
            if child.is_dir() and child.name != self.run_stamp:
                _rmpath(child)
        return True

    def configure_test(self, request):
        """Switch to a test-specific log directory and file.

        This is applied as a per-test "autouse" fixture.

        Arguments:
            request (FixtureRequest): Fixture function or method
        """
        # Generate the new log directory.
        folders = str(request.node.nodeid).split('::')
        folders[0] = re.sub(
            r'\.py', '', re.sub(
                r'^tests[/\\]', '', folders[0]))
        self.log_dir = self.run_dir
        for folder in folders:
            self.log_dir /= folder
            self.log_dir.mkdir(exist_ok=True)

        # Remove and close the prior handler.
        root_logger = logging.getLogger()
        if self.handler:
            root_logger.removeHandler(self.handler)
            self.handler.flush()
            self.handler.close()

        # Add a new handler.
        self.handler = logging.FileHandler(
            self.log_dir / f'{request.node.name}.log')
        self.handler.setLevel(logging.DEBUG)
        self.handler.setFormatter(self.formatter)
        root_logger.addHandler(self.handler)
        LOG.info('Start: %s', request.node.nodeid)

    def log_to_file(self, name: str, content: bytes):
        """Write content to the named log file. If the file already
        exists, the new file name will include an appended index number.

        Arguments:
            name (str): Name of the log directory file
            content (bytes): Content of the log directory file

        Returns:
            Path: Path of log directory file
        """
        log_file = Path(self.log_dir, name)
        idx, stem = 0, log_file.stem
        while log_file.exists():
            idx = idx + 1
            log_file = Path(
                self.log_dir,
                f'{stem}-{idx:03d}' + log_file.suffix)
        log_file.write_bytes(content)
        return log_file


_LOG_MANAGER = LogManager()


###########################
# Framework Modifications
###########################


def pytest_addoption(parser):
    """Add custom options to the test runner."""
    parser.addoption(
        '-F', '--flush-logs', action='store_true',
        help='Delete logs from prior runs')


def pytest_configure(config):
    """Configure testing resources."""
    # Define the main log file logging.
    log_file = _LOG_MANAGER.run_dir.joinpath('main.log')
    config.option.log_file = log_file
    config.option.log_file_date_format = r'%Y-%m-%d %H:%M:%S'
    config.option.log_file_format = _LOG_MANAGER.FORMAT
    config.option.log_file_level = 'DEBUG'

    # The Docker SDK uses the urllib3 package, which does a lot of
    # DEBUG-level logging. Reduce that package's logging verbosity.
    logging.getLogger('urllib3').setLevel(logging.WARN)

    # If requested, flush test logs.
    if config.getoption('flush_logs'):
        _LOG_MANAGER.purge_logs()


###########################
# Test Fixtures
###########################


@pytest.fixture(autouse=True)
def _set_logging(caplog, request):
    # Configure detailed logging for each test case.
    caplog.set_level(logging.DEBUG)
    _LOG_MANAGER.configure_test(request)


@pytest.fixture
def log2file() -> Callable[[str, bytes], None]:
    """Get the test log file writer.

    Returns:
        Callable: Log file writer
    """
    return _LOG_MANAGER.log_to_file

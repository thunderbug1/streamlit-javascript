from typing import Final, List
import os
import json
import subprocess
import setuptools
from io import TextIOWrapper
from subprocess import CompletedProcess
from setuptools.command.build_py import build_py

PACKAGE_MGR = "npm"
PACKAGE_DIR = os.path.dirname(__file__)
PACKAGE_NAME = "streamlit-javascript"
STREAMLIT_VERSION = "1.42.0"  # PEP-440


class build_sdist(build_py):
    def run(self):
        build_py.run(self)
        self.run_command("Build-Frontend")


class BuildErrorException(Exception):
    msg: Final[str]

    def __init__(self, msg):
        self.msg = msg


class BuildFrontend(setuptools.Command):
    description: str = "Build ReAct interface"
    user_options: List = []
    frontend_dir: str
    modules_dir: str
    build_dir: str
    log_file: TextIOWrapper

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        self.frontend_dir = os.path.join(
            PACKAGE_DIR, "streamlit_javascript", "frontend"
        )
        self.modules_dir = os.path.join(self.frontend_dir, "node_modules")
        self.build_dir = os.path.join(self.frontend_dir, "build")

    def msg_log(self, msg: str, /, indent: int = 0) -> None:
        assert self.log_file.writable()
        for line in msg.splitlines():
            if len(line.strip()) > 0:
                self.log_file.write(" " * indent + line + os.linesep)
        self.log_file.flush()

    def msg_run(self, result, /, indent: int):
        self.msg_log(f"RC:{result.returncode}", indent=indent)
        self.msg_log("STDOUT:", indent=indent)
        self.msg_log(result.stdout, indent=indent + 2)
        self.msg_log("STDERR:", indent=indent)
        self.msg_log(result.stderr, indent=indent + 2)
        return result

    def check_package_json(self):
        self.msg_log("Checking package.json version...")
        with open(
            os.path.join(self.frontend_dir, "package.json"),
            mode="r",
            encoding="utf-8",
        ) as pkg_json:
            try:
                pkg_desc = json.load(pkg_json)
                if "version" not in pkg_desc:
                    self.msg_log(
                        f"WARNING\xe2\x9a\xa0: package.json:version is missing, should be {STREAMLIT_VERSION}"
                    )
                elif pkg_desc["version"] != STREAMLIT_VERSION:
                    self.msg_log(
                        f"WARNING\xe2\x9a\xa0: package.json:version should be {STREAMLIT_VERSION} not {pkg_desc["version"]}"
                    )
            except json.decoder.JSONDecodeError as exc:
                self.msg_log("Unable to read package.JSON file - syntax error")
                raise json.decoder.JSONDecodeError(
                    "package.json: " + exc.msg,
                    os.path.join(self.frontend_dir, "package.json"),
                    exc.pos,
                ) from None

    def check_need_protobuff(self):
        # TODO: streamlit-javascript does not use protobuf, but we should have a test
        self.msg_log(f"{PACKAGE_NAME} does not use protobuf...")

    def show_msg_if_build_dir_exists(self):
        self.msg_log("Checking if Fontend has already been built...")
        if os.path.isdir(self.build_dir):
            self.msg_log("Found build directory", indent=2)

    def show_msg_if_modules_dir_exists(self):
        self.msg_log("Checking if node_modules exists...")
        if os.path.isdir(self.modules_dir):
            self.msg_log("Found build directory", indent=2)

    def check_node_installed(self) -> CompletedProcess:
        self.msg_log("Checking node is installed...")
        result: CompletedProcess = self.msg_run(
            subprocess.run(
                ["node", "--version"],
                executable="node",
                cwd=PACKAGE_DIR,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ),
            indent=2,
        )
        if result.returncode != 0:
            raise BuildErrorException(
                "Could not find node - it is required for ReAct components"
            )
        return result

    def check_pkgmgr_installed(self) -> CompletedProcess:
        self.msg_log(f"Checking {PACKAGE_MGR} is installed...")
        result = self.msg_run(
            subprocess.run(
                [PACKAGE_MGR, "--version"],
                executable=PACKAGE_MGR,
                cwd=PACKAGE_DIR,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ),
            indent=2,
        )
        if PACKAGE_MGR == "yarn":
            self.msg_log("Checking yarn corepack is installed")
            result = self.msg_run(
                subprocess.run(
                    ["corepack", "enable"],
                    executable="corepack",
                    cwd=PACKAGE_DIR,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                ),
                indent=2,
            )
            if result.returncode != 0:
                raise BuildErrorException(
                    f"Could not find corepack/{PACKAGE_MGR} - it is required to install node packages"
                )
        if result.returncode != 0:
            raise BuildErrorException(
                f"Could not find {PACKAGE_MGR} - it is required to install node packages"
            )
        return result

    def run_install(self) -> CompletedProcess:
        self.msg_log(f"Running {PACKAGE_MGR} install...")
        result = self.msg_run(
            subprocess.run(
                [PACKAGE_MGR, "install"],
                executable=PACKAGE_MGR,
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ),
            indent=2,
        )
        return result

    def run_build(self) -> CompletedProcess:
        self.msg_log(f"Running {PACKAGE_MGR} run build...")
        result = self.msg_run(
            subprocess.run(
                [PACKAGE_MGR, "run", "build"],
                executable=PACKAGE_MGR,
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ),
            indent=2,
        )
        return result

    def run_npm_audit(self) -> CompletedProcess:
        self.msg_log("Running npm audit...")
        result = self.msg_run(
            subprocess.run(
                [PACKAGE_MGR, "audit"],
                executable=PACKAGE_MGR,
                cwd=self.frontend_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ),
            indent=2,
        )
        return result

    def check_build_output_ok(self):
        self.msg_log("Checking if Fontend was built...")
        if os.path.isdir(self.build_dir):
            self.msg_log("Found build directory", indent=2)
        else:
            raise BuildErrorException("Failed to create output directory")

    def run(self) -> None:
        original_directory = os.getcwd()
        try:
            os.chdir(PACKAGE_DIR)
            self.log_file = open(
                "setup.log",
                mode="w",
                encoding="utf-8",
            )
            # PreInstallation Checks
            self.check_package_json()
            self.check_need_protobuff()
            self.show_msg_if_build_dir_exists()
            self.show_msg_if_modules_dir_exists()
            self.check_node_installed()
            self.check_pkgmgr_installed()
            # RunInstallation
            result = self.run_install()
            if result.stdout.find("npm audit fix") != -1:
                result = self.run_npm_audit()
            result = self.run_build()
            # PostInstallation Checks
            self.check_build_output_ok()
        finally:
            if not self.log_file.closed:
                self.log_file.close()
            os.chdir(original_directory)


readme_path = os.path.join(PACKAGE_DIR, "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version=STREAMLIT_VERSION,
    description="component to run javascript code in streamlit application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thunderbug1/streamlit-javascript",
    author="Alexander Balasch & Strings",
    author_email="",
    license="MIT License",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "streamlit >= " + STREAMLIT_VERSION,
    ],
    python_requires=">=3.9, !=3.9.7",  # match streamlit v1.42.0
    # PEP 561: https://mypy.readthedocs.io/en/stable/installed_packages.html
    packages=setuptools.find_packages(),
    cmdclass={
        "build_py": build_sdist,
        "Build-Frontend": BuildFrontend,
    },
    zip_safe=False,  # install source files not egg
    include_package_data=True,  # copy html and friends
)

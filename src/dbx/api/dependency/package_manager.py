from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dbx.models.workflow.common.libraries import Library
from dbx.utils import dbx_echo

class PackageManager:
    def __init__(self, package_path: Optional[str] = None):
        self._package: Optional[Library] = self.prepare_package(package_path= package_path)

    @property
    def package(self) -> Optional[Library]:
        return self._package
    
    def prepare_package(self, package_path:Optional[str]=None) -> Optional[Library]:
        package_file = self.get_package_file(package_path = package_path)

        if package_file:
            return Library(whl=f"file://{package_file}")
        else:
            dbx_echo(
                "Package file was not found. Please check the dist folder if you expect to use package-based imports"
            )
        
    @staticmethod
    def get_package_file(package_path:Optional[str] = None) -> Optional[Path]:
        dbx_echo("Locating package file")
        if package_path:
            file_locator = list((Path(package_path) / "dist").glob("*.whl"))
        else:
            file_locator = list(Path("dist").glob("*.whl"))

        sorted_locator = sorted(
            file_locator, key=os.path.getmtime
        )  # get latest modified file, aka latest package version   
        if sorted_locator:
            file_path = sorted_locator[-1]
            dbx_echo(f"Package file located in: {file_path}")
            return file_path
        else:
            dbx_echo("Package file was not found")
            return None

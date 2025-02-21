from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from poetry.core.semver.helpers import parse_constraint
from poetry.core.version.markers import parse_marker


if TYPE_CHECKING:
    from poetry.core.packages.types import DependencyTypes
    from poetry.core.semver.version_constraint import VersionConstraint

from poetry.core.packages.package import Package
from poetry.core.packages.utils.utils import create_nested_marker


class ProjectPackage(Package):
    def __init__(
        self,
        name: str,
        version: str | VersionConstraint,
        pretty_version: str | None = None,
    ) -> None:
        super().__init__(name, version, pretty_version)

        self.build_config = {}
        self.packages = []
        self.include = []
        self.exclude = []
        self.custom_urls = {}

        if self._python_versions == "*":
            self._python_constraint = parse_constraint("~2.7 || >=3.4")

    @property
    def build_script(self) -> str | None:
        return self.build_config.get("script")

    def is_root(self) -> bool:
        return True

    def to_dependency(self) -> DependencyTypes:
        dependency = super().to_dependency()

        dependency.is_root = True

        return dependency

    @property
    def python_versions(self) -> str:
        return self._python_versions

    @python_versions.setter
    def python_versions(self, value: str) -> None:
        self._python_versions = value

        if value == "*":
            value = "~2.7 || >=3.4"

        self._python_constraint = parse_constraint(value)
        self._python_marker = parse_marker(
            create_nested_marker("python_version", self._python_constraint)
        )

    @property
    def urls(self) -> dict[str, Any]:
        urls = super().urls

        urls.update(self.custom_urls)

        return urls

    def build_should_generate_setup(self) -> bool:
        return self.build_config.get("generate-setup-file", True)

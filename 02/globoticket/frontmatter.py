import os
import re
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_DIRECTORY = Path(__file__).parent.parent / "product_info"


def get_frontmatter(product_code: str) -> dict[str, Any]:
    """Read the frontmatter for event with given product_code,
    and return the properties as a dict."""
    frontmatter = find_frontmatter_file(product_code, FRONTMATTER_DIRECTORY).read_text()
    return parse_frontmatter(frontmatter)


def find_frontmatter_file_jmf(product_code: str, frontmatter_dir: Path) -> Path:  # type: ignore
    """Find a file named `product_code`.yml in frontmatter_dir and its subdirectories.
    Raises FileNotFoundError if no file is found for this product_code"""

    file_path = frontmatter_dir / f"{product_code}.yml"
    if os.path.isfile(file_path):
        return file_path
    else:
        for sub_dir in frontmatter_dir.iterdir():
            if sub_dir.is_dir():
                file_path = sub_dir / f"{product_code}.yml"
                if os.path.isfile(file_path):
                    return file_path

    if not os.path.isfile(file_path):
        raise FileNotFoundError


def find_frontmatter_file(product_code: str, frontmatter_dir: Path) -> Path:
    """Find a file named `product_code`.yml in frontmatter_dir and its subdirectories.
    Raises FileNotFoundError if no file is found for this product_code"""
    matches = list(frontmatter_dir.glob(f"**/{product_code}.yml"))
    if not matches:
        raise FileNotFoundError(
            f"Cannot find yaml file for product {product_code} in {frontmatter_dir}"
        )
    return matches[0]


class InvalidFrontmatterError(Exception):
    pass


FRONTMATTER_REGEX = re.compile(
    # Please add a regular expression
    # containing two named groups:
    # one named "yaml" containing the YAML data (first part of the file)
    # one named "content" containing the text content (second part of the file)
    r"---\n(?P<yaml>.*?)---\n(?P<content>.*)",
    re.DOTALL,
)


def parse_frontmatter(frontmatter: str) -> dict[str, Any]:
    """Return the contents of frontmatter as a dict.
    Raises an InvalidFrontmatterError if anything is wrong."""

    match = re.match(FRONTMATTER_REGEX, frontmatter)
    if not match:
        raise InvalidFrontmatterError("Invalid file structure")

    try:
        data = yaml.load(match.group("yaml"), Loader=yaml.FullLoader)
        data["content"] = match.group("content") or ""
    except (yaml.YAMLError, TypeError) as e:
        raise InvalidFrontmatterError("Invalid YAML (should be a dict)") from e

    return data

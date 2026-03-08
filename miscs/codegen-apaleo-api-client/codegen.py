#!/usr/bin/env python3
"""
A simple CLI tool to read OpenAPI JSON file and convert it into Pydantic models.
"""

import argparse
import json
import sys
from pathlib import Path


def read_json_file(file_path: str) -> dict:
    """
    Read a JSON file and return its contents as a dictionary.

    Args:
        file_path (str): Path to the JSON file

    Returns:
        dict: The contents of the JSON file

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path_obj, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print(f"Warning: JSON file contains {type(data).__name__}, not a dictionary")

        return data

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Read a JSON file and load it into a dictionary",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file data.json
  %(prog)s --file /path/to/config.json
        """,
    )

    parser.add_argument("--file", type=str, required=True, help="Path to the JSON file to read")

    parser.add_argument("--pretty", action="store_true", help="Pretty print the JSON output")

    args = parser.parse_args()

    # Read the JSON file
    data = read_json_file(args.file)

    return data


if __name__ == "__main__":
    main()

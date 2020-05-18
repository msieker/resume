#!/usr/bin/env python3
"""Processes a JSON file and turns it into a resume"""

import argparse
import json
from json import decoder
from typing import Dict, Optional

from jinja2 import Template
from jsonschema import validate, exceptions # type: ignore

SCHEMA_FILE = "resumeschema.json"

def load_template(template_name: str) -> Optional[Template]:
    """Loads a Jinja template from a file"""
    try:
        with open(template_name, "r") as template_file:
            return Template(template_file.read())
    except FileNotFoundError:
        print("Template file '{}' does not exist".format(template_name))
    return None

def generate_output(out_name: str, template: Template, data: Dict):
    """Runs the resume JSON through a Jinja template and writes the
    output to a file"""
    output_text = template.render(data)

    with open(out_name, "w") as out_file:
        out_file.write(output_text)

def load_schema() -> Dict:
    """Loads the resume JSON schema and returns the dict"""
    with open(SCHEMA_FILE, "r") as schema_file:
        return json.load(schema_file)

def load_and_validate_file(file_name: str, schema: Dict) -> Optional[Dict]:
    """Attempts to load and validate the resume JSON file specified"""
    try:
        with open(file_name, "r") as in_file:
            resume_json = json.load(in_file)
        validate(resume_json, schema)
        return resume_json
    except FileNotFoundError:
        print("Resume file '{}' does not exist".format(file_name))
    except decoder.JSONDecodeError:
        print("Resume file '{}' does not appear to be a JSON file".format(file_name))
    except exceptions.ValidationError as e:
        print("Resume file '{}' does not match the resume JSON schema\n".format(file_name), e)
    return None

def main():
    """Main entry point"""
    schema = load_schema()
    resume_json = load_and_validate_file(args.input_file, schema)
    if not resume_json:
        return
    template = load_template(args.template_file)
    if not template:
        return
    generate_output(args.output_file, template, resume_json)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a resume from a JSON file")
    parser.add_argument("--input", dest="input_file", type=str,
                        default="resume.json",
                        help="The JSON file to process. Defaults to 'resume.json")
    parser.add_argument("--template", dest="template_file", type=str,
                        default="template.html",
                        help="""The HTML file to use as an output template.
                        Defaults to 'template.html'""")
    parser.add_argument("--output", dest="output_file", type=str,
                        default="resume.html",
                        help="The output file name. Defaults to 'resume.html")
    args = parser.parse_args()
    main()

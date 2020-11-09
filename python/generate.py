#!/usr/bin/env python3
"""Processes a YAML file and turns it into a resume"""

import argparse
import os
from typing import Dict, Optional
from ruamel.yaml import YAML
from jinja2 import Template, Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

yaml = YAML(typ='safe')
latex_jinja_env = Environment(
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=FileSystemLoader(os.path.abspath('.'))
)

html_jinja_env = Environment(
    trim_blocks=True,
    loader=FileSystemLoader(os.path.abspath('.'))
)


def make_loader(template_name: str) -> Optional[Environment]:
    if template_name.endswith("html"):
        return Environment(
            trim_blocks=True,
            loader=FileSystemLoader(os.path.dirname(template_name))
        )
    elif template_name.endswith("tex"):
        return Environment(
            block_start_string=r'\BLOCK{',
            block_end_string='}',
            variable_start_string=r'\VAR{',
            variable_end_string='}',
            comment_start_string=r'\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=FileSystemLoader(os.path.dirname(template_name))
        )
    else:
        print(
            f"Unknown template type for file {os.path.basename(template_name)}")
        return None


def load_template(template_name: str) -> Optional[Template]:
    """Loads a Jinja template from a file, returning None if the file was not found"""
    try:
        jinja_env = make_loader(template_name)
        if not jinja_env:
            return None
        return jinja_env.get_template(os.path.basename(template_name))
    except TemplateNotFound:
        print(f"Template file '{template_name}' does not exist")
    return None


def generate_output(out_name: str, template: Template, data: Dict):
    """Runs the resume YAML through a Jinja template and writes the
    output to a file"""
    output_text = template.render(data)

    with open(out_name, "w") as out_file:
        out_file.write(output_text)


def load_file(file_name: str) -> Optional[Dict]:
    """Attempts to load the resume YAML file specified"""
    try:
        with open(file_name, "r") as in_file:
            resume_dict = yaml.load(in_file)
        return resume_dict
    except FileNotFoundError:
        print(f"Resume file '{file_name}' does not exist")
    return None


def main():
    """Main entry point"""
    resume_dict = load_file(args.input_file)
    if not resume_dict:
        return
    template = load_template(args.template_file)
    if not template:
        return
    print(resume_dict)
    generate_output(args.output_file, template, resume_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a resume from a YAML file")
    parser.add_argument("--input", dest="input_file", type=str,
                        default="resume.yaml",
                        help="The JSON file to process. Defaults to 'resume.yaml")
    parser.add_argument("--template", dest="template_file", type=str,
                        default="template.html",
                        help="""The HTML file to use as an output template.
                        Defaults to 'template.html'""")
    parser.add_argument("--output", dest="output_file", type=str,
                        default="resume.html",
                        help="The output file name. Defaults to 'resume.html")
    args = parser.parse_args()
    main()

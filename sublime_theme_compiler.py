#
# Created in 2024 by Gaëtan Serré
#

import argparse
import json
import xml.dom.minidom


def cli():
    parser = argparse.ArgumentParser(
        description="A compiler new Sublime Text theme to old."
    )
    parser.add_argument("file", help="The theme to compile.")
    parser.add_argument("--output", "-o", required=True, help="The output file.")
    return parser.parse_args()


def xml_key(key):
    return f"<key>{key}</key>"


def xml_string(key, value):
    return f"{xml_key(key)}<string>{value}</string>"


def extract_variables(key, theme_dict):
    return theme_dict["variables"][key.strip()]


def parse_color(color, theme_dict):
    if color.startswith("#"):
        return color
    elif color.startswith("var("):
        return extract_variables(color[4:-1], theme_dict)
    elif color.startswith("color("):
        color = color[6:-1].split(" ")
        original_color = extract_variables(color[0][4:-1], theme_dict)
        alpha = str(hex(int(float(color[1][6:-1]) * 255)))[2:]
        return original_color + alpha
    else:
        return color


def parse_globals(theme_dict):
    res = "<dict>" + xml_key("settings") + "<dict>"
    for key, value in theme_dict["globals"].items():
        res += xml_string(key, parse_color(value, theme_dict))
    res += "</dict></dict>"
    return res


def parse_scope(theme_dict, scope):
    res = "<dict>"
    if "name" in scope:
        res += xml_string("name", scope["name"])
    if "scope" in scope:
        res += xml_string("scope", scope["scope"])
    res += xml_key("settings") + "<dict>"
    for key, value in scope.items():
        if key in ["name", "scope"]:
            continue
        res += xml_string(key, parse_color(value, theme_dict))
    res += "</dict></dict>"
    return res


def parse_scopes(theme_dict):
    res = ""
    for scope in theme_dict["rules"]:
        res += parse_scope(theme_dict, scope)
    return res


def create_old_theme(file_path, output_path):
    with open(file_path, "r") as file:
        theme_dict = json.load(file)

    xml_header = """<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><dict>"""

    old_theme = (
        xml_header
        + xml_string("name", theme_dict["name"])
        + xml_key("settings")
        + "<array>"
        + parse_globals(theme_dict)
        + parse_scopes(theme_dict)
        + "</array></dict>"
    )

    with open(output_path, "w") as file:
        file.write(xml.dom.minidom.parseString(old_theme).toprettyxml())


if __name__ == "__main__":
    args = cli()

    create_old_theme(args.file, args.output)

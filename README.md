## Sublime theme compiler

This is a simple script that compiles a recent Sublime Text (`json` format) theme file into a old Sublime text theme (`.xml` format). It is written in Python 3 and uses the `json` module to parse the theme file.

This script is particularly useful for people who want to use a recent Sublime Text theme in [Typst](https://github.com/typst/typst) raw text format.

### Usage

```bash
python3 sublime_theme_compiler.py <input_file> -o <output_file>
```
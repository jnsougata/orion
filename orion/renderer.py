import re


def extract_style(content: str):
    pattern = r"<style>(.*)</style>"
    css = re.findall(pattern, content, re.DOTALL)
    return css[0] if css else ""

def extract_script(content: str):
    pattern = r"<script>(.*)</script>"
    js = re.findall(pattern, content, re.DOTALL)
    return js[0] if js else ""


class Tree:
    def __init__(self, filename: str):
        self.filename = filename
        self.html = None
        self.css = None
        self.js = None
        self.fp = None

    def __enter__(self):
        self.fp = open(self.filename)
        self.html = self.fp.read()
        self.css = extract_style(self.html)
        self.js = extract_script(self.html)
        return self

    def __str__(self):
        self.html = render_component(self.html, self)
        self.html = re.sub(
            r"<style>.*</style>",
            f"<style>{self.css}</style>",
            self.html, flags=re.DOTALL
        )
        self.html = re.sub(
            r"<script>.*</script>",
            f"<script>{self.js}</script>",
            self.html, flags=re.DOTALL
        )
        return self.html

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()



def render_component(content: str, tree: Tree):
    matches = re.findall(r"<{(.*)}>", content)
    for match in matches:
        filename = match.strip() + ".html"
        with Template(filename, tree) as c:
            pattern = "<{" + match + "}>"
            tree.css += "\n" + c.css
            tree.js += "\n" + c.js
            content = re.sub(pattern, c.html, content)
    return content

class Template:
    def __init__(self, fp: str, tree: Tree):
        self.fp = fp
        self.f = None
        self.raw_content = None
        self.css = None
        self.js = None
        self.html = None
        self.tree = tree

    def __enter__(self):
        self.f = open(self.fp)
        self.raw_content = self.f.read()
        self.css = self._style
        self.js = self._script
        self.html = render_component(self._html, self.tree)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()

    def __str__(self):
        return self.f.read()

    def __repr__(self):
        return self.f.read()

    @property
    def _style(self):
        return extract_style(self.raw_content)

    @property
    def _script(self):
        pattern = r"<script>(.*)</script>"
        js = re.findall(pattern, self.raw_content, re.DOTALL)
        return js[0] if js else ""

    @property
    def _html(self):
        pattern = r"<template>(.*)</template>"
        html = re.findall(pattern, self.raw_content, re.DOTALL)
        return html[0] if html else ""

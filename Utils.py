from flask import render_template as render_template_
import json
from Config import Company

langs=["es", "fa"]
class language:
    def __init__(self, request): self.request=request
    def translate(self, text):
        if "Lang" not in self.request.cookies or self.request.cookies["Lang"] not in langs: d="en"
        else: d=self.request.cookies["Lang"]
        b=dict(sorted(json.load(open(f"Lang/{d}.json", encoding="utf8+")).items(), key=lambda x: len(x[0]), reverse=True))
        for i in b:
            if i in text: text=text.replace(i, b[i])
        if Company!="": text=text.replace("VPS Control Panel", f"{Company} VPS Control Panel")
        return text
    def render_template(self, *arg, **kwarg): return self.translate(render_template_(*arg, **kwarg))
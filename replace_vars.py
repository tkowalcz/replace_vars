import re
import os
from markdown.preprocessors import Preprocessor
from markdown import Extension

# Match {{ some.var.name }}
VAR_RE = re.compile(r"{{\s*([\w\.-]+)\s*}}")

class ReplaceVarsPreprocessor(Preprocessor):
    def __init__(self, md, replacements):
        super().__init__(md)
        self.replacements = replacements or {}

    def run(self, lines):
        def _repl(m):
            name = m.group(1)
            # 1) explicit replacements from mkdocs.yml
            if name in self.replacements:
                return self.replacements[name]
            # 2) env var fallback: look up the exact name (with dots)
            env_val = os.getenv(name)
            if env_val is not None:
                return env_val
            # 3) nothing found → leave placeholder
            return m.group(0)

        return [VAR_RE.sub(_repl, line) for line in lines]

class ReplaceVarsExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'replacements': [{}, "Mapping of variable names to replacement strings"]
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        replacements = self.getConfig('replacements')
        md.preprocessors.register(
            ReplaceVarsPreprocessor(md, replacements),
            'replace_vars',
            175
        )

def makeExtension(**kwargs):
    return ReplaceVarsExtension(**kwargs)

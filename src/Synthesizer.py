import ast
import shutil
from pathlib import Path
from helper import get_primitive_schema

class Synthesizer:

    def __init__(self):
        self.genAst = ast.Module([], [])
        self.addImports()
        pass

    def addImports(self):
        self.genAst.body.append(
            ast.ImportFrom(
                module="includes.computable_primitives",
                names=[ast.alias(name="*")],
                level=0
            )
        )
        self.genAst.body.append(
            ast.ImportFrom(
                module="includes.computable_legacy_primitives",
                names=[ast.alias(name="*")],
                level=0
            )
        )

    def generateOutput(self):
        root_dir = Path(__file__).resolve().parent.parent
        output_dir = root_dir / "output" 

        if output_dir.exists():
            shutil.rmtree(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "output.py"
        with open(output_file, "w") as f:
            f.write(ast.unparse(self.genAst))

        src_folder = root_dir / "includes"
        dest_folder = root_dir / "output" / "includes"
        shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)

    def visit():
        pass
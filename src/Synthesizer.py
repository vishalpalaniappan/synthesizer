import ast
import shutil
from pathlib import Path
from helper import get_primitive_schema

class Synthesizer:

    def __init__(self, arthaIR):
        self.genAst = ast.Module([], [])
        self.narrative = arthaIR["narrative"]
        self.addImports()
        self.visit(self.genAst.body, self.narrative)

    def addImports(self):
        '''
            Adds the imports to call the computable primitives
        '''
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
        '''
            Creates output folder, unparse ast and copies include files.
        '''
        root_dir = Path(__file__).resolve().parent.parent
        output_dir = root_dir / "output" 

        # Clear output folder
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Unparse the ast
        ast.fix_missing_locations(self.genAst)
        output_file = output_dir / "output.py"
        with open(output_file, "w") as f:
            f.write(ast.unparse(self.genAst))

        # Copy includes
        src_folder = root_dir / "includes"
        dest_folder = root_dir / "output" / "includes"
        shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)

    def visit(self, astBody, narrative):
       '''
            Visit node recursively visit body of nodes.
       '''
       for node in narrative:
            if node["name"] == "behavior":
                func_node = ast.FunctionDef(
                    name=node["behaviorName"],
                    args=[],
                    body=[],
                    decorator_list=[],
                    returns=None
                )
                self.visit(func_node.body, node["body"])
                print(ast.dump(func_node))
                astBody.append(func_node)
            elif node["name"] == "participant":
                pass
            else:
                # This is temporary, I am just making the primitive name a call
                # I will get type of primitive and make decision in the coming changes
                # Only computable primitives will be called directly, the meta primitives
                # need to be address (ex. introduce needs to be synthesized as assignment)
                call_node = ast.Expr(value=ast.Call(
                    func=ast.Name(id=node["name"], ctx=ast.Load()),
                    args=[],
                    keywords=[]
                ))
                astBody.append(call_node)
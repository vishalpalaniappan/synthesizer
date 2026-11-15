import ast
import jsonata
from pathlib import Path
import shutil
from helper import get_primitive_schema
from helper import generateEntryBlock
from helper import exec

class Synthesizer:

    def __init__(self, arthaIR):
        self.genAst = ast.Module([], [])
        self.narrative = arthaIR["narrative"]
        self.initialBehavior = arthaIR["initialBehavior"]
        self.addImports()
        self.stack = []
        self.visit(self.genAst.body, self.narrative)
        self.addInitial()

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

    def addInitial(self):
        self.genAst.body.append(generateEntryBlock(self.initialBehavior))


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
        output_file = output_dir / f"{self.initialBehavior}.py"
        with open(output_file, "w") as f:
            f.write(ast.unparse(self.genAst))

        # Copy includes
        src_folder = root_dir / "includes"
        dest_folder = root_dir / "output" / "includes"
        shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)

    def synthesizeBehavior(self, behaviorNode, astBody):
        '''
            Process the behavior node and visit the children recursively
            and add synthesized output into body of synthesized behavior
        '''
        # TODO: Have not synthesized behaviors
        func_node = ast.FunctionDef(
            name=behaviorNode["behaviorName"],
            args=[],
            body=[],
            decorator_list=[],
            returns=None
        )
        self.visit(func_node.body, behaviorNode["body"])
        astBody.append(func_node)

    def synthesizeIf(self, ifNode, astBody):
        '''
            Process the if node and visit the children recursively
            and add synthesized output into body of synthesized behavior
        '''
        condition = exec("args[argName = 'condition'].value", ifNode)
        synthesizedIfNode = ast.If(
            test=ast.Name(id=condition, ctx=ast.Load()),
            body=[],
            orelse=[]
        )
        self.visit(synthesizedIfNode.body, ifNode["body"])
        astBody.append(synthesizedIfNode)

    def synthesizeCall(self, name, node):
        '''
            Synthesize computable primitive (synthesize args, alias and call)
        '''
        alias = jsonata.Jsonata("alias.aliasName").evaluate(node)

        args = []
        for arg in node["args"]:
            if (arg["argType"] == "const"):
                args.append(
                    ast.keyword(arg=arg["argName"], value=ast.Constant(value=arg["value"]))
                )
            elif (arg["argType"] == "name"):
                args.append(
                    ast.keyword(arg=arg["argName"], value=ast.Name(id=arg["value"]))
                )

        call = ast.Call(
            func=ast.Name(id=name, ctx=ast.Load()),
            args=args,
            keywords=[]
        )

        if alias:
            return ast.Assign(
                targets=[ast.Name(id=alias, ctx=ast.Store())],
                value=call
            )
        else:
            return ast.Expr(value=call)

    def processMetaPrimitive(self, node):   
        '''
            Process meta primitive node and return synthesized node.
        '''     
        # TODO: participant can also have initial value etc.
        if (node["name"] == "introduce"):
            alias = exec("alias.aliasName", node)
            participant = exec("args[argName = 'role'].value", node)
            participantType = exec(f"**[participantName = '{participant}'].body[name = 'structural_type'].args[value].value",self.narrative)

            if(participantType == "list"):
                return ast.Assign(
                    targets=[ast.Name(id=alias, ctx=ast.Store())],
                    value=ast.List(elts=[], ctx=ast.Load())
                )

    def visit(self, astBody, narrative):
       '''
            Visit node recursively visit body of nodes.
       '''
       for node in narrative:
            if node["name"] == "behavior":
                self.synthesizeBehavior(behaviorNode= node, astBody= astBody)
            elif node["name"] == "participant":
                pass
            elif node["name"] == "invoke":
                astBody.append(self.synthesizeCall(node["behaviorName"], node))
            elif node["name"] == "if":
                self.synthesizeIf(ifNode = node, astBody = astBody)
            else:
                schema = get_primitive_schema(primitiveName = node["name"])
                type = schema["properties"]["primitiveType"]["const"]

                if (type == "computable-primitive" or type == "computable-legacy-primitive"):
                    astBody.append(self.synthesizeCall(node["name"], node))
                elif (type == "meta-primitive"):
                    metaNode = self.processMetaPrimitive(node)
                    if metaNode:
                        astBody.append(metaNode)
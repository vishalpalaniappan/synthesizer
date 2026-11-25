
import ast
import jsonata

def get_primitive_schema(primitiveName: str, schema: object):
    '''
        This is a bit crude, I am searching the schema to find the schema for
        the particular node I am visiting. Then I use the schema to find out
        what kind of primitive it is and take the relevant step. In a future change
        I will establish the primitive schemas in definitions and use them, so that
        it can be accessed directly.
    '''

    def search(node):
        if isinstance(node, dict):
            if node.get("$id") == f"./{primitiveName}.schema.json":
                return node
            for value in node.values():
                result = search(value)
                if result: return result
        elif isinstance(node, list):
            for item in node:
                result = search(item)
                if result: return result
        return None

    return search(schema)

def exec(expression: str, item):
    return jsonata.Jsonata(expression).evaluate(item)

def generateEntryBlock(initialBehaviorName):
    '''
        Generates the entry of the python script.

        if __name__ == "__main__":
            <initialBehaviorName>()
    '''
    return ast.If(
        test=ast.Compare(
            left=ast.Name(id='__name__', ctx=ast.Load()),
            ops=[ast.Eq()],
            comparators=[ast.Constant(value='__main__')]
        ),
        body=[
            ast.Expr(ast.Call(
                func=ast.Name(id=initialBehaviorName, ctx=ast.Load()),
                args=[],
                keywords=[]
            ))
        ],
        orelse=[]
    )
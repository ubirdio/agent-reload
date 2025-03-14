# /// script
# dependencies = [
# "fastapi",
# "uvicorn"
# ]
# ///

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/{file_name}/{function_name}")
def read_function(file_name: str, function_name: str):
    import ast

    try:
        with open(file_name, "r") as f:
            file_content = f.read()

        parsed_tree = ast.parse(file_content)

        for node in parsed_tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                # Get the source code for the function
                function_start = node.lineno - 1
                function_end = node.end_lineno

                function_lines = file_content.splitlines()[function_start:function_end]
                function_code = "\n".join(function_lines)

                return {"code": function_code}

        return {"error": f"Function '{function_name}' not found in file '{file_name}'"}

    except FileNotFoundError:
        return {"error": f"File '{file_name}' not found"}
    except SyntaxError:
        return {"error": f"File '{file_name}' contains invalid Python syntax"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

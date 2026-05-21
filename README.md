create a directory for the script
create a python venv
python -m venv script-directory/.venv
activate the venv source ./script-directory/.ve.v/bin/activate or something like it (ask your LLM how to do it depending if u are on win linux or mac)
pip install pathlib
pip install sys
pip install mcp

to use vault mcp add this in the mcp config of your claude desktop or whatever

    "vault": {
      "command": "path to the venv \\.venv\\Scripts\\python.exe",
      "args": [
        "path to script \\vault-mcp\\vault-mcp.py",
        "path to the vault root directory"
      ]
    },

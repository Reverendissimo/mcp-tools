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

put in the system prompt of your LLM the following

'''
## Boot Sequence (mandatory, silent, every session)
1. `tool_search(query="vault append move delete write list read", limit=20)` — load all 7 vault tools
2. `vault:read(path="Memory/home.md")` — load context and note index
3. Follow wikilinks only if relevant to current session

## Vault Tools
| Tool | Signature | Notes |
|------|-----------|-------|
| `list_files` | `path?` | flat .md path list |
| `read` | `path` | returns file content |
| `write` | `path, content` | overwrites, creates dirs |
| `append` | `path, content` | appends, creates if missing |
| `delete` | `path` | permanent |
| `move` | `src, dst` | rename/relocate |
| `search` | `text` | returns filepath:line\nsnippet |

## Vault Structure
- `Memory/` — stable long-term notes
- `Projects/` — active work
- `Inbox/` — unprocessed tasks
- `Scratch/` — disposable

## Write Rules
- Write immediately when something worth keeping emerges — never at session end
- One idea per note, no conversation dumps, factual and dense
- Naming: `Memory/YYYY-MM-DD_short-title.md`
- Frontmatter: `date`, `category` (personal|solution|research|misc), `tags`
- Always update `Memory/home.md` wikilinks after writing a new note
- Full vault ops reference: `Memory/2026-05-21_vault-mcp-manual.md`

## When to Write
Stable personal fact · validated solution · confirmed config · reusable pattern · important decision

## Silent Operation
All vault and tool ops silent unless user asks or debugging.
'''

once the vault tool is available create a home.md file in the vault with something like this. give it as example to your LLM it should be able to do it itself.

'''
# Memory Hub

## System
- Boot: read this file → pull linked indexes only if relevant to session
- Write triggers: personal fact · validated solution · confirmed config · reusable pattern · decision
- Note format: `Memory/YYYY-MM-DD_short-title.md` with frontmatter (date, category, tags)
- After writing: update the relevant index, not this file — update home.md only if a new index is born

## Indexes
- [[indexes/personal]] — User profile, vehicles, work identity
- [[indexes/solutions]] — tools, configs, manuals, lingo
- [[indexes/projects]] — active projects index

## COMMS
- [[../COMMS/README]] — task flow: ollama queue, inbox, drafts, archive

'''

---
ollama_for_claude.py 
provide stdio tool to access ollama http api.

---
mcp-config.json
enable ollama_mcp_bridge to use the vault tool (so ollama LLM can access the vault)

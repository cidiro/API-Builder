# deno.json.py
# deno.json builder

def build(entities):
    return """
{
  "tasks": {
    "dev": "deno run --allow-all --env --watch main.ts",
    "start": "deno run --allow-all --env main.ts"
  },
  "imports": {
    "@apollo/server": "npm:@apollo/server",
    "@apollo/server/standalone": "npm:@apollo/server/standalone",
    "graphql": "npm:graphql@^16.8.1",
    "mongoose": "npm:mongoose@^8.0.1"
  }
}
""".lstrip()

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { 
  CallToolRequestSchema, 
  ListToolsRequestSchema 
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";
import path from "path";
import fs from "fs";

const server = new Server(
  {
    name: "crucible-local-db",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Cache for active DB connections to avoid reopening repeatedly
const dbCache = new Map();

function getDb(dbPath) {
  const absPath = path.resolve(dbPath);
  if (!fs.existsSync(absPath)) {
      // Ensure directory exists before creating a new DB
      const dir = path.dirname(absPath);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  }
  
  if (!dbCache.has(absPath)) {
    const db = new Database(absPath);
    dbCache.set(absPath, db);
  }
  return dbCache.get(absPath);
}

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query_db",
        description: "Execute a SQL query against a local SQLite database.",
        inputSchema: {
          type: "object",
          properties: {
            db_path: { type: "string", description: "Absolute or relative path to the SQLite .db file." },
            query: { type: "string", description: "The SQL query to execute." },
            params: { 
              type: "array", 
              description: "Optional array of parameters for the query.",
              items: { type: "string" } 
            }
          },
          required: ["db_path", "query"],
        },
      },
      {
        name: "list_tables",
        description: "List all tables and their schema in a SQLite database.",
        inputSchema: {
          type: "object",
          properties: {
            db_path: { type: "string", description: "Path to the SQLite .db file." }
          },
          required: ["db_path"],
        },
      }
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    const db = getDb(args.db_path);

    if (name === "query_db") {
      const stmt = db.prepare(args.query);
      const isSelect = args.query.trim().toUpperCase().startsWith("SELECT");
      const params = args.params || [];
      
      let result;
      if (isSelect) {
        result = stmt.all(...params);
      } else {
        const info = stmt.run(...params);
        result = { changes: info.changes, lastInsertRowid: info.lastInsertRowid };
      }
      
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      
    } else if (name === "list_tables") {
      const stmt = db.prepare("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'");
      const tables = stmt.all();
      return { content: [{ type: "text", text: JSON.stringify(tables, null, 2) }] };
      
    } else {
      throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return { 
      content: [{ type: "text", text: `Database Error: ${error.message}` }],
      isError: true 
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Crucible Local DB Bridge (MCP) running on stdio.");
}

main().catch((error) => {
  console.error("Fatal error in Local DB Bridge:", error);
  process.exit(1);
});

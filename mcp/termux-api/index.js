import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { 
  CallToolRequestSchema, 
  ListToolsRequestSchema 
} from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "child_process";

const server = new Server(
  {
    name: "crucible-hardware-bridge",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Helper to run termux-api commands
 */
function runTermux(cmd) {
  try {
    return execSync(cmd).toString().trim();
  } catch (error) {
    return `Error running ${cmd}: ${error.message}`;
  }
}

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "battery_status",
        description: "Get current battery level, health, and charging status.",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "get_clipboard",
        description: "Read the current contents of the Android system clipboard.",
        inputSchema: { type: "object", properties: {} },
      },
      {
        name: "set_clipboard",
        description: "Write text to the Android system clipboard.",
        inputSchema: {
          type: "object",
          properties: {
            text: { type: "string", description: "The text to copy to clipboard." },
          },
          required: ["text"],
        },
      },
      {
        name: "send_notification",
        description: "Send an Android push notification via termux-api.",
        inputSchema: {
          type: "object",
          properties: {
            title: { type: "string", description: "Notification title." },
            content: { type: "string", description: "Notification body text." },
          },
          required: ["title", "content"],
        },
      },
    ],
  };
});

/**
 * Handle tool execution
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "battery_status":
      return { content: [{ type: "text", text: runTermux("termux-battery-status") }] };
    
    case "get_clipboard":
      return { content: [{ type: "text", text: runTermux("termux-clipboard-get") }] };
    
    case "set_clipboard":
      runTermux(`termux-clipboard-set "${args.text}"`);
      return { content: [{ type: "text", text: `Successfully copied to clipboard.` }] };
    
    case "send_notification":
      runTermux(`termux-notification --title "${args.title}" --content "${args.content}"`);
      return { content: [{ type: "text", text: `Notification sent.` }] };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Crucible Hardware Bridge (MCP) running on stdio.");
}

main().catch((error) => {
  console.error("Fatal error in Crucible Hardware Bridge:", error);
  process.exit(1);
});

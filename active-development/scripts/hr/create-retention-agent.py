#!/usr/bin/env python3
"""
Employee Retention AI Agent - Agent Garden Creator
===================================================
Creates a structured Boomi Agent Garden agent that leverages the 3 MCP tools
built for employee retention and satisfaction:

  1. get_retention_risk_report  - retention risk data by dept/risk level
  2. get_engagement_metrics     - engagement scores, trends, key drivers
  3. recommend_retention_actions - targeted retention action recommendations

Each MCP tool is exposed as an Agent Garden OpenAPI tool pointing to the
MCP server's HTTP messages endpoint on the Atom.

Usage:
    python create-retention-agent.py [--atom-host <host>] [--dry-run]

    --atom-host   Atom hostname or IP (default: localhost)
    --dry-run     Print the config that would be sent, without calling API
"""

import os
import sys
import json
import argparse
import importlib.util
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# ── locate .env (workspace root, two levels up from scripts/) ────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent          # scripts → active-development → workspace root
env_path = WORKSPACE_ROOT / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"Loaded .env from {env_path}")
else:
    load_dotenv()
    print("Warning: .env not found at workspace root, trying CWD fallback")

# ── add agent-garden-api.py to path ─────────────────────────────────────────
AGENT_GARDEN_SCRIPT = (
    SCRIPT_DIR.parent.parent.parent   # scripts → active-development → workspace → ClaudeCode
    / "boomi-agent-tool-pr-v2.2" / "tools" / "agent-garden-api.py"
)

if not AGENT_GARDEN_SCRIPT.exists():
    print(f"ERROR: agent-garden-api.py not found at {AGENT_GARDEN_SCRIPT}")
    print("Expected location: ../boomi-agent-tool-pr-v2.2/tools/agent-garden-api.py")
    sys.exit(1)

# Load the hyphenated script via importlib (hyphens are not valid in module names)
spec = importlib.util.spec_from_file_location("agent_garden_api", AGENT_GARDEN_SCRIPT)
_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_mod)

create_openapi_tool = _mod.create_openapi_tool
install_tool        = _mod.install_tool
create_agent        = _mod.create_agent
activate_agent      = _mod.activate_agent

# ── MCP server config ────────────────────────────────────────────────────────
MCP_SERVER_NAME   = "employee-retention"
MCP_TOKEN         = "a7f3e219-4b8d-4c2a-9d1e-3f7b6c852a0e"
MCP_PORT          = 8000

# ── tool definitions ─────────────────────────────────────────────────────────
TOOLS_CONFIG = [
    {
        "name": "EmployeeRetention - Get Retention Risk Report",
        "description": (
            "Retrieves a list of employees categorized by retention risk level. "
            "Optionally filter by department and/or risk level to identify at-risk "
            "employees and their key risk factors. Returns employee details including "
            "name, department, role, tenure, risk score, and risk factors."
        ),
        "path": f"/mcp/{MCP_SERVER_NAME}/messages",
        "method": "POST",
        "input_parameters": [
            {
                "name": "department",
                "type": "string",
                "required": False,
                "description": (
                    "Filter by department name "
                    "(e.g., Engineering, Sales, Marketing, Product, Customer Success). "
                    "Omit or pass 'all' to include all departments."
                )
            },
            {
                "name": "risk_level",
                "type": "string",
                "required": False,
                "description": (
                    "Filter by risk classification. "
                    "Accepted values: high, medium, low, all. "
                    "Omit or pass 'all' to see every risk tier."
                )
            }
        ],
        "request_body": {
            "type": "application/json",
            "template": json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "get_retention_risk_report",
                    "arguments": {
                        "department": "{{department}}",
                        "risk_level": "{{risk_level}}"
                    }
                },
                "id": 1
            })
        }
    },
    {
        "name": "EmployeeRetention - Get Engagement Metrics",
        "description": (
            "Returns employee engagement scores, trends, key satisfaction drivers, "
            "and top workforce concerns. Optionally filter by department and time period. "
            "Includes an overall score benchmarked against industry averages and a breakdown "
            "by department with trend indicators."
        ),
        "path": f"/mcp/{MCP_SERVER_NAME}/messages",
        "method": "POST",
        "input_parameters": [
            {
                "name": "department",
                "type": "string",
                "required": False,
                "description": (
                    "Filter engagement data by a specific department "
                    "(e.g., Engineering, Sales). Omit or pass 'all' for company-wide view."
                )
            },
            {
                "name": "period",
                "type": "string",
                "required": False,
                "description": (
                    "Time period for the metrics. "
                    "Examples: current_quarter, last_quarter, ytd. "
                    "Defaults to current_quarter."
                )
            }
        ],
        "request_body": {
            "type": "application/json",
            "template": json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "get_engagement_metrics",
                    "arguments": {
                        "department": "{{department}}",
                        "period": "{{period}}"
                    }
                },
                "id": 1
            })
        }
    },
    {
        "name": "EmployeeRetention - Recommend Retention Actions",
        "description": (
            "Generates targeted, prioritized retention action recommendations "
            "based on risk level, department, and focus area. Returns a list of "
            "concrete actions with estimated impact, timeframes, and immediate next steps. "
            "Also lists resources needed to execute the recommendations."
        ),
        "path": f"/mcp/{MCP_SERVER_NAME}/messages",
        "method": "POST",
        "input_parameters": [
            {
                "name": "risk_level",
                "type": "string",
                "required": False,
                "description": (
                    "Target recommendations at a specific risk tier: high, medium, or low. "
                    "Defaults to high (most urgent)."
                )
            },
            {
                "name": "department",
                "type": "string",
                "required": False,
                "description": (
                    "Scope recommendations to a department "
                    "(e.g., Engineering, Sales). Omit for company-wide recommendations."
                )
            },
            {
                "name": "focus_area",
                "type": "string",
                "required": False,
                "description": (
                    "Category of retention levers to focus on. "
                    "Examples: compensation, career_growth, management, work_life_balance. "
                    "Omit for all focus areas."
                )
            }
        ],
        "request_body": {
            "type": "application/json",
            "template": json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "recommend_retention_actions",
                    "arguments": {
                        "risk_level": "{{risk_level}}",
                        "department": "{{department}}",
                        "focus_area": "{{focus_area}}"
                    }
                },
                "id": 1
            })
        }
    }
]


def build_base_url(atom_host: str) -> str:
    return f"http://{atom_host}:{MCP_PORT}"


def create_all_tools(base_url: str, dry_run: bool = False) -> List[Dict]:
    """Create and install all 3 OpenAPI tools. Returns list of created tool records."""
    created_tools = []

    for i, cfg in enumerate(TOOLS_CONFIG, 1):
        print(f"\n[{i}/3] Creating tool: {cfg['name']}")

        if dry_run:
            print(f"  DRY RUN - would POST to Agent Garden:")
            print(f"    base_url: {base_url}")
            print(f"    path:     {cfg['path']}")
            print(f"    params:   {json.dumps(cfg['input_parameters'], indent=6)}")
            created_tools.append({
                "id": f"dry-run-tool-id-{i}",
                "name": cfg["name"],
                "unique_name": f"dry_run_tool_{i}"
            })
            continue

        result = create_openapi_tool(
            name=cfg["name"],
            description=cfg["description"],
            base_url=base_url,
            path=cfg["path"],
            method=cfg["method"],
            input_parameters=cfg["input_parameters"],
            headers=[{"name": "Authorization", "static_value": f"Bearer {MCP_TOKEN}"}],
            authentication={
                "type": "token_auth",
                "token": f"Bearer {MCP_TOKEN}",
                "header_name": "Authorization"
            },
            request_body=cfg.get("request_body")
        )

        tool_data = result.get("data", result)
        tool_id   = tool_data["id"]
        uname     = tool_data.get("unique_name", "")

        print(f"  Tool ID:     {tool_id}")
        print(f"  Unique name: {uname}")
        print(f"  Installing tool...")

        install_result = install_tool("openapi", tool_id)
        print(f"  Installed:   OK")

        created_tools.append({
            "id":          tool_id,
            "name":        cfg["name"],
            "unique_name": uname
        })

    return created_tools


def build_agent_tasks(tools: List[Dict]) -> List[Dict]:
    """Map tools to structured agent tasks."""
    tool_map = {t["name"]: t for t in tools}

    tasks = [
        {
            "name": "Assess Retention Risk",
            "objective": (
                "Retrieve and analyse employee retention risk data. "
                "Identify individuals and departments with elevated departure probability "
                "and surface the underlying risk factors driving attrition."
            ),
            "instructions": [
                "Parse the user query to determine if a department or risk-level filter was requested.",
                "Call the retention risk report tool with the appropriate filters.",
                "Summarise the results: total at-risk count, highest-risk individuals, "
                "and predominant risk factors.",
                "Flag any employees with a risk score above 80 as requiring immediate attention."
            ],
            "tools": [
                {
                    "id":                 tool_map["EmployeeRetention - Get Retention Risk Report"]["id"],
                    "name":               "EmployeeRetention - Get Retention Risk Report",
                    "type":               "OpenAPI",
                    "unique_name":        tool_map["EmployeeRetention - Get Retention Risk Report"]["unique_name"],
                    "requires_approval":  False,
                    "response_passthrough": False
                }
            ]
        },
        {
            "name": "Analyse Engagement Metrics",
            "objective": (
                "Pull employee engagement scores, trends, and workforce sentiment data. "
                "Interpret what the numbers mean for overall organisational health "
                "and highlight the key drivers and concerns expressed by employees."
            ),
            "instructions": [
                "Determine if the user wants a specific department or time period.",
                "Call the engagement metrics tool with the identified filters.",
                "Present the overall engagement score, benchmark comparison, and trend direction.",
                "List the top 3 key satisfaction drivers and top 3 employee concerns.",
                "Call out any department with a declining trend as a priority area."
            ],
            "tools": [
                {
                    "id":                 tool_map["EmployeeRetention - Get Engagement Metrics"]["id"],
                    "name":               "EmployeeRetention - Get Engagement Metrics",
                    "type":               "OpenAPI",
                    "unique_name":        tool_map["EmployeeRetention - Get Engagement Metrics"]["unique_name"],
                    "requires_approval":  False,
                    "response_passthrough": False
                }
            ]
        },
        {
            "name": "Recommend Retention Actions",
            "objective": (
                "Generate concrete, prioritised retention action recommendations "
                "tailored to the risk tier, department, and focus area specified by the user. "
                "Provide a clear execution roadmap with timelines and resource requirements."
            ),
            "instructions": [
                "Identify the risk level, department, and focus area from the user's request.",
                "Call the retention actions tool with those parameters.",
                "Present recommendations in priority order (critical → high → medium).",
                "Include estimated impact and implementation timeframe for each action.",
                "Highlight the immediate actions that should start within the week.",
                "Summarise the resources required to execute the full recommendation set."
            ],
            "tools": [
                {
                    "id":                 tool_map["EmployeeRetention - Recommend Retention Actions"]["id"],
                    "name":               "EmployeeRetention - Recommend Retention Actions",
                    "type":               "OpenAPI",
                    "unique_name":        tool_map["EmployeeRetention - Recommend Retention Actions"]["unique_name"],
                    "requires_approval":  False,
                    "response_passthrough": False
                }
            ]
        }
    ]
    return tasks


def main():
    parser = argparse.ArgumentParser(
        description="Create Employee Retention structured agent in Boomi Agent Garden"
    )
    parser.add_argument(
        "--atom-host",
        default="localhost",
        help="Atom hostname or IP address (default: localhost)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print config without calling the API"
    )
    args = parser.parse_args()

    base_url = build_base_url(args.atom_host)
    dry_run  = args.dry_run

    print("=" * 60)
    print("  Employee Retention Agent - Agent Garden Creator")
    print("=" * 60)
    print(f"  MCP base URL : {base_url}")
    print(f"  Dry run      : {dry_run}")
    print("=" * 60)

    # ── Step 1: Create tools ─────────────────────────────────────────────────
    print("\nSTEP 1: Creating OpenAPI tools")
    tools = create_all_tools(base_url, dry_run=dry_run)

    # ── Step 2: Create structured agent ─────────────────────────────────────
    print("\nSTEP 2: Building agent task definitions")
    tasks = build_agent_tasks(tools)
    print(f"  {len(tasks)} tasks configured")

    agent_name = "Employee Retention & Satisfaction Agent"
    agent_objective = (
        "Help HR professionals and people managers understand employee retention risk, "
        "interpret engagement data, and take targeted action to improve workforce "
        "satisfaction and reduce voluntary attrition. "
        "Process natural language queries to surface retention insights, engagement "
        "trends, and prioritised recommendations drawn from live employee data."
    )

    conversation_starters = [
        "Show me employees at high risk of leaving, especially in Engineering.",
        "What are our current engagement scores and what are employees most concerned about?",
        "Which departments have declining engagement trends this quarter?",
        "What actions should we take immediately to retain at-risk employees in Sales?",
        "Give me a full retention risk report for the Product team."
    ]

    personality = {
        "voice_tone": "Professional",
        "creativity": 25,
        "clarity":    90
    }

    print("\nSTEP 3: Creating structured agent in Agent Garden")
    print(f"  Name: {agent_name}")

    if dry_run:
        print("  DRY RUN - agent config preview:")
        print(json.dumps({
            "name":                 agent_name,
            "objective":            agent_objective,
            "agent_mode":           "conversational",
            "personality_traits":   personality,
            "conversation_starters": conversation_starters,
            "tasks":                tasks
        }, indent=2))
        print("\nDry run complete. No API calls were made.")
        return

    # Note: "structured" agent_mode requires explicit JSON I/O schemas (not yet
    # supported by agent-garden-api.py). For natural-language query processing,
    # "conversational" mode is correct — the agent still has structured tasks and
    # tools, it simply engages via dialogue rather than fixed I/O schemas.
    agent_result = create_agent(
        name=agent_name,
        objective=agent_objective,
        tasks=tasks,
        personality_traits=personality,
        conversation_starters=conversation_starters,
        agent_mode="conversational",
        status="DRAFT",
        validate=True
    )

    agent_data = agent_result.get("data", agent_result)
    agent_id   = agent_data["id"]

    print(f"  Agent created: {agent_id}")
    print(f"  Status: {agent_data.get('agent_status', 'DRAFT')}")

    # ── Step 4: Activate agent ───────────────────────────────────────────────
    print("\nSTEP 4: Activating agent")
    activate_agent(agent_id)
    print(f"  Agent activated!")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  DONE - Agent created and activated")
    print("=" * 60)
    print(f"  Agent ID   : {agent_id}")
    print(f"  Agent name : {agent_name}")
    print(f"  Tools      : {len(tools)}")
    print(f"  Tasks      : {len(tasks)}")
    print()
    print(f"  View in UI:")
    print(f"  https://platform.boomi.com/BoomiAI.html#/agents/{agent_id}")
    print()
    print("  Tools created:")
    for t in tools:
        print(f"    - {t['name']}")
        print(f"      ID: {t['id']}")
    print()
    print("  NOTE: Update the tool base_url from 'localhost' to your")
    print(f"  Atom host if you're not running locally. Current base URL:")
    print(f"  {base_url}")


if __name__ == "__main__":
    main()

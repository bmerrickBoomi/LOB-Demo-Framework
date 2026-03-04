#!/usr/bin/env python3
"""
HR Operations Console Agent - Agent Garden Creator
====================================================
Creates a structured Boomi Agent Garden agent that surfaces HR operations
data through 9 OpenAPI tools backed by the HROpsConsole Boomi processes:

  GET  /ws/simple/getHrOpsDashboard      - KPIs, priority queue, time-saved
  GET  /ws/simple/getHrOpsEmployees      - Employee roster with cross-system profiles
  GET  /ws/simple/getHrOpsCases          - Case management data
  POST /ws/simple/createHrOpsCase        - Create a new HR case
  GET  /ws/simple/getHrOpsCompliance     - Compliance alerts and training status
  GET  /ws/simple/getHrOpsIntegrations   - HR system integration health
  GET  /ws/simple/getHrOpsTasks          - Task queue and manager actions
  GET  /ws/simple/getHrOpsNotifications  - System notifications and alerts
  GET  /ws/simple/getHrOpsAuditlog       - Audit trail of HR operations

The agent is created in STRUCTURED mode with JSON input/output schemas,
making it suitable for programmatic orchestration as well as natural-language
interaction via the Boomi Agent Garden UI.

Prerequisites:
  - HROpsConsole-APIs Boomi processes deployed to the target environment
  - API Management (APIM) configured on the Advanced atom to expose the
    WSS endpoints (the processes exist but need APIM publishing to be callable)

Usage:
    python create-hrops-agent.py [--atom-host <host>] [--dry-run]

    --atom-host   Shared web server hostname (default: c02-usa-east.integrate.boomi.com)
    --dry-run     Print config without calling the API
"""

import os
import sys
import json
import argparse
import importlib.util
import requests
from base64 import b64encode
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# ── locate .env (workspace root, two levels up from scripts/) ────────────────
SCRIPT_DIR     = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent          # scripts → active-development → workspace root
env_path       = WORKSPACE_ROOT / ".env"
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

spec = importlib.util.spec_from_file_location("agent_garden_api", AGENT_GARDEN_SCRIPT)
_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_mod)

create_openapi_tool        = _mod.create_openapi_tool
install_tool               = _mod.install_tool
activate_agent             = _mod.activate_agent
get_headers                = _mod.get_headers
AGENT_GARDEN_BASE_URL      = _mod.AGENT_GARDEN_BASE_URL

# ── HR Ops API config ─────────────────────────────────────────────────────────
SERVER_BASE_URL  = os.getenv("SERVER_BASE_URL", "https://c02-usa-east.integrate.boomi.com")
SERVER_USERNAME  = os.getenv("SERVER_USERNAME", "")
SERVER_TOKEN     = os.getenv("SERVER_TOKEN", "")

def build_basic_auth_header() -> str:
    """Build a Basic auth header value from SERVER_USERNAME:SERVER_TOKEN."""
    creds = b64encode(f"{SERVER_USERNAME}:{SERVER_TOKEN}".encode()).decode()
    return f"Basic {creds}"


# ── Tool definitions ──────────────────────────────────────────────────────────
#
# Endpoint URL formula (from WSS operation XML):
#   lowercase(operationType) + SentenceCase(objectName)
#   e.g. operationType=GET, objectName=hrOpsDashboard → /ws/simple/getHrOpsDashboard
#
TOOLS_CONFIG = [
    {
        "name":        "HROps - Get Dashboard",
        "description": (
            "Retrieves the HR Operations Console dashboard data: KPI metrics "
            "(open cases, critical cases, overdue manager actions, compliance alerts, "
            "sync errors, payroll exceptions, retention risk), time-saved estimates "
            "(baseline hours, weekly savings in hours and dollars, annual projection), "
            "case status distribution, and a prioritised action queue of the highest-"
            "urgency items requiring immediate HR attention."
        ),
        "path":   "/ws/simple/getHrOpsDashboard",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Get Employees",
        "description": (
            "Retrieves the complete employee roster with full cross-system profiles. "
            "Each record includes: employee ID, name, department, role, employment status, "
            "manager, location, hire date, salary (HRIS and Payroll), engagement score "
            "(Glint), performance rating (Lattice), benefits enrollment (Benefitfocus), "
            "and retention risk level. Covers all 15 employees across Engineering, Sales, "
            "Customer Success, Marketing, Finance, and HR departments."
        ),
        "path":   "/ws/simple/getHrOpsEmployees",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Get Cases",
        "description": (
            "Retrieves all HR case management records. Each case includes: case ID, type "
            "(Employee Relations, Accommodation, Compliance, Performance, Integration), "
            "title, description, linked employee, assigned owner, status (Open, Investigation, "
            "Under Review, Approved, Critical, Closed), severity (Low/Medium/High/Critical), "
            "SLA date, case notes timeline, and task list. Useful for reviewing open ER issues, "
            "accommodation requests, compliance violations, PIPs, and integration exceptions."
        ),
        "path":   "/ws/simple/getHrOpsCases",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Create Case",
        "description": (
            "Creates a new HR case in the system. Use this to open a case for an employee "
            "relation issue, accommodation request, policy violation, performance concern, "
            "or integration error. Returns the new case ID and confirmation."
        ),
        "path":   "/ws/simple/createHrOpsCase",
        "method": "POST",
        "input_parameters": [
            {
                "name":        "type",
                "type":        "string",
                "required":    True,
                "description": (
                    "Case type. Must be one of: Employee Relations, Accommodation, "
                    "Compliance, Performance, Integration."
                )
            },
            {
                "name":        "title",
                "type":        "string",
                "required":    True,
                "description": "Short descriptive title of the case."
            },
            {
                "name":        "employee_id",
                "type":        "string",
                "required":    True,
                "description": "Employee ID (e.g. E001) of the subject employee."
            },
            {
                "name":        "severity",
                "type":        "string",
                "required":    True,
                "description": "Case severity. Must be one of: Low, Medium, High, Critical."
            },
            {
                "name":        "notes",
                "type":        "string",
                "required":    False,
                "description": "Initial case notes or description of the issue."
            },
            {
                "name":        "sla_date",
                "type":        "string",
                "required":    False,
                "description": "Target resolution date in YYYY-MM-DD format."
            },
        ],
    },
    {
        "name":        "HROps - Get Compliance",
        "description": (
            "Retrieves compliance tracking data across all employees and departments. "
            "Includes: mandatory training completions (harassment prevention, safety modules, "
            "HIPAA, etc.), policy sign-off status, overdue items with days-past-due counts, "
            "and compliance alerts by type and department. Critical for identifying regulatory "
            "risk exposure and prioritising remediation efforts."
        ),
        "path":   "/ws/simple/getHrOpsCompliance",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Get Integrations",
        "description": (
            "Retrieves the health and sync status of all five HR system integrations: "
            "Workday HRIS, ADP Payroll, Benefitfocus (Benefits), Lattice (Performance), "
            "and Glint (Engagement). Each integration record includes: last sync timestamp, "
            "sync status (Active/Error/Warning), error counts, error details with specific "
            "field discrepancies between systems (e.g. salary mismatches, terminated employees "
            "still active in payroll), and reconciliation status. Use this to diagnose data "
            "integrity issues across the HR technology stack."
        ),
        "path":   "/ws/simple/getHrOpsIntegrations",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Get Tasks",
        "description": (
            "Retrieves the HR operations task queue. Tasks are linked to cases or flagged as "
            "standalone manager action items. Each task includes: title, linked case ID, "
            "assigned employee, task owner, due date, severity, and completion status. "
            "Use this to identify overdue tasks, assign follow-up actions, and track "
            "progress against case resolution milestones."
        ),
        "path":   "/ws/simple/getHrOpsTasks",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Get Notifications",
        "description": (
            "Retrieves system notifications and alerts for the HR Operations Console. "
            "Notification types include: new case assignments, SLA warnings, compliance "
            "deadline reminders, integration sync errors, manager action required flags, "
            "and system status updates. Each notification includes a timestamp, category, "
            "severity, and read/unread status."
        ),
        "path":   "/ws/simple/getHrOpsNotifications",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name":        "HROps - Get Audit Log",
        "description": (
            "Retrieves the HR operations audit trail. Each audit log entry records: timestamp, "
            "action type (case_update, reconciliation, compliance_flag, system_sync, etc.), "
            "target entity (employee ID or case ID), the user who performed the action, "
            "and details of what changed. Use this for compliance auditing, investigating "
            "data changes, or understanding the history of HR operations activity."
        ),
        "path":   "/ws/simple/getHrOpsAuditlog",
        "method": "GET",
        "input_parameters": [],
    },
]


def create_all_tools(base_url: str, auth_header: str, dry_run: bool = False) -> List[Dict]:
    """Create and install all 9 HR Ops OpenAPI tools. Returns created tool records."""
    created_tools = []
    total = len(TOOLS_CONFIG)

    for i, cfg in enumerate(TOOLS_CONFIG, 1):
        print(f"\n[{i}/{total}] Creating tool: {cfg['name']}")

        if dry_run:
            print(f"  DRY RUN - base_url: {base_url}")
            print(f"            path:     {cfg['path']}")
            print(f"            method:   {cfg['method']}")
            if cfg["input_parameters"]:
                print(f"            params:   {len(cfg['input_parameters'])} defined")
            created_tools.append({
                "id":          f"dry-run-tool-id-{i}",
                "name":        cfg["name"],
                "unique_name": f"dry_run_tool_{i}"
            })
            continue

        # Build per-tool args
        kwargs = dict(
            name             = cfg["name"],
            description      = cfg["description"],
            base_url         = base_url,
            path             = cfg["path"],
            method           = cfg["method"],
            headers          = [{"name": "Authorization", "static_value": auth_header}],
            authentication   = {
                "type":        "token_auth",
                "token":       auth_header,
                "header_name": "Authorization"
            },
        )

        if cfg["input_parameters"]:
            kwargs["input_parameters"] = cfg["input_parameters"]

        # POST tools use a simple JSON pass-through body template
        if cfg["method"] == "POST" and cfg["input_parameters"]:
            body_params = {p["name"]: f"{{{{{p['name']}}}}}" for p in cfg["input_parameters"]}
            kwargs["request_body"] = {
                "type":     "application/json",
                "template": json.dumps(body_params)
            }

        result    = create_openapi_tool(**kwargs)
        tool_data = result.get("data", result)
        tool_id   = tool_data["id"]
        uname     = tool_data.get("unique_name", "")

        print(f"  Tool ID:     {tool_id}")
        print(f"  Unique name: {uname}")
        print(f"  Installing tool...")

        install_tool("openapi", tool_id)
        print(f"  Installed:   OK")

        created_tools.append({
            "id":          tool_id,
            "name":        cfg["name"],
            "unique_name": uname
        })

    return created_tools


def build_agent_tasks(tools: List[Dict]) -> List[Dict]:
    """Map tools to structured agent tasks covering key HR operational workflows."""
    tool_map = {t["name"]: t for t in tools}

    def binding(tool_name: str) -> Dict:
        t = tool_map[tool_name]
        return {
            "id":                   t["id"],
            "name":                 t["name"],
            "type":                 "OpenAPI",
            "unique_name":          t["unique_name"],
            "requires_approval":    False,
            "response_passthrough": False
        }

    return [
        {
            "name": "HR Dashboard & Priority Queue",
            "objective": (
                "Retrieve the HR operations dashboard to surface key performance indicators, "
                "identify the highest-priority items requiring immediate attention, and report "
                "on time savings achieved through HR process automation."
            ),
            "instructions": [
                "Call the Dashboard tool to retrieve current KPIs.",
                "Summarise the critical metrics: open cases, critical cases, overdue manager "
                "actions, compliance alerts, sync errors, payroll exceptions, and retention risk.",
                "Present the top priority queue items sorted by severity and due date.",
                "Report the weekly and annual time-savings dollar value based on the "
                "configured hourly rate and baseline hours.",
                "Flag any metric exceeding normal thresholds (e.g. more than 2 critical cases, "
                "compliance alerts above 10, sync errors above 5)."
            ],
            "tools": [binding("HROps - Get Dashboard")]
        },
        {
            "name": "Employee Profile & Cross-System Analysis",
            "objective": (
                "Retrieve employee records and analyse cross-system data integrity across "
                "Workday HRIS, ADP Payroll, Benefitfocus, Lattice, and Glint. Identify "
                "discrepancies, risk levels, and employees requiring HR attention."
            ),
            "instructions": [
                "Call the Employees tool to retrieve the full roster.",
                "If the user specifies an employee name or ID, filter results to that employee.",
                "If the user specifies a department, filter to that department.",
                "Highlight any salary mismatches between HRIS and Payroll.",
                "List employees with High retention risk level.",
                "Note any terminated employees who remain active in downstream systems.",
                "Report benefits enrollment gaps for active employees.",
                "Summarise performance ratings and engagement scores for employees of interest."
            ],
            "tools": [binding("HROps - Get Employees")]
        },
        {
            "name": "Case Management",
            "objective": (
                "Review, analyse, and create HR cases covering employee relations, "
                "accommodations, compliance violations, performance issues, and integration "
                "exceptions. Support the full case lifecycle from triage to resolution."
            ),
            "instructions": [
                "To review cases: call the Get Cases tool and filter by status or severity "
                "based on the user's request.",
                "To create a case: extract type, title, employee ID, severity, and optional "
                "notes from the user's request, then call the Create Case tool.",
                "Summarise open cases by severity: list Critical cases first, then High.",
                "For each case presented, include the SLA date and flag any that are overdue.",
                "List the tasks and next steps attached to cases the user asks about.",
                "Recommend case types and severity levels if the user describes a situation "
                "without specifying them."
            ],
            "tools": [
                binding("HROps - Get Cases"),
                binding("HROps - Create Case")
            ]
        },
        {
            "name": "Compliance Monitoring",
            "objective": (
                "Monitor mandatory training completions, policy acknowledgements, and regulatory "
                "requirements across all departments. Identify overdue items, quantify risk "
                "exposure, and recommend remediation priorities."
            ),
            "instructions": [
                "Call the Compliance tool to retrieve all compliance tracking data.",
                "Summarise overdue items by department and employee.",
                "List the most critical overdue items (sort by days past due, descending).",
                "Identify departments with the highest compliance risk exposure.",
                "Recommend which items should be addressed first based on regulatory risk.",
                "Note any employees approaching upcoming compliance deadlines."
            ],
            "tools": [binding("HROps - Get Compliance")]
        },
        {
            "name": "Integration Health & Data Reconciliation",
            "objective": (
                "Monitor the health of all HR system integrations (Workday, ADP, Benefitfocus, "
                "Lattice, Glint), identify sync errors and data discrepancies, and support "
                "data reconciliation between systems."
            ),
            "instructions": [
                "Call the Integrations tool to retrieve sync status for all five systems.",
                "Highlight any integrations with Error or Warning status.",
                "List specific field-level discrepancies (e.g. salary mismatches, status "
                "conflicts) and which employees are affected.",
                "Report the last successful sync timestamp for each integration.",
                "Summarise total error counts across all integrations.",
                "Recommend reconciliation actions for the most severe discrepancies."
            ],
            "tools": [binding("HROps - Get Integrations")]
        },
        {
            "name": "Operations Monitoring (Tasks, Notifications & Audit)",
            "objective": (
                "Monitor the HR operations task queue, review system notifications, and "
                "audit the activity log to support operational oversight and accountability."
            ),
            "instructions": [
                "For task enquiries: call the Tasks tool and present overdue or high-severity "
                "tasks first; group by case where applicable.",
                "For notification enquiries: call the Notifications tool and summarise unread "
                "alerts by category and urgency.",
                "For audit enquiries: call the Audit Log tool and filter entries by the "
                "date range, action type, or employee specified by the user.",
                "Cross-reference tasks with cases when the user asks for a full case status.",
                "Flag any tasks past their due date as overdue with the number of days elapsed."
            ],
            "tools": [
                binding("HROps - Get Tasks"),
                binding("HROps - Get Notifications"),
                binding("HROps - Get Audit Log")
            ]
        }
    ]


def create_structured_agent(
    name: str,
    objective: str,
    tasks: List[Dict],
    personality: Dict,
    starters: List[str],
    dry_run: bool = False
) -> Dict:
    """
    Create the agent in STRUCTURED mode, including JSON input/output schemas.
    Structured mode makes the agent suitable for both natural-language and
    programmatic orchestration.
    """
    # Input schema: what the agent accepts
    input_schema_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type":    "object",
        "properties": {
            "query": {
                "type":        "string",
                "description": (
                    "Natural-language HR operations query, e.g. "
                    "'Show me critical open cases', 'Who are our high-risk employees in Sales?', "
                    "'What compliance items are overdue?'"
                )
            },
            "employee_id": {
                "type":        "string",
                "description": "Optional employee ID filter (e.g. E001) for employee-specific queries."
            },
            "department": {
                "type":        "string",
                "description": "Optional department filter (e.g. Engineering, Sales, HR)."
            },
            "case_id": {
                "type":        "string",
                "description": "Optional case ID filter (e.g. C-2024-001) for case-specific queries."
            },
            "severity": {
                "type":        "string",
                "description": "Optional severity filter: Low, Medium, High, Critical.",
                "enum":        ["Low", "Medium", "High", "Critical"]
            }
        },
        "required": ["query"]
    }

    # Output schema: what the agent returns
    output_schema_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type":    "object",
        "properties": {
            "summary": {
                "type":        "string",
                "description": "Human-readable summary of the HR operations findings."
            },
            "data": {
                "type":        "object",
                "description": "Structured HR data payload returned by the tools."
            },
            "priority_items": {
                "type":        "array",
                "description": "List of high-priority action items surfaced by the query.",
                "items": {
                    "type":       "object",
                    "properties": {
                        "title":    {"type": "string"},
                        "severity": {"type": "string"},
                        "category": {"type": "string"},
                        "due_date": {"type": "string"}
                    }
                }
            },
            "recommendations": {
                "type":        "array",
                "description": "Recommended next steps or actions for the HR professional.",
                "items":       {"type": "string"}
            }
        },
        "required": ["summary"]
    }

    # Validated Agent Garden API format for structured mode (discovered 2025-02):
    #   agent_mode         = "structured"
    #   input_schema_type  = "json"  (lowercase — NOT "JSON")
    #   input_schema       = plain JSON string (NOT a wrapped object)
    #   output_schema_type = "json"  (lowercase — NOT "JSON")
    #   output_schema      = plain JSON string
    #
    # IMPORTANT: structured mode does NOT accept personality_traits or
    # conversation_starters — these fields cause a 422 validation error.
    # Use conversational mode for agents that need those fields.
    payload = {
        "name":               name,
        "objective":          objective,
        "agent_mode":         "structured",
        "status":             "DRAFT",
        "tasks":              tasks,
        "input_schema_type":  "json",
        "input_schema":       json.dumps(input_schema_data),
        "output_schema_type": "json",
        "output_schema":      json.dumps(output_schema_data)
    }

    if dry_run:
        print("  DRY RUN - agent payload preview:")
        preview = {k: v for k, v in payload.items() if k not in ("tasks",)}
        preview["tasks_count"] = len(tasks)
        print(json.dumps(preview, indent=2))
        return {"data": {"id": "dry-run-agent-id", "agent_status": "DRAFT"}}

    url      = f"{AGENT_GARDEN_BASE_URL}/api/v1/agent-garden/agents"
    response = requests.post(url, headers=get_headers(), json=payload)

    if response.status_code != 200:
        print(f"  Structured mode failed ({response.status_code}): {response.text}", flush=True)
        # Fall back to conversational mode without schemas
        print("  Falling back to conversational mode...")
        payload.pop("input_schema",  None)
        payload.pop("output_schema", None)
        payload["agent_mode"] = "conversational"
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        print("  Fallback to conversational succeeded.")

    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Create HR Operations Console structured agent in Boomi Agent Garden"
    )
    parser.add_argument(
        "--atom-host",
        default=SERVER_BASE_URL.replace("https://", "").replace("http://", ""),
        help=f"Shared web server hostname (default: {SERVER_BASE_URL})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print config without calling the API"
    )
    args    = parser.parse_args()
    dry_run = args.dry_run

    # Build auth and base URL
    scheme   = "https" if not args.atom_host.startswith("http") else ""
    base_url = f"https://{args.atom_host}" if scheme else args.atom_host
    auth_hdr = build_basic_auth_header()

    print("=" * 65)
    print("  HR Operations Console Agent - Agent Garden Creator")
    print("=" * 65)
    print(f"  Base URL : {base_url}")
    print(f"  Auth     : Basic (SERVER_USERNAME:SERVER_TOKEN)")
    print(f"  Dry run  : {dry_run}")
    print("=" * 65)

    # ── Step 1: Create tools ─────────────────────────────────────────────────
    print(f"\nSTEP 1: Creating {len(TOOLS_CONFIG)} OpenAPI tools")
    tools = create_all_tools(base_url, auth_hdr, dry_run=dry_run)

    # ── Step 2: Build task definitions ───────────────────────────────────────
    print("\nSTEP 2: Building agent task definitions")
    tasks = build_agent_tasks(tools)
    print(f"  {len(tasks)} tasks configured")
    for t in tasks:
        print(f"    - {t['name']} ({len(t['tools'])} tool(s))")

    # ── Step 3: Create structured agent ──────────────────────────────────────
    agent_name = "HR Operations Console Agent"
    agent_objective = (
        "Help HR professionals quickly surface and act on operational data across "
        "the HR technology stack. Retrieve and analyse employee profiles, open cases, "
        "compliance requirements, integration health, and operational tasks using live "
        "data from Workday HRIS, ADP Payroll, Benefitfocus, Lattice, and Glint. "
        "Present findings with clear prioritisation, identify data discrepancies between "
        "systems, flag compliance risk, and support HR case creation and management."
    )

    conversation_starters = [
        "Show me the HR dashboard — what are the most urgent items right now?",
        "Which employees are at high risk of leaving and why?",
        "What compliance training items are overdue and how many days past due?",
        "Is our ADP Payroll integration healthy? What errors are open?",
        "Open a new High severity Employee Relations case for employee E003.",
        "What cases are currently in Critical status and what are the next steps?",
        "Show me all overdue tasks and who they're assigned to.",
    ]

    personality = {
        "voice_tone": "Professional",
        "creativity": 20,
        "clarity":    95
    }

    print(f"\nSTEP 3: Creating structured agent in Agent Garden")
    print(f"  Name: {agent_name}")

    result     = create_structured_agent(
        name        = agent_name,
        objective   = agent_objective,
        tasks       = tasks,
        personality = personality,
        starters    = conversation_starters,
        dry_run     = dry_run
    )

    if dry_run:
        print("\nDry run complete. No API calls were made.")
        return

    agent_data = result.get("data", result)
    agent_id   = agent_data["id"]
    mode       = agent_data.get("agent_mode", "unknown")

    print(f"  Agent created: {agent_id}")
    print(f"  Mode:          {mode}")
    print(f"  Status:        {agent_data.get('agent_status', 'DRAFT')}")

    # ── Step 4: Activate agent ───────────────────────────────────────────────
    print("\nSTEP 4: Activating agent")
    activate_agent(agent_id)
    print("  Agent activated!")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  DONE — Agent created and activated")
    print("=" * 65)
    print(f"  Agent ID   : {agent_id}")
    print(f"  Agent name : {agent_name}")
    print(f"  Agent mode : {mode}")
    print(f"  Tools      : {len(tools)}")
    print(f"  Tasks      : {len(tasks)}")
    print()
    print(f"  View in UI:")
    print(f"  https://platform.boomi.com/BoomiAI.html#/agents/{agent_id}")
    print()
    print("  Tools created:")
    for t in tools:
        print(f"    - {t['name']}")
        print(f"      ID:   {t['id']}")
        print(f"      Name: {t['unique_name']}")
    print()
    print("  NOTE: The 9 HR Ops API processes are deployed and Active, but the")
    print("  underlying Boomi atom uses apiType=advanced. The WSS endpoints")
    print("  (/ws/simple/...) require API Management (APIM) configuration in")
    print("  the Boomi GUI before the agent tools can call them successfully.")
    print("  See CLAUDE.md for the APIM setup steps.")


if __name__ == "__main__":
    main()

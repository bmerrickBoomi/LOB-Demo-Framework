#!/usr/bin/env python3
"""
Registrar Enrollment Portal Agent - Agent Garden Creator
=========================================================
Creates a structured Boomi Agent Garden agent that surfaces registrar and
enrollment data through 10 OpenAPI tools backed by Registrar-EnrollmentPortal
Boomi processes:

  GET  /ws/simple/getRegistrarDashboard            - KPIs, priority queue, term summary
  GET  /ws/simple/getRegistrarStudents             - Full student directory
  POST /ws/simple/queryRegistrarStudent            - Student 360 profile by ID
  GET  /ws/simple/getRegistrarEnrollmentRequests   - Add/drop request queue
  POST /ws/simple/createRegistrarEnrollmentRequest - Submit a new enrollment request
  POST /ws/simple/updateRegistrarEnrollmentStatus  - Approve, deny, or update a request
  GET  /ws/simple/getRegistrarCourses              - Course catalog with capacity data
  GET  /ws/simple/getRegistrarDeadlines            - Academic deadlines and compliance
  GET  /ws/simple/getRegistrarSystems              - Integration system health status
  GET  /ws/simple/getRegistrarNotifications        - Registrar notifications and alerts

The agent is created in STRUCTURED mode with JSON input/output schemas, making
it suitable for programmatic orchestration as well as natural-language interaction
via the Boomi Agent Garden UI.

Prerequisites:
  - Registrar-EnrollmentPortal Boomi processes deployed to the target environment
  - Shared web server or APIM configured on the atom to expose the WSS endpoints

Usage:
    python create-registrar-agent.py [--atom-host <host>] [--dry-run]

    --atom-host   Shared web server hostname (default: from SERVER_BASE_URL in .env)
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

# ── locate .env (workspace root, two levels up from scripts/) ─────────────────
SCRIPT_DIR     = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent.parent   # scripts → active-development → workspace root
env_path       = WORKSPACE_ROOT / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"Loaded .env from {env_path}")
else:
    load_dotenv()
    print("Warning: .env not found at workspace root, trying CWD fallback")

# ── add agent-garden-api.py to path ──────────────────────────────────────────
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

create_openapi_tool   = _mod.create_openapi_tool
install_tool          = _mod.install_tool
activate_agent        = _mod.activate_agent
get_headers           = _mod.get_headers
AGENT_GARDEN_BASE_URL = _mod.AGENT_GARDEN_BASE_URL

# ── Registrar API config ──────────────────────────────────────────────────────
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "https://c02-usa-east.integrate.boomi.com")
SERVER_USERNAME = os.getenv("SERVER_USERNAME", "")
SERVER_TOKEN    = os.getenv("SERVER_TOKEN", "")


def build_basic_auth_header() -> str:
    """Build a Basic auth header value from SERVER_USERNAME:SERVER_TOKEN."""
    creds = b64encode(f"{SERVER_USERNAME}:{SERVER_TOKEN}".encode()).decode()
    return f"Basic {creds}"


# ── Tool definitions ──────────────────────────────────────────────────────────
#
# Endpoint URL formula (from WSS operation XML):
#   lowercase(operationType) + SentenceCase(objectName)
#   e.g. operationType=GET, objectName=RegistrarDashboard → /ws/simple/getRegistrarDashboard
#   e.g. operationType=QUERY, objectName=RegistrarStudent → /ws/simple/queryRegistrarStudent
#   e.g. operationType=CREATE, objectName=RegistrarEnrollmentRequest → /ws/simple/createRegistrarEnrollmentRequest
#   e.g. operationType=UPDATE, objectName=RegistrarEnrollmentStatus → /ws/simple/updateRegistrarEnrollmentStatus
#
TOOLS_CONFIG = [
    {
        "name": "Registrar - Get Dashboard",
        "description": (
            "Retrieves the Registrar Enrollment Portal dashboard data for the current term "
            "(Spring 2025). Returns KPI metrics (active students, students with holds, "
            "academic probation count, pending add/drop requests, waitlisted students, "
            "overdue deadlines, system errors, courses at capacity), a prioritised action "
            "queue of the highest-urgency items requiring immediate registrar attention, "
            "enrollment breakdown by academic standing, and a list of upcoming deadlines. "
            "Use this as the starting point for any general registrar status query."
        ),
        "path":   "/ws/simple/getRegistrarDashboard",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name": "Registrar - Get Students",
        "description": (
            "Retrieves the full student directory for the current term. Each student record "
            "includes: student ID, name, email, academic program, level (Freshman/Sophomore/"
            "Junior/Senior), GPA, academic standing (Good Standing or Academic Probation), "
            "advisor name, credits completed, credits in progress, total credits required, "
            "active holds (Financial, Academic, Immunization, Background Check, Graduation "
            "Clearance), and list of enrolled course IDs. Use this to find students, filter "
            "by program or standing, or identify students with active holds."
        ),
        "path":   "/ws/simple/getRegistrarStudents",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name": "Registrar - Query Student",
        "description": (
            "Retrieves a full 360-degree student profile by student ID. Returns all student "
            "details including current enrollment with course schedules, complete academic "
            "history by term (courses taken, credits, GPA), enrollment request history, "
            "active holds with details, advisor notes, and degree progress percentage. "
            "Use this when a student ID is known and deep profile data is required — "
            "after calling Get Students to identify the student ID, or when the user "
            "provides a specific student ID directly."
        ),
        "path":   "/ws/simple/queryRegistrarStudent",
        "method": "POST",
        "input_parameters": [
            {
                "name":        "studentId",
                "type":        "string",
                "required":    True,
                "description": (
                    "The student ID to look up (e.g. STU-001). Obtain from the Get Students "
                    "tool if not already known."
                )
            }
        ],
    },
    {
        "name": "Registrar - Get Enrollment Requests",
        "description": (
            "Retrieves all enrollment add/drop/waitlist requests for the current term. "
            "Each request includes: request ID, student ID and name, course ID and name, "
            "request type (Add, Drop, or Waitlist), current status (Pending Review, Blocked, "
            "Approved, Denied, or Waitlisted), waitlist position if applicable, submission "
            "date, and processing notes explaining any blocks or conditions. Requests are "
            "grouped with a summary count of needs-action, approved, and waitlisted. "
            "Use this to review the add/drop queue and identify requests requiring action."
        ),
        "path":   "/ws/simple/getRegistrarEnrollmentRequests",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name": "Registrar - Create Enrollment Request",
        "description": (
            "Submits a new course enrollment request (add, drop, or waitlist) on behalf of "
            "a student. Use this when the user wants to enroll a student in a course, drop "
            "a course, or add a student to a waitlist. Returns a confirmation with the new "
            "request ID and initial status. Note: requests for students with active holds "
            "will be created with Blocked status."
        ),
        "path":   "/ws/simple/createRegistrarEnrollmentRequest",
        "method": "POST",
        "input_parameters": [
            {
                "name":        "studentId",
                "type":        "string",
                "required":    True,
                "description": "Student ID submitting the request (e.g. STU-001)."
            },
            {
                "name":        "courseId",
                "type":        "string",
                "required":    True,
                "description": "Course ID to add, drop, or waitlist (e.g. CS-401)."
            },
            {
                "name":        "courseName",
                "type":        "string",
                "required":    True,
                "description": "Full course name (e.g. Advanced Algorithms)."
            },
            {
                "name":        "type",
                "type":        "string",
                "required":    True,
                "description": "Request type. Must be one of: Add, Drop, Waitlist."
            },
            {
                "name":        "notes",
                "type":        "string",
                "required":    False,
                "description": "Optional notes or reason for the enrollment request."
            }
        ],
    },
    {
        "name": "Registrar - Update Enrollment Status",
        "description": (
            "Updates the status of an existing enrollment request — for example, approving "
            "or denying a pending add/drop request. Use this after reviewing a Blocked or "
            "Pending Review request and determining the appropriate action. Returns the "
            "updated request with new status, timestamp, and the registrar who made the change."
        ),
        "path":   "/ws/simple/updateRegistrarEnrollmentStatus",
        "method": "POST",
        "input_parameters": [
            {
                "name":        "requestId",
                "type":        "string",
                "required":    True,
                "description": "Enrollment request ID to update (e.g. ENR-004)."
            },
            {
                "name":        "status",
                "type":        "string",
                "required":    True,
                "description": (
                    "New status. Must be one of: Approved, Denied, Pending Review, Blocked."
                )
            },
            {
                "name":        "notes",
                "type":        "string",
                "required":    False,
                "description": "Notes about the decision or reason for the status change."
            }
        ],
    },
    {
        "name": "Registrar - Get Courses",
        "description": (
            "Retrieves the full course catalog for the current term. Each course record "
            "includes: course ID, name, department, credit hours, enrolled count, capacity, "
            "waitlist count, instructor, schedule (days and times), room assignment, "
            "prerequisite course IDs, and availability status (Open or Full). "
            "Use this to check enrollment capacity, identify full courses with waitlists, "
            "verify prerequisites, or provide course scheduling information to a student."
        ),
        "path":   "/ws/simple/getRegistrarCourses",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name": "Registrar - Get Deadlines",
        "description": (
            "Retrieves all academic deadlines and compliance milestones for the current term. "
            "Deadlines are categorised as Overdue (with days-past-due) or Upcoming (with "
            "days-until). Categories include: Enrollment (add/drop and withdrawal), Graduation "
            "(application submission), Grading (faculty grade submission), Registration "
            "(next-term opens), Compliance (FERPA training), and Financial Aid certification. "
            "Each deadline includes its impact statement explaining what happens if missed. "
            "Use this to identify urgent compliance items and report on upcoming action dates."
        ),
        "path":   "/ws/simple/getRegistrarDeadlines",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name": "Registrar - Get Systems",
        "description": (
            "Retrieves the health and sync status of all five integrated systems in the "
            "Registrar technology stack: Banner SIS (core student record system), Oracle "
            "Student Cloud (degree audit and records), Financial Aid System (aid eligibility "
            "and disbursement), Canvas LMS (course rosters), and Housing and Meal Plans. "
            "Each system record includes: status (healthy, warning, or error), last sync "
            "timestamp, error count, and detailed error records with field-level discrepancies, "
            "severity (critical, high, medium), and recommended resolution steps. "
            "Use this to diagnose data integrity issues, identify sync failures, and "
            "surface critical integration errors requiring immediate attention."
        ),
        "path":   "/ws/simple/getRegistrarSystems",
        "method": "GET",
        "input_parameters": [],
    },
    {
        "name": "Registrar - Get Notifications",
        "description": (
            "Retrieves the registrar notification feed. Notifications cover: financial aid "
            "certification alerts, enrollment deadline warnings, FERPA compliance reminders, "
            "integration sync errors, student graduation milestone alerts, and system status "
            "updates. Each notification includes: ID, title, timestamp, human-readable time "
            "label, severity (critical, high, medium, low), category, and read status. "
            "Use this to surface urgent unread alerts for the registrar's immediate attention."
        ),
        "path":   "/ws/simple/getRegistrarNotifications",
        "method": "GET",
        "input_parameters": [],
    },
]


def create_all_tools(base_url: str, auth_header: str, dry_run: bool = False) -> List[Dict]:
    """Create and install all 10 Registrar OpenAPI tools. Returns created tool records."""
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

        # Build per-tool kwargs
        kwargs = dict(
            name           = cfg["name"],
            description    = cfg["description"],
            base_url       = base_url,
            path           = cfg["path"],
            method         = cfg["method"],
            headers        = [{"name": "Authorization", "static_value": auth_header}],
            authentication = {
                "type":        "token_auth",
                "token":       auth_header,
                "header_name": "Authorization"
            },
        )

        if cfg["input_parameters"]:
            kwargs["input_parameters"] = cfg["input_parameters"]

        # POST tools: build a JSON request body template from input parameters
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
    """Map tools to structured agent tasks covering key registrar workflows."""
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
            "name": "Enrollment Dashboard & Priority Queue",
            "objective": (
                "Retrieve the registrar dashboard to surface key performance indicators for "
                "the current term, identify the highest-priority items requiring immediate "
                "registrar attention, and provide a quick status snapshot of enrollment health, "
                "compliance posture, and system integrity."
            ),
            "instructions": [
                "Call the Dashboard tool to retrieve the current term's KPI summary.",
                "Report key metrics: active students, students with holds, students on academic "
                "probation, pending add/drop requests, waitlisted students, overdue deadlines, "
                "and system errors.",
                "Present the priority queue items sorted by severity (Critical first, then High).",
                "Summarise enrollment by academic standing (Good Standing vs Academic Probation).",
                "List the next three upcoming deadlines and flag any that are within 7 days.",
                "Also call Get Notifications and surface any unread critical or high-severity alerts.",
                "Flag any metric that exceeds normal thresholds — e.g. more than 3 students on "
                "probation, more than 5 pending requests, or any critical system errors."
            ],
            "tools": [
                binding("Registrar - Get Dashboard"),
                binding("Registrar - Get Notifications")
            ]
        },
        {
            "name": "Student 360 Profile Lookup",
            "objective": (
                "Look up student profiles and provide comprehensive academic information including "
                "enrollment status, GPA, degree progress, academic history, active holds, and "
                "advisor notes. Support queries about individual students or filtered groups "
                "across the student directory."
            ),
            "instructions": [
                "If the user provides a student name or partial name: call Get Students and "
                "search for the matching student to obtain their student ID.",
                "If the user provides a student ID directly: call Query Student with that ID "
                "to retrieve the full 360 profile.",
                "For general roster queries (e.g. 'students on probation', 'students with holds', "
                "'Computer Science juniors'): call Get Students and filter the results.",
                "For a full student profile: call Query Student with the resolved student ID and "
                "present: GPA with color-coded standing, degree progress percentage, current "
                "courses with schedules, term-by-term academic history, active holds with "
                "descriptions, and advisor notes.",
                "Flag any students with multiple holds, GPA below 2.5, or graduation clearance pending.",
                "If a student has holds, explain each hold type and what office needs to clear it."
            ],
            "tools": [
                binding("Registrar - Get Students"),
                binding("Registrar - Query Student")
            ]
        },
        {
            "name": "Enrollment Request Management",
            "objective": (
                "Review, process, create, and update course enrollment requests. Support the "
                "full add/drop workflow including approving blocked requests, managing the "
                "waitlist queue, and submitting new enrollment requests on behalf of students."
            ),
            "instructions": [
                "To review the request queue: call Get Enrollment Requests and summarise by "
                "status — present Blocked and Pending Review requests first as they need action.",
                "For each blocked request, explain the reason for the block and what is needed "
                "to resolve it (e.g. which hold needs clearing, which office to contact).",
                "To approve or deny a specific request: extract the request ID and new status "
                "from the user's instruction, then call Update Enrollment Status.",
                "To submit a new add/drop/waitlist request: collect studentId, courseId, "
                "courseName, and type (Add/Drop/Waitlist) from the user, then call "
                "Create Enrollment Request and return the confirmation.",
                "When reporting waitlisted students, include their position in the waitlist queue.",
                "Cross-reference with Get Students to check for holds before approving requests — "
                "warn the user if the student has an active hold that blocks enrollment.",
                "Summarise the add/drop deadline status so the user knows if a late override fee applies."
            ],
            "tools": [
                binding("Registrar - Get Enrollment Requests"),
                binding("Registrar - Create Enrollment Request"),
                binding("Registrar - Update Enrollment Status"),
                binding("Registrar - Get Students")
            ]
        },
        {
            "name": "Course Catalog & Availability",
            "objective": (
                "Provide information about Spring 2025 course offerings including enrollment "
                "capacity, waitlist status, scheduling, prerequisites, and instructor assignments. "
                "Help the registrar and students understand course availability and identify "
                "sections with capacity constraints."
            ),
            "instructions": [
                "Call Get Courses to retrieve the full course catalog.",
                "For a general catalog query: list all courses grouped by department, showing "
                "enrollment vs capacity and availability status (Open or Full).",
                "For a capacity analysis: identify all courses at or near capacity (80%+ full) "
                "and list those with active waitlists sorted by waitlist length.",
                "For a specific course lookup: filter by course ID or name and return full "
                "details including schedule, room, instructor, prerequisites, and current enrollment.",
                "If the user asks about course availability for a specific student: cross-reference "
                "with Query Student to verify the student meets prerequisites.",
                "Present enrollment fill rate as a percentage alongside enrolled/capacity counts.",
                "Flag any course that is full (100% capacity) and has a non-zero waitlist as "
                "potentially requiring a section expansion decision."
            ],
            "tools": [
                binding("Registrar - Get Courses"),
                binding("Registrar - Query Student")
            ]
        },
        {
            "name": "Academic Deadlines & Compliance",
            "objective": (
                "Monitor and report on academic calendar deadlines and compliance requirements "
                "for the current term. Identify overdue items, quantify impact, and surface "
                "upcoming deadlines requiring registrar or faculty action."
            ),
            "instructions": [
                "Call Get Deadlines to retrieve all academic calendar milestones.",
                "Lead with overdue items — sort by days-past-due (descending) and explain "
                "the operational impact of each missed deadline.",
                "For each overdue deadline, state the category, how many days past due it is, "
                "and the specific impact (e.g. number of affected students or faculty).",
                "List upcoming deadlines in chronological order, highlighting any within 14 days "
                "as urgent.",
                "Group deadlines by category: Enrollment, Graduation, Grading, Registration, "
                "Compliance, and Financial Aid.",
                "For FERPA compliance deadlines: note how many faculty members are non-compliant.",
                "For Financial Aid deadlines: identify how many students' disbursements are at risk.",
                "Recommend immediate actions for the most critical overdue items."
            ],
            "tools": [
                binding("Registrar - Get Deadlines")
            ]
        },
        {
            "name": "Integration System Health",
            "objective": (
                "Monitor the health of all five integrated systems in the Registrar technology "
                "stack (Banner SIS, Oracle Student Cloud, Financial Aid System, Canvas LMS, "
                "Housing and Meal Plans). Identify sync failures, data discrepancies, and "
                "integration errors requiring remediation."
            ),
            "instructions": [
                "Call Get Systems to retrieve the integration health dashboard.",
                "Lead with any systems in Error status, then Warning status, then Healthy.",
                "For each system with errors: list each error record including type, affected "
                "field, severity, specific description (including affected student IDs where "
                "present), and recommended resolution steps.",
                "Summarise the total error count across all systems and break down by severity "
                "(critical, high, medium).",
                "Report the last successful sync timestamp for each system.",
                "Flag the Financial Aid System as highest priority if it shows critical errors "
                "involving student aid disbursement.",
                "For Banner SIS errors: note that Banner is the source of record and downstream "
                "systems should be updated to match Banner data.",
                "Recommend which integration errors should be escalated vs resolved by the registrar."
            ],
            "tools": [
                binding("Registrar - Get Systems")
            ]
        }
    ]


def create_structured_agent(
    name: str,
    objective: str,
    tasks: List[Dict],
    dry_run: bool = False
) -> Dict:
    """
    Create the agent in STRUCTURED mode with JSON input/output schemas.
    Structured mode makes the agent suitable for both natural-language and
    programmatic orchestration.

    NOTE: structured mode does NOT accept personality_traits or
    conversation_starters — these cause a 422 validation error.
    """
    input_schema_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type":    "object",
        "properties": {
            "query": {
                "type":        "string",
                "description": (
                    "Natural-language registrar query, e.g. 'Show me the enrollment dashboard', "
                    "'Which students have active financial holds?', "
                    "'Approve enrollment request ENR-004', "
                    "'What courses are at full capacity?'"
                )
            },
            "student_id": {
                "type":        "string",
                "description": "Optional student ID filter (e.g. STU-001) for student-specific queries."
            },
            "course_id": {
                "type":        "string",
                "description": "Optional course ID filter (e.g. CS-401) for course-specific queries."
            },
            "request_id": {
                "type":        "string",
                "description": "Optional enrollment request ID (e.g. ENR-004) for request-specific actions."
            },
            "status": {
                "type":        "string",
                "description": "Optional status filter for enrollment requests.",
                "enum":        ["Pending Review", "Blocked", "Approved", "Denied", "Waitlisted"]
            },
            "program": {
                "type":        "string",
                "description": "Optional academic program filter (e.g. Computer Science, Nursing)."
            }
        },
        "required": ["query"]
    }

    output_schema_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type":    "object",
        "properties": {
            "summary": {
                "type":        "string",
                "description": "Human-readable summary of the registrar findings or action taken."
            },
            "data": {
                "type":        "object",
                "description": "Structured registrar data payload returned by the tools."
            },
            "priority_items": {
                "type":        "array",
                "description": "High-priority action items surfaced by the query.",
                "items": {
                    "type":       "object",
                    "properties": {
                        "title":    {"type": "string"},
                        "severity": {"type": "string"},
                        "category": {"type": "string"},
                        "due":      {"type": "string"}
                    }
                }
            },
            "recommendations": {
                "type":        "array",
                "description": "Recommended next steps or actions for the registrar.",
                "items":       {"type": "string"}
            },
            "action_result": {
                "type":        "object",
                "description": "Result of a create or update action (enrollment request, status change).",
                "properties": {
                    "success": {"type": "boolean"},
                    "message": {"type": "string"},
                    "id":      {"type": "string"}
                }
            }
        },
        "required": ["summary"]
    }

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
        preview = {k: v for k, v in payload.items() if k not in ("tasks", "input_schema", "output_schema")}
        preview["tasks_count"] = len(tasks)
        print(json.dumps(preview, indent=2))
        return {"data": {"id": "dry-run-agent-id", "agent_status": "DRAFT", "agent_mode": "structured"}}

    url      = f"{AGENT_GARDEN_BASE_URL}/api/v1/agent-garden/agents"
    response = requests.post(url, headers=get_headers(), json=payload)

    if response.status_code != 200:
        print(f"  Structured mode failed ({response.status_code}): {response.text}", flush=True)
        # Fall back to conversational mode
        print("  Falling back to conversational mode...")
        payload.pop("input_schema_type",  None)
        payload.pop("input_schema",       None)
        payload.pop("output_schema_type", None)
        payload.pop("output_schema",      None)
        payload["agent_mode"] = "conversational"
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        print("  Fallback to conversational succeeded.")

    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Create Registrar Enrollment Portal structured agent in Boomi Agent Garden"
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
    print("  Registrar Enrollment Portal Agent - Agent Garden Creator")
    print("=" * 65)
    print(f"  Base URL : {base_url}")
    print(f"  Auth     : Basic (SERVER_USERNAME:SERVER_TOKEN)")
    print(f"  Dry run  : {dry_run}")
    print("=" * 65)

    # ── Step 1: Create tools ──────────────────────────────────────────────────
    print(f"\nSTEP 1: Creating {len(TOOLS_CONFIG)} OpenAPI tools")
    tools = create_all_tools(base_url, auth_hdr, dry_run=dry_run)

    # ── Step 2: Build task definitions ───────────────────────────────────────
    print("\nSTEP 2: Building agent task definitions")
    tasks = build_agent_tasks(tools)
    print(f"  {len(tasks)} tasks configured")
    for t in tasks:
        print(f"    - {t['name']} ({len(t['tools'])} tool(s))")

    # ── Step 3: Create structured agent ──────────────────────────────────────
    agent_name = "Registrar Enrollment Portal Agent"
    agent_objective = (
        "Help university registrars quickly surface and act on enrollment data across "
        "the academic term. Retrieve and analyse student records, manage add/drop and "
        "waitlist requests, monitor course capacity, track academic deadlines and "
        "compliance requirements, and diagnose integration health issues across Banner SIS, "
        "Oracle Student Cloud, Financial Aid, Canvas LMS, and Housing systems. "
        "Present findings with clear prioritisation, identify students with holds or academic "
        "concerns, flag overdue compliance items, and support enrollment request creation "
        "and approval workflows — all grounded in live data from the Registrar portal APIs."
    )

    print(f"\nSTEP 3: Creating structured agent in Agent Garden")
    print(f"  Name: {agent_name}")

    result = create_structured_agent(
        name      = agent_name,
        objective = agent_objective,
        tasks     = tasks,
        dry_run   = dry_run
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

    # ── Step 4: Activate agent ────────────────────────────────────────────────
    print("\nSTEP 4: Activating agent")
    activate_agent(agent_id)
    print("  Agent activated!")

    # ── Summary ───────────────────────────────────────────────────────────────
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
        print(f"      Unique name: {t['unique_name']}")
    print()
    print("  Endpoints (base URL + path):")
    for cfg in TOOLS_CONFIG:
        print(f"    {cfg['method']:4s}  {cfg['path']}")


if __name__ == "__main__":
    main()

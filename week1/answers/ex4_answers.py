"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "It seems there are currently no Edinburgh venues available that can accommodate 300 people with vegan options. You might want to lower the capacity requirement or revisit the constraints."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changing The Albanach from available to full only required editing
`sovereign_agent/tools/mcp_venue_server.py`. After rerunning the client,
Query 1's search results dropped from two matches to one, so The Haymarket
Vaults became the only candidate. The discovered tool list did not change,
the client code did not change, and Query 2 still returned no matches for
300 guests. After the test, I reverted the server file.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 302
LINES_OF_TOOL_CODE_EX4 = 291

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP buys you a shared contract, not just separation. The LangGraph client
can discover tools dynamically, and another client such as the Rasa side
can reuse the same server without copying venue logic. When the venue data
changed in the experiment, I updated one server file and both clients would
see the new truth automatically.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner is a strong-reasoning model upstream of the autonomous loop that turns Rod's vague request into ordered subgoals before the executor starts.
- The Executor grows out of `sovereign_agent/agents/research_agent.py` and lives in the autonomous-loop half, where it performs ReAct-style tool use against venue, weather, and later web-search tasks.
- The Shared MCP Tool Server grows out of `sovereign_agent/tools/mcp_venue_server.py` and lives in the shared layer, exposing venue lookup and later calendar, email, and search tools to both halves.
- The Structured Confirmation Agent grows out of `exercise3_rasa/` and lives in the structured-agent half, where it handles pub-manager calls through explicit flows and deterministic business rules.
- The Handoff Bridge lives between the two halves and routes work from the executor to the structured agent when a human confirmation call is needed, then passes control back afterward.
- The Memory Layer lives alongside the autonomous half and the shared layer, storing prior research, retrieved venue context, and longer-term state so PyNanoClaw does not restart every task from zero.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph agent is the right agent for research because I watched it in
Exercise 2 sequence venue checks, weather, catering, and flyer generation
without being scripted step by step, and it handled impossible or
out-of-scope questions by reasoning over what tools existed. The Rasa CALM
agent is the right agent for the phone call because in Exercise 3 it
collected slots in order, enforced the deposit rule deterministically, and
deflected the parking request through a named out-of-scope flow. Swapping
them feels wrong because LangGraph is too improvisational for binding
confirmation logic, while CALM is too rigid for open-ended research.
"""

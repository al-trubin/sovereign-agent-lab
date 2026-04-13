"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
You: calling to confirm a booking
Bot: How many guests are you confirming for tonight's event?
You: 160 guests
Bot: And how many of those guests will need vegan meals?
You: about 50 need vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
You: £200 deposit
Bot: Thank you — booking confirmed. 160 guests, 50 requiring vegan meals,
£200 deposit accepted. I'll send written confirmation to the organiser
shortly.
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
You: calling to confirm a booking
Bot: How many guests are you confirming for tonight's event?
You: 160 guests
Bot: And how many of those guests will need vegan meals?
You: 50 vegan
Bot: What deposit amount in GBP are you proposing to secure the booking?
You: £500 deposit
Bot: I need to check one thing with the organiser before I can confirm. The
issue is: a deposit of £500 exceeds the organiser's authorised limit of
£300. Can I call you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "A deposit of £500 exceeded the organiser's authorised limit of £300."

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
You: calling to confirm a booking
Bot: How many guests are you confirming for tonight's event?
You: 160 guests
Bot: And how many of those guests will need vegan meals?
You: can you arrange parking for the speakers?
Bot: I can only help with confirming tonight's venue booking. For anything
else, please contact the event organiser directly.
Bot: Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM switched into the out-of-scope handling path, refused the parking
request cleanly, and then explicitly offered to continue the booking flow
instead of losing the conversation state.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa CALM handled the parking request more structurally than LangGraph did
in Exercise 2 Scenario 3. CALM routed to a dedicated out-of-scope flow,
gave a fixed policy answer, and then asked whether to continue the booking.
LangGraph also stayed safe, but it simply admitted it lacked a train tool
and suggested websites rather than preserving a controlled workflow.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I uncommented the guard, retrained the model, and ran the three normal
conversations. Then I temporarily changed the condition to `if True`,
retrained again, restarted the action server, completed one confirmation
flow, observed the explicit 16:45 cutoff escalation message, and finally
reverted the code and retrained.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
CALM removes a lot of glue code because the LLM now handles intent
selection and slot extraction from natural language, which old Rasa made
you express through training examples, rules, and regex-heavy validation
helpers. Python still owns the binding business rules, which is correct for
deposit limits, capacity ceilings, and time cutoffs. The tradeoff is that
the LLM layer is more flexible but also less transparent than old fully
symbolic parsing.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The extra setup buys you predictability. CALM is harder to boot than the
LangGraph loop because it needs config files, training, an action server,
and a licence, but in return you get an auditable path for a high-stakes
phone call. It cannot freely improvise across arbitrary tools the way the
research agent can, and for confirmation work that limitation is mostly a
feature rather than a bug.
"""

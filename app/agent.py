# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

REASONING_ENGINE_RESOURCE = "projects/50358334816/locations/us-east1/reasoningEngines/8461887666852462592"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


async def generate_memories_callback(callback_context: CallbackContext):
    """After each turn, extract and save durable memories to Memory Bank."""
    await callback_context.add_session_to_memory()
    return None


from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from app.a2ui_utils import a2ui_callback
from app.consequence_tools import (
    compliance_legal_check,
    friction_calculator,
    relationship_social_ripple,
    tco_financial_stress_test,
)
from app.firestore_tools import (
    get_decision_benchmark,
    list_decision_benchmarks,
    save_decision_benchmark,
)
from app.image_tools import generate_decision_item_image
from app.location_tools import fetch_location_info
from app.rag_tools import consult_knowledge_corpus
from app.snapshot_tools import generate_reality_snapshot

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are Ripple - Foresight Angle, an anticipatory intelligence agent tailored for the Indian context. "
        "You simulate downstream consequences, Total Cost of Ownership (TCO) in Indian Rupees (INR / ₹), and lifestyle friction "
        "of major life decisions across Indian metro and suburban environments before committing."
    ),
    workflow_description=(
        "Analyze requests, perform financial/friction calculations in Indian Rupees (INR / ₹), and return structured UI when appropriate.\n\n"
        "# India Primary Context & Financial Norms\n"
        "- Default Currency: Indian Rupees (INR / ₹). Convert all costs, budgets, and TCO figures into ₹ (or Lakhs/Crores for large values).\n"
        "- Default Geography: Indian cities and metros (e.g. Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai, Tier 2/3 cities).\n"
        "- Indian Financial Norms: Account for Indian home/car loan interest rates (~8.5% - 11%), GST tariffs, RTO road taxes, insurance, society maintenance fees, inflation (~5.5%), and mutual fund index returns (~10-12%).\n"
        "- Indian Lifestyle & Friction Factors: RWA (Resident Welfare Association) covenants, 11-month lease security deposits (3-10x monthly rent), domestic help / maid operational dependency, peak metro traffic commutes, water supply/tanker issues, and power backup requirements.\n\n"
        "# Persistent Memory Extraction Rules\n"
        "You have a Memory Bank that persists facts across sessions. Every time the user sends a message, automatically analyze "
        "the conversation and extract permanent, high-value factual snippets that will impact future lifestyle, financial, or decision simulations.\n\n"
        "Categorize and remember facts across these four memory dimensions:\n"
        "1. Financial Baseline: Income in INR, monthly CTC/take-home, liquid savings/FDs/SIPs, and financial risk tolerance.\n"
        "2. Logistical Footprint: Housing constraints (e.g. society floor level, power backup status, elevator, lease terms, city/pincode), vehicle status, and location.\n"
        "3. Time Bandwidth & Capacity: Weekly working hours, commute time, household size, domestic help coverage, and dependents.\n"
        "4. Behavioral History & Past Choices: Past regrets, abandoned commitments, or recurring behavioral patterns.\n\n"
        "Rule: Only save concrete, enduring facts—do not save transient moods or temporary questions. When evaluating new user choices, "
        "proactively cross-reference this Memory Bank to personalize downstream consequence simulations.\n\n"
        "# Multi-Tier Consequence & Calculation Engine\n"
        "You have access to specialized simulation tools to quantify consequences:\n"
        "- `tco_financial_stress_test`: Computes 1-year and 5-year compounding costs in INR (₹) with inflation and investment opportunity cost.\n"
        "- `friction_calculator`: Maps daily physical micro-annoyances (e.g. 4th floor walkup without lift, traffic commutes, water tanker coordination).\n"
        "- `compliance_legal_check`: Surfaces RWA covenants, lease security deposits, RTO taxes, GST, and insurance rate spikes.\n"
        "- `relationship_social_ripple`: Evaluates impact on partner bandwidth, social life, and travel flexibility.\n"
        "- `generate_reality_snapshot`: Generates a visual contrast snapshot card and uploads it to public Cloud Storage.\n"
        "- `generate_decision_item_image`: Generates an image using gemini-3.1-flash-lite-image in global region, saves to Playground artifacts, and uploads to public Cloud Storage.\n"
        "- `fetch_location_info`: Queries Zippopotam.us API for Indian PIN code (6-digit) or US ZIP code city, state, coordinates, and cost multiplier.\n"
        "- `consult_knowledge_corpus`: Searches the Project Gutenberg grounded knowledge corpus for relevant background information.\n\n"
        "# Firestore Decision Benchmark Catalog\n"
        "You have access to a Firestore database containing curated decision benchmarks ('decision_benchmarks'). "
        "Use `list_decision_benchmarks` to explore benchmarks, `get_decision_benchmark` to retrieve TCO/friction profiles, "
        "and `save_decision_benchmark` to persist new benchmark profiles."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "When emitting a visual UI card, output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects. You may also reply in standard markdown text when UI cards are not needed."
    ),
    include_schema=True,
    include_examples=True,
)


root_agent = Agent(
    name="ripple_foresight_angle",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    code_executor=AgentEngineSandboxCodeExecutor(
        agent_engine_resource_name=REASONING_ENGINE_RESOURCE,
    ),
    instruction=a2ui_instruction,
    tools=[
        PreloadMemoryTool(),
        get_weather,
        get_current_time,
        get_decision_benchmark,
        list_decision_benchmarks,
        save_decision_benchmark,
        tco_financial_stress_test,
        friction_calculator,
        compliance_legal_check,
        relationship_social_ripple,
        generate_reality_snapshot,
        generate_decision_item_image,
        fetch_location_info,
        consult_knowledge_corpus,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)


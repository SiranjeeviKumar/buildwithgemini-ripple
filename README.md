# Ripple — Foresight Angle
> *"Don't just make the choice. Simulate the ripple."*

Ripple is an anticipatory intelligence agent tailored for the Indian context. It helps decision-makers simulate the hidden 1-to-5-year downstream consequences, Total Cost of Ownership (TCO in INR / ₹), legal/compliance constraints, and lifestyle friction of major life decisions before committing.

![Ripple Demo](ripple_demo.gif)

---

## 🌟 What Ripple Does

When faced with major decisions—such as buying a car, relocating to a new city, adopting a pet, or switching careers—people often focus only on the upfront purchase price or immediate outcome. Ripple simulates multi-tier compounding consequences:

- **1st-Order Consequences**: Direct financial costs (upfront capital, monthly EMIs, deposit locks).
- **2nd-Order Consequences**: Operational friction & daily micro-annoyances (commutes, RWA rules, water tanker dependencies, domestic help gaps).
- **3rd-Order Consequences**: Long-term financial opportunity costs (compounding interest vs equity returns), social bandwidth, and career flexibility.

---

## 🛠️ Implemented Architecture & Google Cloud Services

Ripple is built with the **Agent Development Kit (ADK)** and integrates directly with Google Cloud Agent Platform services:

| Component / Service | Implementation File | Purpose & Functionality |
|---|---|---|
| **Vertex AI Memory Bank** | [`app/agent.py`](app/agent.py) | Persists user facts across sessions (`PreloadMemoryTool` & `generate_memories_callback`). Categorizes memories into Financial Baseline, Logistical Footprint, Time Capacity, and Behavioral History. |
| **Google Cloud Firestore** | [`app/firestore_tools.py`](app/firestore_tools.py) | Stores and queries curated decision benchmarks (`decision_benchmarks` collection). Provides `get_decision_benchmark`, `list_decision_benchmarks`, and `save_decision_benchmark`. |
| **Google Cloud Storage (GCS)** | [`app/image_tools.py`](app/image_tools.py) | Stores generated visual reality snapshots and product images in a public Cloud Storage bucket. |
| **Imagen Image Generation** | [`app/image_tools.py`](app/image_tools.py) | Uses Imagen (`gemini-3.1-flash-lite-image`) via Vertex AI / Google GenAI to render decision item visuals and scenario snapshots (`generate_decision_item_image`). |
| **Omni Video Generation** | [`app/video_tools.py`](app/video_tools.py) | Uses Google's Omni model (`gemini-omni-flash-preview`) in the `global` region to generate short decision videos (`generate_decision_item_video`), saves artifacts via `tool_context.save_artifact`, and uploads bytes to public Cloud Storage. |
| **Vertex AI RAG Engine** | [`app/rag_tools.py`](app/rag_tools.py) | Grounded retrieval-augmented generation (`consult_knowledge_corpus`) querying a Vertex AI RAG corpus. |
| **Agent Engine Code Executor** | [`app/agent.py`](app/agent.py) | Runs Python computations for 1-year and 5-year TCO curves, compounding inflation, and investment opportunity costs inside an isolated Agent Engine sandbox (`AgentEngineSandboxCodeExecutor`). |
| **A2UI Rendering Engine** | [`app/a2ui_utils.py`](app/a2ui_utils.py) | Generates structured A2UI v0.8 cards (`Card`, `Column`, `Row`, `Text`, `Image`) returned as data parts to display rich UI cards in chat interfaces. |
| **Location & PIN Code API** | [`app/location_tools.py`](app/location_tools.py) | Fetches city, state, location metadata, and regional cost multipliers for 6-digit Indian PIN codes via `fetch_location_info`. |
| **Consequence Engine** | [`app/consequence_tools.py`](app/consequence_tools.py) | Simulates TCO (`tco_financial_stress_test`), physical friction (`friction_calculator`), Indian compliance & RWA legal checks (`compliance_legal_check`), and social ripples (`relationship_social_ripple`). |
| **FastAPI Proxy & Web UI** | [`frontend/main.py`](frontend/main.py) | FastAPI proxy communicating via A2A protocol to Agent Engine, serving a responsive HTML5 chat UI (`frontend/static/index.html`). |

---

## 🇮🇳 India Context Customizations

- **Currency & Financial Metrics**: Calculates figures in Indian Rupees (INR / ₹), Lakhs, and Crores. Computes Indian home/car loan interest rates (~8.5–11%), GST tariffs, RTO road taxes, insurance premiums, society maintenance fees, and mutual fund SIP returns (~10–12%).
- **Regional Logistics**: Incorporates Resident Welfare Association (RWA) rules, 11-month lease security deposit locks (3–10x rent), maid/cook operational dependencies, peak traffic commutes, water supply/tanker coordination, and power backup requirements.
- **PIN Code Lookup**: Resolves 6-digit Indian PIN codes (e.g. `560001` for Bengaluru, `400001` for Mumbai, `600001` for Chennai).

---

## 🔮 Planned / Stretch Features (Not Yet Implemented in Code)

The following items from the initial design brief were conceptualized but are **not currently implemented** in the active codebase:

- ⏳ **Interactive Ripple Tree Flowchart**: An interactive D3 branching flowchart component for visual 1st/2nd/3rd order consequence trees (currently rendered as structured text and A2UI cards).
- ⏳ **Interactive Slider Cards**: Live slider components inside A2UI cards for real-time parameter tweaking (currently limited to static display cards supported by A2UI v0.8).

---

## 🚀 Local Development & Execution Setup

### Prerequisites

- Python 3.11+
- Node.js 18+ and `npm`
- Google Cloud SDK (`gcloud`) authenticated to your GCP Project

### 1. Installation

Clone the repository and install Python dependencies:

```bash
pip install -r app/requirements.txt
```

### 2. Environment Configuration

Set the required environment variables:

```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_REGION="us-east1"
```

### 3. Running the Agent Backend & Dev UI

Start the Agent Development Kit (ADK) local web server:

```bash
adk web --port 8000
```

### 4. Running the Web Frontend Proxy

Navigate to the `frontend/` directory, install dependencies, and start the FastAPI proxy:

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

---

## 📂 Repository Structure

```
.
├── README.md                  # Project documentation
├── ripple_demo.gif            # Looping demo recording preview
├── agents-cli-manifest.yaml   # Agent Engine deployment manifest
├── app/                       # Core ADK Agent implementation
│   ├── agent.py               # Root agent definition & A2UI prompt setup
│   ├── a2ui_utils.py          # A2UI callback and JSON card renderer
│   ├── consequence_tools.py   # TCO, friction, compliance & social tools
│   ├── firestore_tools.py     # Firestore decision benchmark catalog tools
│   ├── image_tools.py         # Imagen visual generation & GCS upload
│   ├── location_tools.py      # Indian PIN code lookup (Zippopotam.us)
│   ├── rag_tools.py           # Grounded RAG knowledge corpus retriever
│   └── snapshot_tools.py     # Visual reality snapshot generator
└── frontend/                  # Production chat web frontend
    ├── main.py                # FastAPI proxy wrapping A2A protocol
    └── static/
        └── index.html         # Responsive single-page chat application
```

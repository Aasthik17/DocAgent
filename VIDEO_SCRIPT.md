# DocAgent: 8–10 Minute Video Submission Script & Presentation Guide

This script is designed for you to deliver the video presentation for the **Python AI Engineer – Autonomous Agents – 60-Minute Build Challenge**.

---

## ⏱️ Video Structure Overview (Target: 8–10 Minutes)

| Section | Target Duration | Focus Area |
| :--- | :--- | :--- |
| **Part 1: Live Demo** | 3 – 4 min | End-to-end execution of Test Case 1 & Test Case 2 in UI, TODO task list, and Word documents |
| **Part 2: What You Built** | 2 – 3 min | Architecture walkthrough, FastAPI REST design, planning engine, tools, reflection gate, python-docx |
| **Part 3: Debugging Insight** | 1 – 2 min | Real problem faced: Role-intent collision in multi-stage LLM dispatch and how it was diagnosed |
| **Part 4: Tradeoff Discussion** | 1 – 2 min | Autonomous Planning vs. Deterministic Workflow & Single vs. Multi-Agent Orchestration |

---

## 🎬 Section-by-Section Spoken Script

### 0:00 – 0:45 | Introduction & Overview
> *"Hello! My name is [Your Name], and today I am presenting **DocAgent**, an autonomous AI agent system engineered for the 60-Minute Autonomous Agent Challenge.*
> 
> *The goal of DocAgent is to accept natural language document requests, autonomously deconstruct them, generate an ordered TODO execution plan, resolve missing or conflicting parameters by formulating explicit business assumptions, execute domain tools, perform self-reflection for quality assurance, and produce an executive-ready Microsoft Word (.docx) document via a production FastAPI REST API.*
> 
> *Let's jump straight into the live demo."*

---

### 0:45 – 4:00 | Part 1: Live Demo (3–4 Minutes)

#### Step 1: Launch & Interface
*(Show browser at `http://localhost:8000`)*
> *"Here we have the DocAgent interactive console served directly by our FastAPI application. We also have full OpenAPI Swagger documentation available at `/docs`.*
> 
> *Notice on the console that we have two preconfigured test cases: a standard business proposal and a complex ambiguous request."*

#### Step 2: Test Case 1 – Standard Proposal
*(Click "Test Case 1: Standard Proposal" and click "Run Autonomous Agent")*
> *"For our first test case, we submit a standard business request:*
> **'Create a formal Project Proposal for a Q3 Customer Onboarding Automation system at Acme Corp, including problem statement, proposed solution, timeline, budget, and risk mitigation.'**
> 
> *When we click 'Run Autonomous Agent', the agent doesn't just call a raw LLM prompt in a single shot. Instead, it initiates its multi-step lifecycle:*
> 1. *It identifies this as an Executive Project Proposal.*
> 2. *It formulates assumptions around KPIs—such as targeting an onboarding reduction from 28 days to under 7 days and a $35,000 budget cap.*
> 3. *It generates an execution plan with 6 discrete tasks, tracking each from PENDING to RUNNING to COMPLETED.*
> 4. *It synthesizes detailed sections and invokes domain tools for data modeling.*
> 5. *It passes through our mandatory engineering improvement—the **Reflection Quality Gate**—which evaluates the draft against 5 dimensions: constraint adherence, completeness, actionability, executive tone, and data consistency.*
> 
> *As you can see, the reflection gate awarded this draft a 95/100 score, confirming all budget and milestone numbers balance."*

#### Step 3: Inspect the Generated Word Document (.docx)
*(Click "Download Word Doc (.docx)" and open the downloaded document)*
> *"Let's open the generated document in Microsoft Word.*
> 
> *Notice the formatting quality:*
> - *Executive title block with metadata table (Date, Status, Classification, Audience).*
> - *Autonomous Assumptions Register clearly stating the operational bounds.*
> - *Custom corporate typography in deep navy and slate accents.*
> - *Executive Callout boxes with colored border styling highlighting strategic goals.*
> - *Formatted Data Tables with header shading, alternating zebra rows, and cell padding (showing the 12-week agile sprint breakdown and $35,000 budget).*
> - *Proper confidentiality notices in the header and footer.*
> 
> *This is an executive-ready document ready for C-suite review."*

#### Step 4: Test Case 2 – Complex & Ambiguous Request
*(Switch back to browser, click "Test Case 2: Complex & Ambiguous", and click "Run Autonomous Agent")*
> *"Now let's examine our second test case, designed specifically to test autonomous decision-making under ambiguous, conflicting constraints:*
> **'Draft a technical specification and rollout strategy for migrating our legacy monolith to microservices next month, but make sure it handles SOC2 compliance, team capacity constraints, and don't spend more than $50k on cloud infra, even though our CTO wants everything on Kubernetes and our lead architect wants serverless.'**
> 
> *Notice the severe conflicts here: a $50k budget constraint vs. a CTO demanding Kubernetes vs. a Lead Architect wanting serverless, with an aggressive timeline and SOC2 compliance.*
> 
> *Watch how DocAgent resolves this:*
> 1. *In the **Assumptions Register**, it autonomously negotiates the architectural compromise: it adopts a **hybrid container/serverless topology**, placing persistent core services on lightweight managed Kubernetes with Spot instances to satisfy the CTO, while routing event-driven functions to serverless to satisfy the Architect.*
> 2. *It models the infrastructure cost to verify the hybrid approach stays at $47,400/year, safely within the $50k ceiling.*
> 3. *It integrates SOC2 audit logging and HashiCorp Vault secrets from Phase 1.*
> 4. *It structures a 3-phase Strangler Fig rollout with automated rollback gates to prevent team burnout.*
> 
> *Let's download the generated technical specification .docx. You can see the Tradeoff Evaluation Matrix comparing Pure Kubernetes, Pure Serverless, and the Recommended Hybrid Solution, complete with annual costs and latency benchmarks."*

---

### 4:00 – 6:30 | Part 2: What You Built (2–3 Minutes)

*(Show code editor or architecture diagram in `README.md`)*
> *"Now let's review how this was engineered under the hood.*
> 
> *DocAgent is structured into five modular components:*
> 
> 1. **FastAPI REST API Layer (`app/main.py`)**:
>    - *Exposes `POST /agent` taking a JSON payload `{"request": "..."}`.*
>    - *Streams generated documents via `GET /download/{doc_id}` using `FileResponse`.*
>    - *Provides interactive health diagnostics at `/health` and serves the UI console.*
> 
> 2. **Autonomous Planning Engine (`app/agent/planner.py`)**:
>    - *Deconstructs incoming prompts into document type, target audience, and explicit assumptions.*
>    - *Dynamically builds an `ExecutionPlan` consisting of structured `AgentTask` objects with assigned tools.*
> 
> 3. **Step-by-Step Task Executor & Tool Dispatcher (`app/agent/executor.py` & `app/agent/tools.py`)**:
>    - *Executes the plan sequentially, updating state transitions (`PENDING` ➔ `RUNNING` ➔ `COMPLETED`).*
>    - *Dispatches tools such as `research_tool` for compliance benchmarks, `table_generator_tool` for financial grids, and `assumption_resolver`.*
> 
> 4. **Mandatory Engineering Improvement: Reflection & Self-Check Gate (`app/agent/reflection.py`)**:
>    - *Why did I choose Reflection? Document generation often fails due to subtle omissions or ungrounded claims. Our reflection reviewer runs an explicit 5-point quality audit against constraint adherence, completeness, actionability, executive tone, and data consistency.*
>    - *If any check fails or the score is below 85, an autonomous self-correction loop refines the sections before document rendering.*
> 
> 5. **Polished Word Document Builder (`app/document/builder.py`)**:
>    - *Built on `python-docx` with direct OpenXML manipulation for cell margins (`w:tcMar`), background shading (`w:shd`), left accent borders (`w:tcBorders`), repeating table headers (`w:tblHeader`), and custom RGB typography.*
> 
> 6. **LLM Provider Flexibility (`app/llm/client.py`)**:
>    - *Supports Groq (Llama 3.3 70B), Google Gemini (2.5 Flash), and a deterministic Local Autonomous Reasoning Engine so the system is fully testable and runnable without API costs or rate-limit surprises."*

---

### 6:30 – 8:00 | Part 3: Debugging Insight (1–2 Minutes)

> *"Let me share a real engineering bug I diagnosed and resolved during development.*
> 
> *During the transition between multi-stage agent reasoning, our LLM client abstraction uses role-based system prompts: the `Chief Planning Officer` for task planning, the `Principal Content Architect` for section drafting, and the `Quality Assurance Reviewer` for reflection.*
> 
> *Initially, I used naive keyword detection where any prompt containing the word `'plan'` triggered the planning routine. However, the Content Architect's prompt read: 'Given the document plan and assumptions, draft the sections.' Because the word 'plan' was in that prompt, the dispatcher mistakenly invoked the planner instead of the section synthesizer!*
> 
> *As a result, the section synthesis step returned an empty list of narrative sections, and the document generated with only title metadata.*
> 
> *To fix this, I replaced loose keyword checks with explicit role-identity matching (`'chief planning officer'`, `'content architect'`, `'quality assurance'`) and isolated the user's raw prompt from the orchestration framing.*
> 
> *Once corrected, the full 5-section narrative with embedded tradeoff tables rendered cleanly. Catching this reinforced the importance of strict schema routing and defensive prompt isolation in multi-stage autonomous workflows."*

---

### 8:00 – 9:30 | Part 4: Tradeoff Discussion (1–2 Minutes)

> *"Finally, let's discuss an important architectural tradeoff: **Autonomous Dynamic Planning versus Deterministic Workflow Pipelines**.*
> 
> *In an autonomous agent, you have two architectural extremes:*
> 1. *A purely deterministic DAG—like a hardcoded 5-step pipeline where step 1 is always outline, step 2 is always draft, and step 3 is always format.*
> 2. *A fully open-ended autonomous loop—where the agent generates arbitrary sub-tasks and loops indefinitely until it chooses to stop.*
> 
> *Why not a purely open-ended loop? In enterprise document production, unconstrained autonomous loops suffer from non-deterministic latency, unpredictable tool hallucination, and run-away cost spikes.*
> 
> *Why not a rigid hardcoded pipeline? A hardcoded pipeline cannot handle ambiguous requests like Test Case 2, where conflicting requirements require an upfront assumption negotiation phase.*
> 
> *In DocAgent, I engineered a **hybrid balanced pattern**: The agent has full autonomous discretion during the **Planning Phase** to assess conflicts, generate explicit assumptions, and determine what tools and sections are required. However, once the execution plan is minted, the agent transitions into a **deterministic execution and reflection gate**.*
> 
> *This provides the optimal balance: the flexibility and problem-solving power of an autonomous agent, combined with the reliability, speed, and safety of an enterprise REST API.*
> 
> *Thank you for your time, and I look forward to your questions!"*

---

## 💡 Quick Tips for Recording
1. **Resolution**: Record at 1080p (1920x1080) with browser zoom at 110%.
2. **Terminal command to run before recording**:
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```
3. **Open URLs in tabs**:
   - Tab 1: `http://localhost:8000` (Main Demo UI)
   - Tab 2: `http://localhost:8000/docs` (Swagger API Docs)
   - Microsoft Word ready to open downloaded `.docx` files.

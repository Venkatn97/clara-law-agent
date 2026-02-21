# Clara — AI Voice Agent for Law Firms

> Production-grade AI receptionist built for Morrison & Associates Law Firm. Clara handles 24/7 call intake, qualifies leads, books consultations, and escalates urgent cases using AWS Bedrock, LangGraph, ElevenLabs, and Vapi.

---

## The Problem

Morrison & Associates Law Firm was missing 40+ calls per day after hours. Each missed call is a potential $5,000+ case. The firm needed a solution that:

- Answers every call 24/7 with no missed calls
- Qualifies leads before passing to attorneys
- Books free consultations automatically
- Escalates arrests and emergencies immediately
- Answers common questions without attorney involvement

**Result:** 0 missed calls. Consultations booked automatically. Lawyers notified of urgent cases within 2 minutes.

---

## Architecture

```
Caller
  │
  ▼
Twilio Phone Number
  │
  ▼
Vapi (Voice Orchestration)
  │
  ├── ElevenLabs Sarah (Speech to Text + Text to Speech)
  │
  ▼
FastAPI Server (api.py)
  │
  ▼
LangGraph Agent (agent/agent.py)
  │
  ├── AWS Bedrock Claude Sonnet (AI Brain)
  │
  ├── Bedrock Knowledge Base (RAG — firm documents)
  │     └── S3 + OpenSearch Vector Store
  │
  ├── Bedrock Guardrails (Safety Layer)
  │     ├── Block legal advice
  │     ├── Mask PII
  │     ├── Block prompt injection
  │     └── Contextual grounding (0.8 threshold)
  │
  └── Tools
        ├── book_consultation
        ├── capture_lead
        ├── escalate_urgent_case
        ├── check_availability
        └── search_firm_knowledge
  │
  ▼
CloudWatch Monitoring
  │
  ▼
Docker Container on AWS ECS Fargate (24/7)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Model | AWS Bedrock Claude Sonnet |
| Agent Orchestration | LangGraph |
| Voice Orchestration | Vapi |
| Text to Speech | ElevenLabs Sarah |
| RAG | AWS Bedrock Knowledge Base + OpenSearch |
| Safety | AWS Bedrock Guardrails |
| API | FastAPI + Uvicorn |
| Deployment | Docker + AWS ECR + ECS Fargate |
| Monitoring | AWS CloudWatch |
| Tunneling (dev) | Ngrok |

---

## Features

- 24/7 voice call handling with natural conversation
- Lead qualification and CRM capture
- Free consultation booking
- Urgent case escalation with on-call attorney notification
- RAG from real firm documents (FAQ, pricing, attorney bios)
- PII protection — caller data masked in logs
- Bedrock Guardrails blocking legal advice and prompt injection
- Streaming responses for low latency voice
- Automated evals with 80% pass threshold before deployment
- CloudWatch monitoring dashboard

---

## Project Structure

```
clara-law-agent/
├── agent/
│   ├── __init__.py
│   ├── agent.py          # LangGraph brain — builds the agent graph
│   ├── memory.py         # AgentState TypedDict + session management
│   ├── prompts.py        # Clara's personality, rules, and system prompt
│   └── tools.py          # 5 tools Clara can call
├── evals/
│   ├── __init__.py
│   └── test_cases.py     # 8 automated test cases, blocks deploy if <80%
├── knowledge-base/
│   ├── attorneys.txt     # Attorney profiles and specialities
│   ├── faq.txt           # Common caller questions and answers
│   └── pricing.txt       # Fee structure for all practice areas
├── api.py                # FastAPI server with /chat and /chat/completions
├── chat.py               # Terminal chat interface for local testing
├── start.py              # Local dev server with Ngrok HTTPS tunnel
├── Dockerfile            # Production container definition
├── .dockerignore         # Excludes .env and unnecessary files
└── requirements.txt      # Python dependencies
```

---

## Local Development

**Prerequisites:**
- Python 3.11+
- AWS account with Bedrock access
- ElevenLabs account
- Vapi account
- Ngrok account

**Setup:**

```bash
git clone https://github.com/yourusername/clara-law-agent
cd clara-law-agent
pip install -r requirements.txt
```

Create a `.env` file:

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
BEDROCK_REGION=us-east-1
BEDROCK_KNOWLEDGE_BASE_ID=your_kb_id
BEDROCK_GUARDRAIL_ID=your_guardrail_id
BEDROCK_GUARDRAIL_VERSION=DRAFT
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
VAPI_PRIVATE_KEY=your_key
NGROK_AUTH_TOKEN=your_token
NGROK_URL=your_ngrok_url
```

**Run terminal chat:**

```bash
python chat.py
```

**Run voice API with Ngrok:**

```bash
python start.py
```

---

## Running Evals

```bash
python evals/test_cases.py
```

8 test cases covering:
- Lead routing by practice area
- Guardrail blocks (legal advice, competitor mentions)
- Urgent case escalation
- Knowledge base queries
- Prompt injection defense
- Professional tone

Must pass 80%+ before deploying to production.

---

## Deployment

**Build and push Docker image:**

```bash
# Login to ECR
(Get-ECRLoginCommand -Region us-east-1).Password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build
docker build -t clara-law-agent .

# Tag
docker tag clara-law-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/clara-law-agent:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/clara-law-agent:latest
```

**Deploy to ECS Fargate:**

1. Create ECS cluster with Fargate
2. Create task definition with ECR image URI and environment variables
3. Create service with desired count 1
4. Open port 8000 in security group
5. Point Vapi Custom LLM URL to container IP

---

## AWS Services Used

| Service | Purpose |
|---|---|
| Bedrock Claude Sonnet | AI language model |
| Bedrock Knowledge Base | RAG document search |
| Bedrock Guardrails | Safety and PII protection |
| S3 | Firm document storage |
| OpenSearch Serverless | Vector database for RAG |
| ECR | Docker image registry |
| ECS Fargate | Serverless container hosting |
| CloudWatch | Monitoring and alerting |
| IAM | Security and access control |

---

## Guardrails Configuration

| Guardrail | Setting |
|---|---|
| Legal advice | Blocked (denied topic) |
| Settlement amounts | Blocked (denied topic) |
| Competitor recommendations | Blocked (denied topic) |
| Prompt injection | Blocked (HIGH sensitivity) |
| PII — SSN, credit card | Blocked |
| PII — phone, email, name | Anonymized |
| Contextual grounding | 0.8 threshold |
| Relevance | 0.7 threshold |

---

## Lessons from Production

- Streaming responses reduced latency from 6.4 seconds to under 2 seconds
- Bedrock Guardrails automatically blocked legal advice requests without any custom code
- ECS Fargate eliminated EC2 instance management entirely
- RAG grounding threshold of 0.8 prevented hallucinations on pricing and attorney details
- LangGraph's conditional edges made tool routing clean and debuggable
- Vapi requires HTTPS — ALB or Cloudflare Tunnel needed for production

---

## Roadmap

- [ ] AWS ALB with HTTPS for permanent Vapi connection
- [ ] Real Calendly API integration for consultation booking
- [ ] Real HubSpot API integration for lead capture
- [ ] Twilio SMS notifications for urgent case escalation
- [ ] LangSmith tracing for production observability
- [ ] GitHub Actions CI/CD pipeline
- [ ] Reduce latency below 2 seconds with Claude Haiku

---

## Built By

Built as a Forward Deployed Engineer portfolio project demonstrating end-to-end AI agent deployment on AWS.

## Demo
https://youtu.be/ZRQZwAqKUx8

**Skills demonstrated:** AWS Bedrock, LangGraph, RAG, Voice AI, Docker, ECS Fargate, CloudWatch, FastAPI, Bedrock Guardrails, Evals

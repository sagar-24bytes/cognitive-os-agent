# Personal Cognitive OS

An autonomous, goal-driven, voice-based AI system that plans, executes, remembers, and learns from user interactions to manage and organize a personal computer.

This is not a chatbot.  
This is an agentic operating system layer.

---

## What it does

Personal Cognitive OS listens to natural language voice commands and:

1. Understands user intent using an LLM (Gemini)
2. Decomposes goals into structured execution plans
3. Normalizes and grounds plans into real system actions
4. Executes tools on the local machine
5. (Planned) Stores long-term memory and reflects on outcomes

---

## Core Architecture
```text
Voice (Whisper – local, offline)
↓
Planner (Gemini + Structured Output)
↓
Plan Normalizer / Grounder
↓
Executor (Defensive Local Tools)
↓
Memory + Reflection (WIP)

```

---

## Current Features

- Whisper (offline, local speech recognition)

- 🧠 LLM-based goal planner (Gemini)
- 📋 Structured JSON planning (Pydantic)
- 🔧 Tool normalization & argument grounding
- 🛡️ Defensive tool execution (safe handling of no-op and invalid plans)
- 🧭 OS-safe path grounding (LLM never executes raw paths)

- 🧪 Dry-run execution mode
- ⚙️ Real system execution layer

---

## Example

User says:

> "Organize my downloads folder"

System generates:

```json
{
  "goal": "Organize my downloads folder",
  "steps": [
    {"tool": "scan_folder", "args": {"path": "~/Downloads"}},
    {"tool": "create_folder", "args": {"path": "~/Downloads/Documents"}},
    {"tool": "move_file", "args": {
      "source_directory": "~/Downloads",
      "destination_directory": "~/Downloads/Documents",
      "file_pattern": "*.pdf"
    }}
  ]
}
```

Then executes locally.

## Tech Stack

- Python 3.11+

- 🎙️ Offline, high-accuracy voice recognition (Whisper – local)


- LangGraph

- LangChain

- Gemini API

- Pydantic

- SQLite (memory layer - WIP)

- Vision

### This project aims to become a personal autonomous operating system layer:

- self-improving agent

- long-term memory

- reflection loops

- tool learning

- minimal human micromanagement

### Inspired by:

- AutoGPT

- BabyAGI

- OpenAI function calling

- Cognitive architectures

## Status

- Actively under development with stable end-to-end voice → action pipeline.
  
- Memory, reflection, and self-correction layers are currently being built.

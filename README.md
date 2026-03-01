# 🎙️ Browser Use Voice Agent

A Voice AI Agent connected to a Browser to perform tasks on your behalf

[<img src="https://img.youtube.com/vi/8Hk0A0hUKyg/sddefault.jpg" alt="Demo Video" style="width: 100%;">](https://www.youtube.com/watch?v=8Hk0A0hUKyg "Watch the demo video")

## Features

- **Real-Time Interaction**: Instant responses and actions based on voice input
- **Autonomous Browser Interaction**: The agent can navigate websites, fill forms, click buttons, and complete complex multi-step workflows
- **Context-Aware**: Browser logs are fed into the agent's context window for intelligent decision-making
- **Persistent Sessions**: Uses Browser Use profiles to maintain logged-in sessions across tasks

## Practical Use Case

I told the Agent to order Sushi for me on Glovo. 30 minutes later, the Sushi was at my door:

![Browser Use Voice Agent ordered Sushi for me](https://github.com/user-attachments/assets/d99bb970-0053-4051-ae08-a38cf9950c74)

The agent understood my request, navigated to Glovo, selected items, and completed the order.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- API keys for:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Deepgram](https://console.deepgram.com/)
  - [Cartesia](https://cartesia.ai/)
  - [Browser Use](https://cloud.browser-use.com/)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/adriablancafort/agentic-hackathon-browser-use-voice-agent.git
cd agentic-hackathon-browser-use-voice-agent
```

### 2. Configure environment variables

Create a `.env` file in the project root with the following:

```env
DEEPGRAM_API_KEY=
OPENAI_API_KEY=
CARTESIA_API_KEY=

BROWSER_USE_API_KEY=
BROWSER_USE_PROFILE_ID=
```

### 3. Setup browser profile

**Important**: Run this first to sync your local browser cookies to Browser Use. This allows the agent to access websites where you're already logged in (e.g., food delivery services, shopping sites):

```bash
bash setup-browseruse-profile.sh
```

This script will:
- Download the profile-use utility
- Connect to your Browser Use account
- Sync your local browser cookies and session data
- Create a persistent browser profile for the agent

### 4. Run the agent

```bash
uv run main.py
```

The agent will:
1. Install all dependencies automatically (first run)
2. Start the voice pipeline
3. Wait for you to connect via WebRTC
4. Greet you and explain its capabilities

## Acknowledgments

- [Pipecat](https://github.com/pipecat-ai/pipecat) - Real-time voice agent framework
- [Browser Use](https://github.com/browser-use/browser-use) - Browser automation library

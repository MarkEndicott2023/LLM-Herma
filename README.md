# AI Instructor

A personal, AI-driven tutor that manages long-term learning across multiple domains. Rather than acting as a chatbot, it works as a spaced-repetition instructor: it tracks what you know, decides what to work on next, teaches in small interactive chunks, and verifies understanding through assessment. All learner state lives in plain JSON files (`learner.json` and one file per domain under `domains/`), so your progress is fully transparent and portable.

## How to Use

Open this project in Claude Code and tell it what you want to do. Say **"let's study"** to begin a session on the highest-priority topic, **"let's study [domain]"** to focus on one subject, **"new subject"** or **"add [topic]"** to bootstrap a new domain, or **"status"** for a dashboard of all your domains and review schedule. Optionally drop curated materials (PDFs, notes) into `sources/[domain]/` so the tutor grounds its teaching in your actual coursework.

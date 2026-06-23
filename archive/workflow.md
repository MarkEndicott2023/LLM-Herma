# AI Instructor — Student Workflow

## 1. Setup

- Open a terminal and navigate to the `AI-Instructor` directory.
- Start a Claude Code session (`claude`).

## 2. Add a New Subject

1. Say **"new subject: [topic]"** (e.g., "new subject: microeconomics").
2. Optionally, drop source materials into `sources/[topic]/` beforehand — textbook PDFs, lecture notes, slides, problem sets.
3. The tutor will ask:
   - What is your goal? (exam, certification, general understanding, work skill)
   - What do you already know?
4. The tutor builds a knowledge graph (15-40 concepts) from your sources or from the topic structure.
5. You take a **quick diagnostic** — 3-5 questions across difficulty levels to establish your starting point.
6. The tutor saves your initial knowledge profile. You're ready to study.

## 3. Daily Study Session

1. Say **"let's study"** (or **"let's study [domain]"** to target a specific subject).
2. The tutor checks your state and picks the highest-priority item:
   - **Overdue reviews** come first — concepts you learned but are about to forget.
   - **New concepts** come next — the next unlocked topic where you've met prerequisites.
   - **Struggling concepts** — things you've seen but haven't retained.
3. The tutor **teaches** the concept concisely (3-5 paragraphs, grounded in your source materials if available).
4. The tutor **quizzes you** immediately — 2-4 questions mixing recall, application, and edge cases.
5. You answer. The tutor scores you, gives feedback on anything you got wrong, and updates your state.
6. The tutor offers to continue with the next item or wrap up.
7. Repeat as long as you want.

## 4. Check Your Progress

- Say **"status"** or **"dashboard"** at any time.
- The tutor shows:
  - Each domain and its overall mastery percentage.
  - How many concepts are learned, in progress, and not yet started.
  - How many reviews are due today.

## 5. Add Source Materials Anytime

1. Create a folder under `sources/` matching your domain name (e.g., `sources/microeconomics/`).
2. Drop in files — PDFs, markdown notes, problem sets.
3. The tutor will incorporate them into future teaching and assessment for that domain.

## 6. Ask Freeform Questions

- You can ask any question at any time, even mid-session.
- The tutor answers it, then checks if it relates to a tracked concept and offers to fold it into your learning state.

## 7. Over Time

- Intervals between reviews stretch as you demonstrate mastery — from 1 day to weeks to months.
- The system adapts: concepts you find easy accelerate, concepts you struggle with get more frequent attention.
- Prerequisites stay gated — you won't be pushed into advanced material with shaky foundations.
- Your state lives in `learner.json` plus one file per domain under `domains/`. It persists across sessions and grows with you.

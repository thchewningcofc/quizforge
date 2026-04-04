Here's a prompt you can paste at the start of any future conversion request:

---

**QuizForge JSON Conversion Prompt**

Convert the attached question file into a QuizForge-importable JSON deck. Follow these rules exactly:

**Format:** Output a single valid JSON file matching this structure:
```json
{
  "version": 2,
  "exportedAt": "<today's ISO date>",
  "decks": [{
    "id": "custom_<topic>_<domain>",
    "name": "<Exam> <Domain Name>",
    "tag": "<source> · <N> questions",
    "questions": [...],
    "builtin": false,
    "provider": "manual",
    "_best": null,
    "_missed": [],
    "_sessions": "0"
  }]
}
```

Each question object:
```json
{
  "id": <sequential integer starting at 1>,
  "question": "<full question text>",
  "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
  "answer": "<single correct letter>"
}
```

**Handling special cases — do not skip, convert instead:**

- **Multi-select questions** ("select all that apply"): Reframe as "Which of the following is NOT..." or "Which ONE of the following best represents..." so a single answer is correct. Adjust the answer key accordingly.
- **Diagram/image-dependent questions**: Embed the essential visual information directly into the question text (e.g., describe matrix axes and quadrant positions, list the framework steps shown, describe what the screenshot depicts). Do not skip.
- **Scenario-based question groups**: Embed a brief scenario summary into each sub-question so it is self-contained without the original preamble.
- **Matching/ordering questions**: Convert to "Which of the following correctly matches X to Y?" with one clearly correct option and three plausible distractors. Do not skip.
- **Questions with answer options exactly like "I, II, III, IV"**: Keep those literal option values — do not expand them to prose.

**Quality rules:**
- Preserve all original option text exactly, including punctuation and capitalization.
- Bold key qualifier words in the question text (MOST, BEST, FIRST, NOT, PRIMARY, ONLY, NEVER, ALWAYS) using ALL CAPS — they are already uppercase in most source materials, keep them that way.
- Never invent answer options or change an answer key.
- If a question is truly impossible to convert to single-answer format without misrepresenting the content, note it at the end as a comment — do not silently drop it.
- Validate your own output: confirm the question count in the tag matches the actual number of question objects.

**After generating the file**, report:
1. Total questions included
2. Any questions that were reframed and how
3. Any questions skipped and why

---

A few tips on using it:

- If the source is a **PDF**, say "Use Gemini/Claude to extract" or just attach it — the prompt handles the rest.
- If you're converting **multiple chapters at once**, add "Create one deck per chapter, using sequential IDs that don't restart between decks" to avoid ID collisions on import.
- The "report at the end" instruction is the key efficiency gain — it surfaces every judgment call in one place rather than requiring you to audit the file yourself.

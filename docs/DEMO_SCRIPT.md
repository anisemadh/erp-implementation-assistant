# ERP Assistant Demo Script - Oct 22, 2025

## Setup (Before Demo)
- Open app: `streamlit run src/app.py`
- Clear chat history (sidebar button)
- Have browser ready, full screen

---

## Introduction (1 minute)

"I've built an AI assistant for Infor M3 implementations. It uses our actual documentation and responds like a senior consultant would - with specific programs, step-by-step guidance, and practical advice."

**Key points:**
- Trained on our M3 documentation (4 PDFs, 6,000+ chunks)
- Understands different question types
- Cites specific M3 programs
- Structured, consistent responses

---

## Demo Flow (8-10 minutes)

### **Demo 1: Configuration Question** (3 min)

**Type:** "How do I configure a customer order type?"

**Watch for:**
- ✅ Status shows "Modules: OIS, PPS" (smart filtering)
- ✅ Response streams in real-time (feels fast)
- ✅ Structured format: Program, Navigation, Steps, Testing, Common Mistakes

**Highlight:**
"Notice it references **OIS010** specifically, gives exact field names like **ORTP** and **ORCA**, and includes a testing section. This is consultant-level detail."

---

### **Demo 2: Troubleshooting Question** (3 min)

**Type:** "Why can't I allocate a customer order?"

**Watch for:**
- ✅ Diagnostic approach (likely causes first)
- ✅ Step-by-step checks with specific programs
- ✅ Multiple resolution paths

**Highlight:**
"It follows a troubleshooting methodology - checks order status, credit holds, inventory - all with specific M3 programs to look at. This is how we'd diagnose it on a real project."

---

### **Demo 3: Best Practice Question** (3 min)

**Type:** "Should we use hard or soft allocation for customer orders?"

**Watch for:**
- ✅ Recommendation with rationale
- ✅ Tradeoffs explained
- ✅ Implementation strategy
- ✅ Decision matrix

**Highlight:**
"It doesn't just say 'use hard allocation' - it explains WHY, gives scenarios for each approach, and provides a decision framework. This is strategic guidance, not just how-to."

---

### **Demo 4: Show Example Questions** (1 min)

**Click sidebar examples:**
- "How do I set up a new customer?"
- "Why doesn't pricing populate?"

**Show:** Variety of question types all get high-quality responses

---

## Key Features to Emphasize

**1. Intelligence:**
- 🧠 Understands question type (config vs troubleshooting vs best practice)
- 📁 Filters to relevant M3 modules automatically
- 🎯 Retrieves most relevant documentation

**2. Quality:**
- 📋 Structured responses (always includes: Program, Steps, Testing, Common Mistakes)
- 🎓 Consultant-level detail (field names, program codes, real-world advice)
- ✅ Consistent format across all questions

**3. Speed:**
- ⚡ Streaming responses (feels fast, 2-3 seconds perceived)
- 🔍 Smart retrieval (only searches relevant modules)

---

## Feedback Questions

**Ask the group:**
1. "What questions would YOU ask it about your current project?"
2. "What would make this more useful for your work?"
3. "Any features you'd want added?"

**Take notes on:**
- Questions they try
- Features they request
- Concerns or limitations they identify

---

## Possible Questions & Answers

**Q: "Can it access live M3 data?"**
A: "Not yet - currently uses documentation only. But we could integrate with M3 APIs to check configurations, which is on the roadmap."

**Q: "How accurate is it?"**
A: "Very accurate on documented procedures. It's trained on official M3 documentation and uses examples I created from real implementations. Always good to verify critical configs, but it's solid."

**Q: "Can it handle project-specific questions?"**
A: "Yes and no. General M3 questions are great. For project-specific customizations, we'd need to add that project's documentation to the knowledge base."

**Q: "What if it gives wrong info?"**
A: "It cites specific programs and documents, so you can verify. Also, it's meant to assist, not replace, consultant judgment. Think of it as a smart junior consultant."

**Q: "How do I access this?"**
A: "Right now it's a prototype on my laptop. Next steps would be deploying it as a web service for the team. That's 1-2 weeks of work."

---

## Wrap Up (1 min)

"This is where we are after 2 weeks of development. Next steps based on your feedback:
- Deploy as web service for team access
- Add more documentation sources
- Potentially integrate with live M3 data
- Whatever features you need most"

**Call to action:**
"I'd love to get your feedback. Try it on your projects, let me know what works and what doesn't."

---

## Technical Details (If Asked)

**Stack:**
- Vector database with 6,360 document chunks
- GPT-4o-mini for generation
- Query enhancement with M3 terminology
- Module-based filtering
- Few-shot learning for consistency

**Performance:**
- ~10 seconds total processing
- Feels like 2-3 seconds with streaming
- Searches 6,360 chunks in <1 second
- Can handle 100+ users with proper deployment
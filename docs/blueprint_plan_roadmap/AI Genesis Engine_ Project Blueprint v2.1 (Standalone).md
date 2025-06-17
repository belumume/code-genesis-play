# **AI Genesis Engine: Project Blueprint v2.1**

## **1\. Introduction**

### **1.1. Vision & Mission**

* **Vision:** To redefine the boundaries of creation by empowering anyone to bring entire interactive worlds to life through a simple, expressed idea.  
* **Mission:** To deploy a live web application, the "Genesis Engine," where users can enter a single-sentence prompt and have a fully autonomous, self-correcting AI system generate and present a unique, playable, browser-based 2D game without human intervention or verification.

### **1.2. Goals & Objectives**

* **Primary Goal:** Win the $10,000 Grand Prize in the Lovable AI Showdown.  
* **Secondary Goal:** Win the $10,000 model-specific prize for Claude 4 Sonnet.  
* **Core Technical Objective:** To architect an engine that generates **JavaScript/HTML5** game code to enable direct, in-browser gameplay, fulfilling modern web application standards.  
* **Demonstration Objective:** Allow judges to interact with a live web app, enter their own prompts, and witness the entire autonomous design, coding, testing, and debugging loop, culminating in a game they can immediately play.

### **1.3. Scope**

* **In Scope:**  
  * A full-stack web application (React/TypeScript Frontend, Python/FastAPI Backend).  
  * An AI agent core loop that performs:  
    1. **Conceptualization:** (Architect Agent) Generates GDD, Tech Plan.  
    2. **Code Generation:** (Engineer Agent) Writes game logic in **JavaScript** (using a simple library like p5.js).  
    3. **Automated Testing:** (Sentry Agent) Executes the generated JS code in a headless browser to detect errors.  
    4. **Autonomous Debugging:** (Debugger Agent) Fixes errors caught by the Sentry.  
  * Generation of a single, self-contained HTML/JS file for each game.  
  * **Direct, in-browser execution** of the generated game within an \<iframe\> or similar sandboxed element in the React UI.  
* **Out of Scope:**  
  * Generation of non-JavaScript-based games (e.g., Python/Pygame).  
  * Manual verification or debugging of generated code by the project lead.

## **2\. Guiding Principles & Development Methodology**

### **2.1. Collaboration Model ("Autonomous Creator")**

* **The Human (Project Director):** The Project Director's role is purely strategic: to provide the initial vision (the prompt) and to observe the autonomous system. The Director does not verify code; they verify that the system as a whole achieves its goal.  
* **The AI Agents (The Autonomous Team):**  
  * **Architect (Claude Sonnet):** The Visionary. Creates the high-level plan.  
  * **Engineer (Claude Sonnet):** The Coder. Executes one task from the plan.  
  * **Sentry (Headless Browser \- Puppeteer/Playwright):** The QA. A merciless, automated script that only reports success (no errors) or failure (provides the exact error).  
  * **Debugger (Claude Sonnet):** The Fixer. Is activated only on failure, receiving the goal, the broken code, and the error to provide a correction.

### **2.2. Development Methodology**

* **Autonomous Self-Correction:** The system is designed as a closed loop. The AI writes code, a script tests it, and if it fails, the AI debugs its own work. This cycle repeats until the code is flawless. This is the cornerstone of the "pushing the limits" narrative.  
* **Documentation-Driven Development:** The Architect MUST first generate the GDD.md and TECH\_PLAN.md before the Engineer begins coding.  
* **Targeted Simplicity:** The AI will be instructed to generate code using a minimal, beginner-friendly JavaScript game library (e.g., p5.js) to maximize the probability of generating correct, self-contained code.

## **3\. Core Requirements**

### **3.1. Functional Requirements (FR)**

* **FR1:** The user shall input a single-sentence game concept into the React web interface.  
* **FR2:** The backend shall orchestrate a multi-agent AI system to autonomously plan, write, test, and debug a 2D game based on the prompt.  
* **FR3:** The generated game code MUST be **JavaScript/HTML5**.  
* **FR4:** The user shall see a real-time log of the autonomous development process (e.g., "Engineer writing player.js...", "Sentry detected error...", "Debugger correcting code...").  
* **FR5:** Upon successful generation, the game MUST be immediately playable within the same browser session without requiring a download or navigation.

### **3.2. Technical Requirements (TR)**

* **TR1:** Frontend: React/TypeScript.  
* **TR2:** Backend: Python/FastAPI.  
* **TR3:** Generated Game Language: **JavaScript** (p5.js or similar).  
* **TR4:** Automated Testing: A headless browser framework (e.g., Puppeteer, Playwright) accessible by the Python backend.  
* **TR5:** AI Model: Claude 4 Sonnet.

## **4\. Detailed Architecture & Technology**

### **4.1. Architecture Diagram**

graph TD  
    A\[User @ React Frontend\] \-- Prompt \--\> B\[Python/FastAPI Backend\];

    subgraph B  
        C\[Orchestrator\] \-- 1\. Plan \--\> D(Architect Agent);  
        D \-- GDD/Tech Plan \--\> C;  
        C \-- 2\. Code Task \--\> E(Engineer Agent);  
        E \-- Generated JS Code \--\> C;  
        C \-- 3\. Test Code \--\> F(Sentry Agent);  
        subgraph F  
            G\[Headless Browser\]  
        end  
        F \-- OK/ERROR \--\> C;  
        C \-- 4\. Debug Task (on ERROR) \--\> H(Debugger Agent);  
        H \-- Corrected JS Code \--\> C;  
    end

    C \-- Final JS/HTML File \--\> I\[File Storage\];  
    B \-- Real-time Log via WebSocket \--\> A;  
    A \-- Request to Play \--\> I;  
    I \-- Game File \--\> J\[iframe/Web Component in React\];  
    J \-- Playable Game \--\> A;

### **4.2. Workflow Breakdown (The Self-Correcting Loop)**

1. **Initiation:** User submits a prompt via the React UI. The request hits the FastAPI backend.  
2. **Architecture:** The **Architect Agent** is called once to generate the high-level GDD.md and a TECH\_PLAN.md that breaks the game into small, testable features.  
3. Autonomous Feature Implementation (Loop): The Orchestrator iterates through each feature in the TECH\_PLAN.md. For each feature:  
   a. Code: The Engineer Agent is tasked to write the JavaScript code for that single feature.  
   b. Test: The Sentry Agent takes the generated code, runs it in a headless browser, and looks for console errors.  
   c. Verify:  
   \* If the Sentry reports OK, the code is committed, and the loop continues to the next feature.  
   \* If the Sentry reports an ERROR, it passes the exact error message back to the Orchestrator.  
   d. Debug (if needed): The Debugger Agent is activated. It receives the feature goal, the broken code, and the specific error message. It generates a corrected version of the code, which is then sent back to the Sentry for re-testing (Step 3b). This debug sub-loop continues until the Sentry reports OK.  
4. **Completion:** Once all features in the plan are complete, the final, validated JS/HTML file is saved. The React UI is notified, and the "Play Game" button becomes active.  
5. **Execution:** When the user clicks "Play Game," the frontend loads the generated HTML file into a sandboxed \<iframe\>.

### **4.3. Technology Stack Summary**

* **Frontend:** React, TypeScript, Vite, TailwindCSS  
* **Backend:** Python 3.10+, FastAPI, WebSockets  
* **AI Model:** Claude 4 Sonnet  
* **Generated Game Language:** **JavaScript (p5.js recommended)**  
* **Autonomous Testing:** **Puppeteer** or **Playwright** (integrated with Python backend)

## **5\. UI/UX Design**

The UI is the existing React web application. The real-time log viewer is a critical component and must be enhanced to show the multi-agent activity, for example: ARCHITECT: Planning..., ENGINEER: Writing player.js..., SENTRY: Testing player.js... OK\!, SENTRY: Testing collision.js... ERROR\!, DEBUGGER: Fixing collision.js.... This makes the "self-policing" aspect visible and is critical for the demo.

## **6\. Deployment & Testing Strategy**

### **6.1. Deployment Strategy**

* React Frontend will be deployed on a static hosting service like Vercel or Netlify.  
* Python/FastAPI Backend will be deployed on a service like Render or Heroku.  
* The backend deployment environment **must include Node.js and the chosen headless browser framework** (Puppeteer/Playwright) to run the Sentry agent. Many hosting platforms support this via custom buildpacks or Dockerfiles.

### **6.2. Testing Strategy**

* The system's internal testing is **fully automated** via the Sentry/Debugger loop.  
* The Project Director's role is to perform **end-to-end integration testing**: ensuring the whole web app, from prompt submission to in-browser play, functions correctly on the final deployment platform.

## **7\. Development Roadmap**

* **Phase 1: JS Generation & Self-Correction (Critical Priority)**  
  * **Goal:** Implement the JavaScript multi-agent, self-correcting loop within the existing backend.  
  * **Tasks:**  
    1. Integrate a headless browser library (e.g., pyppeteer) into the Python backend.  
    2. Modify the core orchestrator to implement the multi-agent loop (Architect \-\> Engineer \-\> Sentry \-\> Debugger).  
    3. Rewrite the AI prompts to target p5.js instead of pygame.  
    4. Update the FastAPI backend to save the final output as a .html file.  
    5. Update the React frontend to fetch and display the .html game in an \<iframe\>.  
    6. Update the real-time log viewer to display the new multi-agent status messages.  
  * **Milestone:** The application can successfully take a prompt and produce a playable, in-browser game that has gone through at least one automated debug cycle.  
* **Phase 2: Final Polish & Deployment**  
  * **Goal:** Ensure stability, polish the UI, and deploy the final application for submission.  
  * **Tasks:**  
    1. Finalize the styling of the in-game \<iframe\> container and surrounding UI.  
    2. Configure and lock down the production deployment environment on a host that supports Python and Node.js.  
    3. Create the final demo video, heavily emphasizing the autonomous testing and debugging loop shown in the logs.  
    4. Write the final README.md and submit the project.

## **8\. AI Agent Collaboration Rules**

1. **Rule of Specialization:** You will act as one of four agents: Architect, Engineer, Sentry, or Debugger. Your role and context will be clearly defined in your prompt.  
2. **Rule of Language:** As the **Engineer** or **Debugger**, your code output MUST be JavaScript, using the p5.js library and contained within a single HTML file structure. You are forbidden from writing Python for the game logic.  
3. **Rule of Focused Debugging:** As the **Debugger**, your only input is the goal, the broken code, and the precise error message. Your only output is the complete, corrected code file. Do not add new features or commentary.  
4. **Rule of Testability:** As the **Architect**, you must break down the game into the smallest possible, independently testable features. As the **Engineer**, you must only implement one of these features at a time.
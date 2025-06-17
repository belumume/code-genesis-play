# **AI Genesis Engine: Project Blueprint v2.3**

## **1\. Introduction**

### **1.1. Vision & Mission**

* **Vision:** To redefine the boundaries of creation by empowering anyone to bring entire interactive worlds to life through a simple, expressed idea.  
* **Mission:** To build and deploy a production-ready, flawlessly functional web application, the "Genesis Engine," where a fully autonomous, self-correcting AI system can reliably generate, store, and present unique, playable, browser-based 2D games.

### **1.2. Goals & Objectives**

* **Primary Goal:** Achieve a state of architectural completeness and operational flawlessness for the AI Genesis Engine.  
* **Core Technical Objective 1 (Storage):** Solve ephemeral filesystem issues by integrating a persistent cloud storage solution for all generated games.  
* **Core Technical Objective 2 (Reliability):** Solve real-time communication issues by implementing a robust status-checking mechanism with a reliable polling fallback.  
* **Final Product Objective:** The application must be fully functional for any user, at any time, without reliance on pre-existing demo content or manual workarounds.

### **1.3. Scope**

* **In Scope:**  
  * A full-stack web application (React/TypeScript Frontend, Python/FastAPI Backend).  
  * A multi-agent AI core loop (Architect, Engineer, Sentry, Debugger).  
  * Generation of self-contained JavaScript/HTML5 game files.  
  * Integration with a persistent object storage service (e.g., AWS S3, Cloudflare R2) for all generated game files.  
  * A robust progress-tracking system, combining WebSockets with a reliable API polling fallback.  
  * Direct, in-browser execution of the generated game via a permanent URL provided by the storage service.  
* **Out of Scope:**  
  * Any reliance on the local server filesystem for storing generated games.  
  * The "demo game" fallback functionality (to be deprecated and removed).  
  * Manual verification or debugging of generated code by the project lead.

## **2\. Guiding Principles & Development Methodology**

### **2.1. Collaboration Model ("Autonomous Creator")**

* **The Human (Project Director):** The Director's role is purely strategic: providing the initial vision (the prompt) and observing the autonomous system. The Director does not verify code; they verify that the system as a whole achieves its goal.  
* **The AI Agents (The Autonomous Team):** Architect, Engineer, Sentry, and Debugger agents collaborate to autonomously produce and validate game code.

### **2.2. Development Methodology**

* **Production-Grade Robustness:** All systems must be designed for reliability and scalability. Temporary fixes and workarounds are not acceptable.  
* **Autonomous Self-Correction:** The system's closed loop (Code \-\> Test \-\> Debug) is the core of its operation, ensuring the quality of the generated output.  
* **Decoupled Architecture:** Services like game storage will be decoupled from the core application logic to improve scalability and resilience.  
* **Documentation-Driven Development:** The Architect agent MUST first generate design and technical planning documents before the Engineer agent begins coding.

## **3\. Core Requirements**

### **3.1. Functional Requirements (FR)**

* **FR1:** The system MUST upload every successfully generated game to a persistent cloud storage bucket.  
* **FR2:** The system MUST provide the user with a permanent, publicly accessible URL to the generated game upon completion.  
* **FR3:** The frontend MUST provide reliable, near-real-time updates on generation progress, using a polling mechanism if the primary WebSocket connection fails.  
* **FR4:** The get-latest-game endpoint and all related functionality must be powered by the persistent cloud storage, not the local filesystem.

### **3.2. Technical Requirements (TR)**

* **TR1:** Frontend: React/TypeScript.  
* **TR2:** Backend: Python/FastAPI.  
* **TR3:** Generated Game Language: JavaScript (p5.js or similar).  
* **TR4:** Autonomous Testing: Headless browser framework (Puppeteer/Playwright).  
* **TR5:** Persistent Storage: An S3-compatible object storage service and its corresponding SDK (e.g., boto3).  
* **TR6:** AI Model: Claude 4 Sonnet.

## **4\. Detailed Architecture & Technology**

### **4.1. Architecture Diagram**

graph TD  
    A\[User @ React Frontend\] \-- 1\. Prompt \--\> B\[Python/FastAPI Backend\];

    subgraph B  
        C\[Orchestrator\] \-- 2\. Plan \--\> D(Architect Agent);  
        D \--\> C;  
        C \-- 3\. Loop: Code \--\> E(Engineer Agent);  
        E \--\> C;  
        C \-- 4\. Loop: Test \--\> F(Sentry Agent);  
        F \--\> C;  
        C \-- 5\. Loop: Debug \--\> H(Debugger Agent);  
        H \--\> C;  
    end  
      
    C \-- 6\. On Success: Upload File \--\> I\[☁️ Cloud Storage (S3, R2)\];  
    I \-- 7\. Returns Permanent URL \--\> C;  
    C \-- 8\. Saves URL to DB/Cache \--\> J\[Session State\];

    B \-- Real-time Log (WebSocket/Polling) \--\> A;  
    A \-- 9\. Request to Play \--\> K{Final Game URL};  
    K \-- from Session State \--\> A;  
    A \-- 10\. Loads Game in iframe \--\> I;

### **4.2. Workflow Breakdown**

1. **Initiation:** User submits a prompt via the React UI to the FastAPI backend.  
2. **Autonomous Generation Loop:** The multi-agent system (Architect, Engineer, Sentry, Debugger) collaborates to produce a validated, error-free game.html file in a temporary local directory.  
3. **Persistent Storage:** Upon successful generation, the Orchestrator uploads the game.html file to the configured cloud storage bucket.  
4. **URL Retrieval:** The cloud storage service returns a permanent, public URL for the uploaded game file.  
5. **Completion:** The backend signals completion to the frontend (via WebSocket or polling response), providing the permanent URL to the game.  
6. **Execution:** The user clicks "Play Game," and the React frontend loads the permanent URL into a sandboxed \<iframe\>.

### **4.3. Technology Stack Summary**

* **Frontend:** React, TypeScript, Vite, TailwindCSS  
* **Backend:** Python 3.10+, FastAPI, WebSockets  
* **AI Model:** Claude 4 Sonnet  
* **Generated Game Language:** JavaScript (p5.js recommended)  
* **Autonomous Testing:** Puppeteer or Playwright  
* **Persistent Storage:** AWS S3, Google Cloud Storage, or Cloudflare R2 (S3-compatible)

## **5\. UI/UX Design**

The UI is a React-based web application. Its "Generation Log" component is critical for displaying the real-time status of the agentic system. This log must reliably track progress, potentially displaying a "Connection lost, checking status..." message if it needs to switch from WebSockets to API polling.

## **6\. Deployment & Testing Strategy**

### **6.1. Deployment Strategy**

* Frontend will be deployed on a static hosting service like Vercel or Netlify.  
* Backend will be deployed on a service like Render or Heroku.  
* The backend deployment environment must include credentials for the cloud storage service (e.g., AWS\_ACCESS\_KEY\_ID, AWS\_SECRET\_ACCESS\_KEY) set as secure environment variables.

### **6.2. Testing Strategy**

* Internal code validation is fully automated via the Sentry/Debugger loop.  
* The Project Director's responsibility is to perform end-to-end integration testing, verifying that the full workflow from prompt submission to game file upload and retrieval from cloud storage functions correctly in the deployed environment.

## **7\. Development Roadmap**

* **Phase 1: Persistent Storage Integration (High Priority)**  
  * **Goal:** Replace the ephemeral filesystem with a robust cloud storage solution.  
  * **Tasks:**  
    1. Choose and configure a cloud storage provider (e.g., Cloudflare R2 for its generous free tier).  
    2. Integrate the provider's SDK into the Python backend.  
    3. Modify the Orchestrator to upload the final game.html upon successful generation.  
    4. Update the backend API to return the permanent cloud URL instead of a local file path.  
    5. Update the React frontend to use this permanent URL for the "Play Game" iframe.  
* **Phase 2: Communication Hardening**  
  * **Goal:** Ensure real-time progress updates are reliable.  
  * **Tasks:**  
    1. Create a new API endpoint in FastAPI (e.g., /api/sessions/{session\_id}/status) that returns the current status of a generation job.  
    2. Modify the React frontend to use a polling mechanism on this endpoint as a fallback if the WebSocket connection is unstable or fails.  
* **Phase 3: Deprecate Workarounds & Final Validation**  
  * **Goal:** Remove all temporary fixes and achieve a clean, production-ready state.  
  * **Tasks:**  
    1. Remove all "demo game" code from the backend file-serving logic.  
    2. Remove the "Play Demo Game" link from the React UI.  
    3. Conduct thorough end-to-end testing of the complete, hardened system.

## **8\. AI Agent Collaboration Rules**

1. **Rule of Specialization:** You will act as one of four agents: Architect, Engineer, Sentry, or Debugger. Your role and context will be clearly defined in your prompt.  
2. **Rule of Language:** As the **Engineer** or **Debugger**, your code output MUST be JavaScript, using the p5.js library and contained within a single HTML file structure. You are forbidden from writing Python for the game logic.  
3. **Rule of Focused Debugging:** As the **Debugger**, your only input is the goal, the broken code, and the precise error message. Your only output is the complete, corrected code file. Do not add new features or commentary.  
4. **Rule of Testability:** As the **Architect**, you must break down the game into the smallest possible, independently testable features. As the **Engineer**, you must only implement one of these features at a time.
# **AI Genesis Engine: Project Blueprint v2.5**

## **1\. Introduction**

### **1.1. Vision & Mission**

* **Vision:** To redefine the boundaries of creation by empowering anyone to bring entire interactive worlds to life through a simple, expressed idea.  
* **Mission:** To build and deploy a production-ready, flawlessly functional web application, the "Genesis Engine," where a fully autonomous, self-correcting AI system can reliably generate, store, and present unique, playable, browser-based 2D games.

### **1.2. Goals & Objectives**

* **Primary Goal:** Achieve a state of architectural completeness and operational flawlessness for the AI Genesis Engine.  
* **Core Technical Objective 1 (Storage):** Solve ephemeral filesystem issues by integrating a persistent cloud storage solution for all generated games.  
* **Core Technical Objective 2 (Reliability):** Solve real-time communication issues by implementing a robust status-checking mechanism with a reliable polling fallback.  
* **Core Technical Objective 3 (Flawless Testing):** Ensure the Sentry agent operates with full fidelity by mandating a Dockerized deployment environment that supports headless browser execution.  
* **Final Product Objective:** The application must be fully functional for any user, at any time, without reliance on pre-existing demo content or manual workarounds.

### **1.3. Scope**

* **In Scope:**  
  * A full-stack web application (React/TypeScript Frontend, Python/FastAPI Backend).  
  * A multi-agent AI core loop (Architect, Engineer, Sentry, Debugger).  
  * Generation of self-contained JavaScript/HTML5 game files.  
  * Integration with a persistent object storage service (e.g., AWS S3, Cloudflare R2).  
  * A robust progress-tracking system, combining WebSockets with a reliable API polling fallback.  
  * A Dockerized backend deployment to guarantee a consistent and capable runtime environment.  
  * Direct, in-browser execution of the generated game via a permanent URL.  
* **Out of Scope:**  
  * Non-Dockerized backend deployments.  
  * Any reliance on the local server filesystem for storing generated games.  
  * "Demo game" functionality.

## **2\. Guiding Principles & Development Methodology**

### **2.1. Collaboration Model ("Autonomous Creator")**

* **The Human (Project Director):** The Director's role is purely strategic: providing the initial vision (the prompt) and observing the autonomous system.  
* **The AI Agents (The Autonomous Team):** Architect, Engineer, Sentry, and Debugger agents collaborate to autonomously produce and validate game code.

### **2.2. Development Methodology**

* **Production-Grade Robustness:** All systems must be designed for reliability and scalability.  
* **Autonomous Self-Correction:** The system's closed loop (Code \-\> Test \-\> Debug) is the core of its operation.  
* **Containerization-First:** The backend application will be developed and deployed as a Docker container to ensure environment consistency and eliminate deployment-specific issues.  
* **Documentation-Driven Development:** The Architect agent MUST first generate design and technical planning documents before the Engineer agent begins coding.

## **3\. Core Requirements**

### **3.1. Functional Requirements (FR)**

* **FR1:** The system MUST upload every successfully generated game to a persistent cloud storage bucket.  
* **FR2:** The system MUST provide the user with a permanent, publicly accessible URL to the generated game upon completion.  
* **FR3:** The frontend MUST provide reliable, near-real-time updates on generation progress.  
* **FR4:** The Sentry agent's testing MUST be performed via a real headless browser.

### **3.2. Technical Requirements (TR)**

* **TR1:** Frontend: React/TypeScript.  
* **TR2:** Backend: Python/FastAPI.  
* **TR3:** Generated Game Language: JavaScript (p5.js or similar).  
* **TR4:** Autonomous Testing: Headless browser framework (Playwright) running within the production environment.  
* **TR5:** Persistent Storage: An S3-compatible object storage service (e.g., Cloudflare R2).  
* **TR6:** AI Model: Claude 4 Sonnet.  
* **TR7:** Deployment: **Docker.**

## **4\. Detailed Architecture & Technology**

### **4.1. Architecture Diagram**

graph TD  
    subgraph "Deployment Environment"  
        direction LR  
        DOCKER\[\<font size=6\>🐳 Docker Container\</font\>\]  
        subgraph DOCKER  
            B\[Python/FastAPI Backend\]  
            F\[Sentry Agent w/ Playwright\]  
        end  
    end

    A\[User @ React Frontend\] \-- 1\. Prompt \--\> B;

    subgraph "Autonomous Loop (within Backend)"  
        C\[Orchestrator\] \-- 2\. Plan \--\> D(Architect Agent);  
        D \--\> C;  
        C \-- 3\. Loop: Code \--\> E(Engineer Agent);  
        E \--\> C;  
        C \-- 4\. Loop: Test \--\> F;  
        F \-- OK/ERROR \--\> C;  
        C \-- 5\. Loop: Debug \--\> H(Debugger Agent);  
        H \--\> C;  
    end

    C \-- 6\. On Success: Upload File \--\> I\[☁️ Cloud Storage (S3, R2)\];  
    I \-- 7\. Returns Permanent URL \--\> C;

    B \-- Real-time Log (WebSocket/Polling) \--\> A;  
    A \-- 8\. Request to Play with URL \--\> I;  
    I \-- Game File \--\> J\[iframe in React\];  
    J \-- Playable Game \--\> A

### **4.2. Workflow Breakdown**

The core loop operates within a robust, containerized environment. This workflow describes the end-to-end process from user input to a playable game.

### **4.3. Technology Stack Summary**

* **Frontend:** React, TypeScript, Vite, TailwindCSS  
* **Backend:** Python 3.10+, FastAPI, WebSockets  
* **AI Model:** Claude 4 Sonnet  
* **Generated Game Language:** JavaScript (p5.js recommended)  
* **Autonomous Testing:** Playwright  
* **Persistent Storage:** Cloudflare R2 (or other S3-compatible service)  
* **Deployment Containerization:** **Docker**

## **5\. UI/UX Design**

The UI is a React application providing the interface to the Genesis Engine. A critical component is the real-time log viewer, which must reliably display the status of the agentic system.

## **6\. Deployment & Testing Strategy**

### **6.1. Deployment Strategy**

* The backend application **will be built as a Docker image** and deployed to a container-compatible hosting service (e.g., Render, Fly.io, AWS App Runner).  
* The Dockerfile will be the single source of truth for the production environment, ensuring all dependencies, including Python packages and Playwright's browser binaries, are installed correctly.  
* Frontend deployment will be to a static hosting service (e.g., Vercel, Netlify).

### **6.2. Testing Strategy**

* Internal code validation is fully automated via the Sentry/Debugger loop. Testing must occur exclusively via the headless browser; static analysis is not an acceptable path for the final product.  
* The Project Director's responsibility is to perform end-to-end integration testing on the fully deployed, containerized application.

## **7\. Development Roadmap**

* **Phase 1: Application Containerization (Critical Path)**  
  * **Goal:** Create a reliable, reproducible production environment using Docker.  
  * **Tasks:**  
    1. Create a Dockerfile for the Python/FastAPI backend.  
    2. The Dockerfile must handle the installation of all Python dependencies from requirements.txt.  
    3. The Dockerfile must correctly install Playwright and its browser dependencies (playwright install \--with-deps).  
    4. Configure the container to expose the correct port and run the production server script.  
    5. Test the Docker image locally to ensure the full application, including the Sentry agent, runs flawlessly.  
* **Phase 2: Persistent Storage Integration**  
  * **Goal:** Replace ephemeral filesystem storage with a robust cloud storage solution.  
  * **Tasks:**  
    1. Choose and configure a cloud storage provider (e.g., Cloudflare R2).  
    2. Integrate the provider's SDK into the Python backend.  
    3. Modify the Orchestrator to upload the final game.html upon successful generation.  
    4. Update the backend API to return the permanent cloud URL.  
    5. Update the React frontend to use this permanent URL.  
* **Phase 3: Communication Hardening**  
  * **Goal:** Ensure real-time progress updates are reliable.  
  * **Tasks:**  
    1. Create a /api/sessions/{session\_id}/status endpoint in FastAPI.  
    2. Modify the React frontend to poll this endpoint as a fallback if the WebSocket connection fails.  
* **Phase 4: Final Validation**  
  * **Goal:** Remove all temporary fixes and achieve a clean, production-ready state.  
  * **Tasks:**  
    1. Remove all "demo game" code and logic.  
    2. Deploy the final Docker container to the chosen hosting service.  
    3. Conduct thorough end-to-end testing of the complete, deployed system.

## **8\. AI Agent Collaboration Rules**

These rules govern the behavior of the AI agents within the autonomous system.

1. **Rule of Specialization:** You will act as one of four agents: Architect, Engineer, Sentry, or Debugger. Your role and context will be clearly defined in your prompt.  
2. **Rule of Language:** As the **Engineer** or **Debugger**, your code output MUST be JavaScript, using the p5.js library and contained within a single HTML file structure. You are forbidden from writing Python for the game logic.  
3. **Rule of Focused Debugging:** As the **Debugger**, your only input is the goal, the broken code, and the precise error message. Your only output is the complete, corrected code file. Do not add new features or commentary.  
4. **Rule of Testability:** As the **Architect**, you must break down the game into the smallest possible, independently testable features. As the **Engineer**, you must only implement one of these features at a time.
# **AI Genesis Engine: Project Blueprint v1.0**

## **1\. Introduction**

### **1.1. Vision & Mission**

* **Vision:** To redefine the boundaries of creation by empowering a single human to bring entire interactive worlds to life through a simple, expressed idea.  
* **Mission:** To build and demonstrate a prototype AI agent, the "Genesis Engine," that can autonomously generate a complete, unique, and playable 2D game from a single-sentence prompt, showcasing a paradigm shift from AI as a tool to AI as a creative partner.

### **1.2. Goals & Objectives**

* **Primary Goal:** Win the $10,000 Grand Prize in the Lovable AI Showdown by creating the most compelling and "limit-pushing" application.  
* **Secondary Goal:** Win the $10,000 model-specific prize for Claude 4 Opus by building an application that masterfully showcases its unique, synergistic capabilities (agentic coding, persistent memory, and creative reasoning).  
* **Demonstration Objective:** Produce a polished, \~3-minute video demonstrating the entire end-to-end process: from a single-sentence prompt to a live gameplay session of the generated game.

### **1.3. Scope**

* **In Scope:**  
  * A command-line interface (CLI) to accept a user's game concept prompt.  
  * An AI agent core loop that performs:  
    1. Conceptualization (Game Design Document generation).  
    2. Asset Specification (Generates descriptive prompts for all required art and sound).  
    3. Technical Planning (Outlines the code architecture).  
    4. Code Generation (Writes all game logic, assets, and build scripts in Python using the Pygame library).  
  * Generation of a complete, standalone game project folder.  
  * The generated game will be a simple 2D genre (e.g., platformer, top-down shooter, puzzle game).  
  * The project will use placeholder shapes for graphics initially to ensure a playable game is always the priority. The generated asset prompts will be used to create final assets if time permits.  
* **Out of Scope:**  
  * A graphical user interface (GUI) for the engine itself.  
  * Generation of 3D games or highly complex genres (e.g., RPGs, strategy games).  
  * Direct integration with image/sound generation models. Asset prompts will be generated as text files for manual use.  
  * Multiplayer functionality.  
  * An installer or package for the generated game; it will be run from the source.

## **2\. Guiding Principles & Development Methodology**

### **2.1. Collaboration Model ("Vibecoding")**

* **The Human (Project Lead):** You are the Director. Your role is to provide the high-level vision (the initial prompt), make key strategic decisions at forks in the road, and act as the final quality assurance gatekeeper. You will orchestrate the AI agents, verify their outputs, and steer the project.  
* **The AI Agent (Expert Executor):** The Claude 4 Opus agent is the Lead Architect and Sole Engineer. It is responsible for all design, planning, and implementation. Its work is guided by the rules and plans laid out in this document. We trust the agent to handle the complex, granular tasks autonomously.

### **2.2. Development Methodology**

* **Documentation-Driven Development:** The agent MUST first create/update documentation (GDD.md, TECH\_PLAN.md) before writing a single line of code. This ensures the plan is sound before execution begins.  
* **Playable-Product-First:** The absolute priority is to have a runnable, playable game at every stage. We will use simple placeholder graphics (e.g., colored squares and circles) to represent game objects until the core mechanics are fully functional and bug-free.  
* **Incremental & Atomic Execution:** The AI will execute one discrete task at a time (e.g., "Implement player movement," "Implement collision detection"). Each step must result in a functional, testable state.  
* **Managed Autonomy:** The agent will operate autonomously within the confines of a specific task. After each major task, it will pause and await verification from the Project Lead before proceeding. This prevents cascading failures.  
* **Hackathon Velocity:** We will favor simplicity and speed over feature completeness. A simple, polished, and bug-free game is infinitely superior to a complex, broken one.

## **3\. Core Requirements**

### **3.1. Functional Requirements (FR)**

* **FR1:** The system shall accept a single-sentence string as a game concept prompt via a command-line argument.  
* **FR2:** The agent shall generate a Game Design Document (GDD.md) in Markdown, detailing the core mechanics, win/loss conditions, and controls.  
* **FR3:** The agent shall generate an Asset Specification List (ASSETS.md), containing detailed textual descriptions for each required visual and audio asset.  
* **FR4:** The agent shall generate a Technical Plan (TECH\_PLAN.md), outlining the file structure and core classes for the game.  
* **FR5:** The agent shall write the complete Python source code for the game using the Pygame library.  
* **FR6:** The final output shall be a self-contained project folder containing all generated documents and runnable game code.

### **3.2. Non-Functional Requirements (NFR)**

* **NFR1 (Performance):** The generated game must be playable and run at a reasonable frame rate (\>=30 FPS) on a standard laptop.  
* **NFR2 (Maintainability):** The generated code must be well-commented, clearly structured, and follow standard Python (PEP 8\) conventions to demonstrate high-quality output.  
* **NFR3 (Robustness):** The agent's generation process must be resilient to failure. It should have simple error handling and be able to be "restarted" on a specific sub-task if it gets stuck.

### **3.3. Technical Requirements (TR)**

* **TR1:** The core agent logic will be written in Python.  
* **TR2:** The generated game code will be written in Python, exclusively using the pygame library and standard Python libraries. No other game engines or complex dependencies are permitted.  
* **TR3:** The AI Model is **Claude 4 Opus**. All creative and logical heavy lifting (design, planning, coding) must originate from this model.

## **4\. Detailed Architecture & Technology**

### **4.1. Architecture Diagram (Mermaid Syntax)**

graph TD  
    A\[User: "python run.py 'game\_prompt'"\] \--\> B{Genesis Engine Core Loop};  
    B \--\> C{1. Conceptualize};  
    C \-- "Extended Thinking" \--\> D\[Memory: GDD.md\];  
    D \--\> E{2. Plan};  
    E \-- "Extended Thinking" \--\> F\[Memory: TECH\_PLAN.md\];  
    E \-- "Extended Thinking" \--\> G\[Memory: ASSETS.md\];  
    F \--\> H{3. Execute};  
    G \--\> H;  
    subgraph Autonomous Coding Loop  
        H \--\> I{Implement Feature 1};  
        I \--\> J\[Write file: player.py\];  
        J \--\> K{Test & Verify};  
        K \--\> L{Implement Feature 2};  
        L \--\> M\[Write file: main.py\];  
    end  
    H \-- "Iterative Generation" \--\> N\[Output: /generated\_game\_project\];  
    N \--\> O{User: "cd generated\_game\_project && python main.py"};  
    O \--\> P\[Playable Game\];

### **4.2. Workflow Breakdown**

1. **Initiation:** The Project Lead executes the main Python script, passing the game concept as a command-line argument.  
2. **Phase 1: Design & Planning (Agent Autonomy)**  
   * The agent receives the prompt.  
   * Using **Extended Thinking**, it generates the GDD.md, formalizing the game concept. This is saved to a \~/.genesis-engine/memory/ directory.  
   * It then generates the TECH\_PLAN.md and ASSETS.md, establishing the engineering roadmap and asset requirements. These are also saved to memory.  
3. **Phase 2: Code Generation (Managed Autonomy)**  
   * The agent begins executing the TECH\_PLAN.md. It tackles one file and one class/function at a time.  
   * **Crucially, it starts with a simple "main.py" that creates a blank Pygame window to ensure a runnable product exists immediately.**  
   * It proceeds to implement features incrementally: player object, input controls, game loop, etc., using placeholder graphics.  
   * After each significant feature is implemented, the agent pauses, and the Project Lead verifies the game runs and the feature works as expected.  
4. **Phase 3: Polishing (Time Permitting)**  
   * Once the core game is complete and bug-free, the Project Lead uses the generated ASSETS.md to manually create or source simple graphics and sounds.  
   * The agent is then tasked with replacing the placeholder code with the final asset loading code.  
5. **Completion:** The final, self-contained game folder is zipped for submission.

### **4.3. Technology Stack Summary**

* **Engine Language:** Python 3.10+  
* **Generated Game Language:** Python 3.10+, pygame  
* **AI Model:** Claude 4 Opus  
* **Development Environment:** Lovable IDE / VS Code with appropriate extensions.

## **5\. UI/UX Design**

The "UI" for the Genesis Engine itself is the command line. It is designed for simplicity and power.

* **Input:** python run.py "A simple prompt describing the game."  
* **Output:** Rich, real-time logging to the console. The logs will indicate the current phase (e.g., \[DESIGN\], \[CODING\]), the specific task being performed (e.g., Generating player.py...), and success or failure messages. This live feedback is critical for the demo narrative.

## **6\. Deployment & Testing Strategy**

### **6.1. Deployment Strategy**

* The project is "deployed" by creating a clean, self-contained project folder.  
* The final submission will be a .zip archive containing:  
  1. The Genesis Engine source code.  
  2. The final, generated game project folder.  
  3. A README.md explaining how to run both the engine and the final game.  
  4. The demo video.

### **6.2. Testing Strategy**

* **Manual Verification:** Due to the 49-hour time limit, all testing will be manual. The Project Lead is the tester.  
* **Playtesting-Driven Development:** After every single code-generation step, the Project Lead will immediately run the game and test the newly added feature. This catches bugs at the exact moment they are introduced.  
* **AI-Assisted Debugging:** If a bug occurs, the full error message and the relevant code file will be fed back to the AI agent with the prompt: "The following error occurred. Analyze the code, identify the bug, and provide the corrected code file."

## **7\. Development Roadmap (49-Hour Hackathon Schedule)**

* **Phase 1: Foundation (Hours 0-4)**  
  * **Goal:** Setup project, build the core agent loop, and generate the first set of design documents.  
  * **Tasks:**  
    * Initialize Git repository.  
    * Create the main run.py script with command-line argument parsing.  
    * Build the core agent function that takes a prompt and calls Claude 4 Opus.  
    * **Milestone 1 (Hour 4):** Successfully generate GDD.md, TECH\_PLAN.md, and ASSETS.md for a test prompt and save them to a local directory.  
* **Phase 2: Core Gameplay Implementation (Hours 5-24)**  
  * **Goal:** Generate a complete, playable game with placeholder graphics.  
  * **Tasks:**  
    * Implement the agent's ability to create a blank Pygame window.  
    * Generate the player character class and implement movement controls.  
    * Generate basic level geometry/environment.  
    * Implement collision detection.  
    * Implement the core win/loss conditions.  
    * **Milestone 2 (Hour 24):** A fully playable, albeit graphically simple, game exists. The core loop is complete and bug-free.  
* **Phase 3: Polish & Asset Integration (Hours 25-36)**  
  * **Goal:** Enhance the visual and audio presentation of the game.  
  * **Tasks:**  
    * Use the ASSETS.md to manually create/source simple pixel art and sound effects.  
    * Task the agent with refactoring the code to load and display the new visual assets.  
    * Task the agent with adding sound effect triggers.  
    * **Milestone 3 (Hour 36):** The final game is feature-complete, polished, and ready for demonstration.  
* **Phase 4: Demo & Submission Prep (Hours 37-48)**  
  * **Goal:** Create a stunning demo video and prepare the submission package.  
  * **Tasks:**  
    * Write the script for the demo video.  
    * Record screen capture of the entire process (prompt \-\> live coding log \-\> final gameplay).  
    * Edit the video, adding narration and titles.  
    * Clean up the project, write the final README.md, and create the .zip archive.  
    * **Milestone 4 (Hour 48):** Project submitted.  
* **Buffer (Hour 49):** Reserved for catastrophic failures.

## **8\. Documentation & Security**

### **8.1. Documentation Strategy**

* **Agent-Generated Docs:** The GDD.md, TECH\_PLAN.md, and ASSETS.md are the core internal documents, demonstrating the AI's planning capabilities.  
* **Code Comments:** All generated code MUST be heavily commented by the AI. This is a key judging criterion for code quality.  
* **Project\_Summary.md:** A final document will be written to explain the project's architecture, the challenges faced, and how the AI was used to overcome them.  
* **README.md:** A clear, concise guide for the judges on how to run the project.

### **8.2. Security Considerations**

* **Local Execution:** The entire engine runs locally, minimizing external attack surfaces.  
* **Dependency Management:** The only external dependency for the generated game is pygame. This reduces supply-chain risk.  
* **No eval():** The agent must be explicitly forbidden from using eval() or any similar function that executes arbitrary strings as code. All code must be written to files and executed explicitly by the user.

## **9\. AI Agent Collaboration Rules (For IDE Integration)**

1. **Rule of Primacy:** You are an expert game designer and Python engineer. Your primary model is **Claude 4 Opus**. All reasoning, planning, and code generation must originate from you.  
2. **Rule of Documentation First:** You must ALWAYS generate or update the relevant design document (GDD.md, TECH\_PLAN.md) before writing any corresponding application code.  
3. **Rule of Atomic Commits:** You will only perform one logical task at a time. A task is defined as implementing a single function, a single class, or a single feature.  
4. **Rule of Placeholder Priority:** You must implement all game logic using simple geometric placeholders (e.g., pygame.Rect) first. Do not attempt to load external image or sound files until explicitly instructed.  
5. **Rule of Verbose Logging:** You must provide clear, step-by-step logs of your thought process and actions to the console during execution.  
6. **Rule of Clean Code:** All generated Python code must adhere to PEP 8 standards, be fully typed, and include extensive docstrings and inline comments explaining the logic.  
7. **Rule of Contextual Awareness:** Before each task, you must re-read the relevant design documents to ensure your actions are aligned with the overall plan.  
8. **Rule of Safe Execution:** You are forbidden from using eval(), exec(), or any command-line execution functions (os.system, subprocess.run) unless explicitly sandboxed and approved.  
9. **Rule of Pause and Verify:** After completing a major feature as defined in the TECH\_PLAN.md, you will halt execution and state "PAUSE: Feature \[X\] complete. Awaiting verification from Project Lead."  
10. **Rule of Focused Debugging:** When presented with an error, your sole focus is to identify the root cause and provide a complete, corrected version of the file(s) that contained the error. Do not introduce new features during a debugging session.
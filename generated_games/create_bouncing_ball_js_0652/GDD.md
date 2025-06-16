# Game Design Document: "Bounce Lab"

## 1. Game Title and Concept

**Title:** Bounce Lab  
**Tagline:** "Master the Art of Physics-Based Creation"

**Concept:** An interactive physics sandbox where players create and control bouncing ball animations using p5.js. Players can experiment with gravity, velocity, colors, and collision effects to create mesmerizing visual patterns and solve creative challenges.

## 2. Core Mechanics

### Primary Mechanics:
- **Ball Spawning:** Click to create new balls at cursor position
- **Physics Simulation:** Real-time gravity and velocity calculations
- **Collision Detection:** Balls bounce off canvas edges with energy loss
- **Trail System:** Optional visual trails showing ball paths

### Secondary Mechanics:
- **Parameter Adjustment:** Modify gravity, bounciness, and friction in real-time
- **Color Cycling:** Balls change color based on velocity or position
- **Size Variation:** Ball size affects mass and bounce behavior

## 3. Player Controls

| Input | Action |
|-------|--------|
| **Left Click** | Spawn new ball at cursor |
| **Right Click** | Remove nearest ball |
| **Spacebar** | Pause/Resume animation |
| **R Key** | Reset all balls |
| **↑↓ Arrow Keys** | Adjust gravity strength |
| **←→ Arrow Keys** | Adjust bounciness coefficient |
| **1-5 Number Keys** | Select ball size preset |
| **T Key** | Toggle trail visibility |

## 4. Win/Loss Conditions

### Challenge Modes:
1. **Pattern Match:** Recreate specific bounce patterns
2. **Target Practice:** Guide balls through goals using physics
3. **Zen Mode:** No win/loss - pure creative sandbox

### Success Metrics:
- Pattern accuracy percentage
- Time to complete challenges
- Creative achievements unlocked

## 5. Visual Style

### Aesthetic:
- **Minimalist Design:** Clean, geometric shapes on gradient backgrounds
- **Color Palette:** 
  - Background: Soft gradients (#1a1a2e → #16213e)
  - Balls: Vibrant neon colors with glow effects
  - UI: Subtle white/gray overlays

### Visual Features:
- Smooth anti-aliased rendering
- Motion blur on fast-moving balls
- Particle effects on collision
- Dynamic shadows based on ball height

## 6. Target Audience

### Primary Audience:
- **Age:** 10-35 years
- **Interests:** Programming, physics, creative coding, visual arts
- **Skill Level:** Beginners learning p5.js to advanced creative coders

### Secondary Audience:
- Educators teaching physics concepts
- Digital artists seeking inspiration
- Casual players enjoying satisfying physics simulations

## 7. Technical Requirements

### Development:
- **Framework:** p5.js (latest version)
- **Language:** JavaScript
- **IDE:** Any text editor (VS Code recommended)

### Performance:
- **Target FPS:** 60 fps
- **Max Balls:** 50 simultaneous balls
- **Browser Support:** Chrome, Firefox, Safari, Edge (latest versions)

### Code Structure:
```javascript
// Core components
- setup() // Initialize canvas and variables
- draw() // Main animation loop
- Ball class // Object-oriented ball entities
- Physics engine // Gravity and collision calculations
- UI Manager // Handle user inputs and display
```

### Deployment:
- **Platform:** Web browser-based
- **Hosting:** GitHub Pages or similar static hosting
- **File Size:** < 500KB total

---

*This GDD serves as a foundation for creating an engaging, educational, and visually appealing bouncing ball animation that showcases p5.js capabilities while providing both creative freedom and structured challenges.*
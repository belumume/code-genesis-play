# Game Design Document: Bounce Lab

## 1. Game Title and Concept

**Title:** Bounce Lab  
**Tagline:** "Master the Art of Physics Simulation"

**Concept:** An interactive physics sandbox where players experiment with bouncing ball animations, adjusting parameters in real-time to create mesmerizing patterns and complete creative challenges. Players learn basic physics concepts while creating beautiful, dynamic visual compositions.

## 2. Core Mechanics

### Primary Mechanics:
- **Ball Spawning:** Click to create new balls at cursor position
- **Physics Simulation:** 
  - Gravity affects vertical velocity
  - Energy loss on collision (dampening)
  - Horizontal momentum preservation
- **Parameter Adjustment:**
  - Gravity strength (0.1 - 2.0)
  - Bounce dampening (0.5 - 1.0)
  - Ball size (10px - 50px)
  - Initial velocity control

### Secondary Mechanics:
- **Trail System:** Balls leave fading trails showing motion paths
- **Color Modes:** 
  - Rainbow (hue based on velocity)
  - Gradient (based on height)
  - User-selected solid colors
- **Collision Effects:** Visual feedback on bounce (ripple effect)

## 3. Player Controls

| Control | Action |
|---------|--------|
| **Left Click** | Spawn ball at cursor |
| **Click + Drag** | Set initial velocity vector |
| **Right Click** | Clear all balls |
| **Space** | Pause/Resume simulation |
| **1-5 Keys** | Select preset configurations |
| **G Key** | Toggle gravity on/off |
| **T Key** | Toggle trails |
| **C Key** | Cycle color modes |
| **Mouse Wheel** | Adjust ball size |

## 4. Win/Loss Conditions

### Challenge Mode Goals:
- **Pattern Master:** Create specific bounce patterns
- **Precision Bounce:** Land balls in target zones
- **Juggler:** Keep X balls airborne for Y seconds
- **Artist:** Match reference patterns using trails

### Sandbox Mode:
- No win/loss conditions
- Focus on experimentation and creativity
- Share creations via screenshot/GIF export

## 5. Visual Style

**Aesthetic:** Clean, minimalist laboratory theme

### Visual Elements:
- **Background:** Subtle grid pattern (light gray on white)
- **Balls:** Smooth circles with soft shadows
- **Trails:** Semi-transparent, gradient fade
- **UI:** Floating glass-morphism panels
- **Effects:** 
  - Particle burst on collision
  - Subtle screen shake on heavy impacts
  - Glow effect on fast-moving balls

### Color Palette:
- Primary: Electric blue (#0080FF)
- Secondary: Warm orange (#FF6B35)
- Accent: Lime green (#32FF32)
- Neutral: Soft grays (#F0F0F0, #333333)

## 6. Target Audience

### Primary Audience:
- **Age:** 10-25 years
- **Interests:** 
  - Creative coding enthusiasts
  - Physics/STEM students
  - Digital art creators
- **Skill Level:** Beginner to intermediate programmers

### Secondary Audience:
- Educators teaching physics concepts
- Parents seeking educational entertainment
- Casual players enjoying satisfying physics simulations

## 7. Technical Requirements

### Development:
- **Framework:** p5.js (latest version)
- **Language:** JavaScript ES6+
- **Canvas Size:** Responsive (min 800x600px)
- **Frame Rate:** Target 60 FPS

### Browser Support:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Performance Targets:
- Handle up to 100 simultaneous balls
- Smooth animation on mid-range devices
- Mobile-responsive design
- Local storage for saving presets

### Key Features Implementation:
```javascript
// Core structure outline
class Ball {
  constructor(x, y, vx, vy, radius, color)
  update()
  display()
  checkBoundaryCollision()
}

class TrailSystem {
  addPoint(x, y)
  update()
  display()
}

class PhysicsEngine {
  applyGravity()
  calculateCollisions()
  updatePositions()
}
```

### Additional Libraries:
- **p5.gui** for parameter controls
- **p5.sound** for optional collision sounds
- **gif.js** for animation export
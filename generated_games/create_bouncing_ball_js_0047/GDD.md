# Game Design Document: Bounce Sphere

## 1. Game Title and Concept

**Title:** Bounce Sphere  
**Genre:** Interactive Physics Simulation / Casual Arcade  
**Platform:** Web Browser (p5.js)

**Core Concept:**  
A mesmerizing interactive bouncing ball experience where players can influence gravity, spawn multiple balls, and create dynamic visual effects. What starts as a simple physics demonstration evolves into an engaging sandbox for creativity and relaxation.

## 2. Core Mechanics

### Primary Mechanics
- **Physics-Based Movement:** Ball follows realistic gravity and momentum
- **Collision Detection:** Ball bounces off screen boundaries with energy loss
- **Gravity Manipulation:** Mouse position influences gravitational pull
- **Multi-Ball System:** Click to spawn additional balls (max 10)
- **Trail Effects:** Optional visual trails following ball movement

### Secondary Mechanics
- **Energy Decay:** Balls gradually lose momentum over time
- **Size Variation:** New balls spawn with random sizes (20-60px diameter)
- **Color Cycling:** Balls shift through HSB color spectrum based on velocity
- **Boundary Wrapping:** Optional mode where balls wrap around screen edges

## 3. Player Controls

| Input | Action |
|-------|--------|
| **Mouse Movement** | Influences gravity direction and strength |
| **Left Click** | Spawn new ball at cursor position |
| **Spacebar** | Reset all balls to center |
| **R Key** | Toggle trail effects |
| **G Key** | Toggle gravity mode (normal/reverse/off) |
| **C Key** | Clear all balls except one |

## 4. Win/Loss Conditions

**Win Conditions:**
- **Zen Mode:** No traditional win/loss - focus on relaxation and creativity
- **Challenge Mode:** Keep at least one ball moving for 60 seconds
- **Collector Mode:** Spawn and maintain 10 balls simultaneously for 30 seconds

**Loss Conditions:**
- **Challenge Mode:** All balls stop moving (velocity < 0.1)
- **Collector Mode:** Ball count drops below 5 before time limit

**Scoring System:**
- Points awarded for ball longevity
- Bonus multipliers for multiple active balls
- Style points for creating interesting patterns

## 5. Visual Style

### Art Direction
- **Aesthetic:** Minimalist, modern, calming
- **Color Palette:** Dynamic HSB spectrum with smooth transitions
- **Background:** Deep space gradient (dark blue to black)

### Visual Elements
- **Balls:** Smooth circles with subtle glow effects
- **Trails:** Fading particle streams (optional)
- **UI:** Clean, transparent overlays with rounded corners
- **Effects:** Gentle screen shake on hard collisions

### Animation Details
- Smooth 60fps movement
- Elastic collision responses
- Color transitions based on speed
- Subtle pulsing glow on ball spawn

## 6. Target Audience

### Primary Audience
- **Age Range:** 8-35 years
- **Demographics:** Students, casual gamers, stress-relief seekers
- **Psychographics:** Enjoys simple, meditative experiences

### Secondary Audience
- **Educators:** Physics demonstration tool
- **Developers:** p5.js learning reference
- **Artists:** Interactive visual inspiration

### Accessibility Features
- High contrast mode option
- Reduced motion settings
- Keyboard-only navigation
- Screen reader compatible UI

## 7. Technical Requirements

### Development Stack
- **Framework:** p5.js (v1.4.0+)
- **Language:** JavaScript (ES6+)
- **Hosting:** Static web hosting (GitHub Pages, Netlify)

### Browser Compatibility
- **Minimum:** Chrome 70+, Firefox 65+, Safari 12+
- **Mobile:** iOS Safari 12+, Chrome Mobile 70+
- **Performance Target:** 60fps on mid-range devices

### File Structure
```
bounce-sphere/
├── index.html
├── sketch.js
├── ball.js
├── physics.js
├── ui.js
└── assets/
    └── sounds/ (optional)
```

### Key Classes
- `Ball`: Position, velocity, color, collision methods
- `Physics`: Gravity calculation, collision detection
- `UI`: Control hints, score display, settings menu
- `Game`: Main game loop, state management

### Performance Considerations
- Object pooling for multiple balls
- Efficient collision detection algorithms
- Canvas optimization techniques
- Memory management for trail effects

---

**Development Timeline:** 2-3 weeks  
**Team Size:** 1-2 developers  
**Estimated Lines of Code:** 300-500 lines

This GDD provides a roadmap for transforming a simple bouncing ball into an engaging, interactive experience while maintaining the educational value of the original physics demonstration.
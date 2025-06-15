# Stellar Drift - Asset Specifications

## 1. Visual Assets

### Ship Sprites
- **Base Ship**
  - Size: 128x64 pixels
  - Layers: Base, Glow, Damage Overlay
  - Color Variants: 
    - Primary: Cyan (#00FFFF)
    - Secondary: Magenta (#FF00FF)
    - Accent: Yellow (#FFFF00)
  - Animation Frames: 
    - Idle: 4 frames
    - Boost: 6 frames
    - Damage: 3 frames

### Asteroid Assets
- **Procedural Texture Base**
  - Size: 256x256 pixels
  - Variants: 3 size classes (Small, Medium, Large)
  - Texture Style: Fractured rock with glowing cracks
  - Color Palette: 
    - Base: Dark Gray (#2C2C2C)
    - Crack Glow: Cyan (#00FFFF) with 50% opacity

### Background Elements
- **Parallax Star Field**
  - Layers: 3 depth layers
  - Particle Count: 200-500 per layer
  - Color Variants: White, Light Blue, Pale Purple
  - Movement: Slow scroll, randomized twinkle

### UI Elements
- **HUD Design**
  - Style: Holographic, minimalist
  - Color Scheme: Neon on transparent black
  - Key Components:
    - Health Bar: Gradient (Green → Red)
    - Boost Meter: Cyan pulse effect
    - Score Display: Floating, slight motion

## 2. Audio Assets

### Sound Effects
- **Ship Sounds**
  - Primary Fire: Sharp, digital pulse (0.2s)
  - Boost: Low-frequency whoosh
  - Damage: Metallic impact with electronic distortion

- **Interaction Sounds**
  - Power-Up Collect: Ascending chime
  - Asteroid Destruction: Explosive crunch
  - Near-Miss: Subtle wind whistle

### Music
- **Dynamic Soundtrack**
  - Base Tempo: 120 BPM
  - Layers: 
    - Ambient space synth
    - Rhythmic electronic beat
  - Intensity Scaling: 3 levels of complexity
  - File Format: OGG (compressed)

## 3. Technical Specifications

### File Formats
- **Sprites:** PNG (32-bit, transparent)
- **Audio:** OGG, WAV
- **Compression:** 
  - Images: Max 256KB
  - Audio: 192kbps

### Performance Optimization
- **Sprite Sheets**
  - Max Size: 2048x2048 pixels
  - Packed Efficiently
  - Mipmap Support

### Resolution Support
- **Base Design Resolution:** 1920x1080
- **Scaling:** 
  - Mobile: 720x1280
  - Desktop: Up to 4K
  - Responsive UI Elements

## 4. Style Guidelines

### Color Palette
- **Primary Colors**
  - Space Black: #0A0A1A
  - Neon Cyan: #00FFFF
  - Neon Magenta: #FF00FF
  - Accent Yellow: #FFFF00

### Design Principles
- **Aesthetic:** Neon-Noir Space
- **Visual Hierarchy**
  - Player Ship: Brightest Element
  - Asteroids: Muted, Textured
  - Background: Subtle, Parallax Depth

### Animation Principles
- **Motion Style**
  - Smooth Acceleration
  - Slight Electromagnetic Distortion
  - Particle Trails on Movement

### Accessibility Considerations
- **Color Blind Modes**
  - Alternative Texture Patterns
  - High Contrast Options
- **Size Considerations**
  - Minimum Touch Target: 44x44 pixels
  - Clear Visual Feedback
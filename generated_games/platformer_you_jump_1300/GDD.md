# Game Design Document: Cloud Hopper

## 1. Game Title and Concept

**Title:** Cloud Hopper

**Concept:** A whimsical vertical platformer where players control Luna, a young dreamweaver who must ascend through the sky realm by jumping on clouds to collect fallen stars and restore light to the night sky.

**Core Loop:** Jump → Collect Stars → Unlock New Heights → Face Greater Challenges

## 2. Core Mechanics

### Movement Mechanics
- **Cloud Jumping:** Clouds have different properties:
  - *Cumulus Clouds:* Solid, stable platforms
  - *Cirrus Clouds:* Thin, disappear after 2 seconds
  - *Storm Clouds:* Bounce players higher but damage if stayed on too long
  - *Rainbow Clouds:* Moving platforms that follow set paths

### Collection System
- **Stars:** Primary collectible (3 per level minimum to progress)
- **Stardust:** Currency for upgrades (5 stardust = 1 star)
- **Constellation Fragments:** Hidden collectibles that unlock bonus levels

### Power-ups
- **Wind Burst:** Double jump ability (temporary)
- **Cloud Shoes:** Walk on clouds 50% longer
- **Star Magnet:** Attracts nearby stars automatically

## 3. Player Controls

### Keyboard
- **Arrow Keys/WASD:** Movement
- **Spacebar:** Jump
- **Shift:** Dash (once unlocked)
- **E:** Activate power-up

### Gamepad
- **Left Stick:** Movement
- **A/X Button:** Jump
- **Right Trigger:** Dash
- **Y/Triangle:** Activate power-up

### Touch (Mobile)
- **Left side:** Virtual joystick
- **Right side:** Jump button
- **Swipe up:** Double jump
- **Top corner:** Power-up button

## 4. Win/Loss Conditions

### Win Conditions
- **Level Victory:** Collect minimum 3 stars and reach the Sky Gate
- **Perfect Clear:** Collect all stars and constellation fragments
- **Game Completion:** Restore all 7 constellation zones

### Loss Conditions
- **Fall Below Screen:** Lose one life
- **Time Limit:** Each level has a sunset timer (3-5 minutes)
- **Life Depletion:** Start with 3 lives, game over when all lost

### Progression
- Stars unlock new zones
- Total stars collected unlock cosmetic rewards
- Speed run times posted to leaderboards

## 5. Visual Style

### Art Direction
- **Style:** Hand-drawn 2.5D with parallax backgrounds
- **Color Palette:** Pastel purples, blues, and pinks with golden star accents
- **Inspiration:** Studio Ghibli clouds meets Ori's luminescent style

### Visual Elements
- **Backgrounds:** 4-layer parallax (stars, distant clouds, mid clouds, foreground)
- **Character Design:** Luna wears flowing robes that react to movement
- **Effects:** Particle trails from jumps, twinkling star collection, cloud puff animations

### UI Design
- Clean, minimal HUD with star counter and life indicator
- Constellation map as level select screen
- Dreamy, ethereal menu transitions

## 6. Target Audience

### Primary Audience
- **Age:** 8-35 years
- **Demographics:** Casual to mid-core gamers
- **Interests:** Platformers, relaxing games, completionists

### Secondary Audience
- **Family Players:** Parents playing with children
- **Speedrunners:** Time attack modes and leaderboards
- **Mobile Gamers:** Quick session-based gameplay

### Appeal Factors
- Low skill floor, high skill ceiling
- Non-violent, all-ages appropriate
- Relaxing yet challenging gameplay
- Short levels perfect for quick sessions

## 7. Technical Requirements

### Minimum Specifications

**PC:**
- OS: Windows 10, macOS 10.14, Ubuntu 18.04
- Processor: Dual Core 2.0 GHz
- Memory: 2 GB RAM
- Graphics: OpenGL 3.3 support
- Storage: 500 MB

**Mobile:**
- iOS 12.0+ / Android 8.0+
- 1 GB RAM
- 200 MB storage

### Recommended Specifications
- Quad Core processor
- 4 GB RAM
- Dedicated graphics card for 60 FPS

### Engine & Tools
- **Engine:** Unity 2022 LTS
- **Physics:** Unity's 2D physics system
- **Audio:** FMOD for dynamic music
- **Analytics:** Unity Analytics for player metrics

### Platform Features
- Cross-platform cloud saves
- Achievement system integration
- Controller support on all platforms
- Accessibility options (colorblind mode, button remapping)
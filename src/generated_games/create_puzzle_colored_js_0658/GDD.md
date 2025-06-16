# Game Design Document: ChromaDrop

## 1. Game Title and Concept

**Title:** ChromaDrop  
**Genre:** Puzzle / Match-3  
**Platform:** Mobile (iOS/Android), PC

**Core Concept:**  
ChromaDrop is a fast-paced falling block puzzle game where players must strategically position colorful geometric blocks to create matches of 3 or more adjacent blocks of the same color. As blocks fall from the top of the screen, players must think quickly to create combos and prevent the play field from filling up.

## 2. Core Mechanics

### Block System
- **Block Types:** 6 different colors (Red, Blue, Green, Yellow, Purple, Orange)
- **Block Shapes:** Single blocks, L-shapes, T-shapes, and straight lines (2-4 blocks)
- **Fall Speed:** Increases progressively with level advancement
- **Preview Window:** Shows next 3 upcoming block formations

### Matching Mechanics
- **Basic Match:** 3+ blocks of same color in horizontal, vertical, or diagonal line
- **Combo System:** 
  - 4 blocks = "Quad Clear" (2x points)
  - 5+ blocks = "Mega Clear" (3x points + special effect)
- **Chain Reactions:** Cleared blocks cause above blocks to fall, potentially creating new matches
- **Special Blocks:** 
  - Rainbow Block (matches any color)
  - Bomb Block (clears 3x3 area when matched)

### Scoring System
- Basic match: 100 points × number of blocks
- Combo multiplier: ×2 for consecutive matches
- Speed bonus: Extra points for quick placement
- Level multiplier: Current level × base score

## 3. Player Controls

### Mobile Controls
- **Swipe Left/Right:** Move falling block horizontally
- **Swipe Down:** Accelerate block fall (soft drop)
- **Tap:** Rotate block 90° clockwise
- **Double Tap:** Instant drop (hard drop)

### PC Controls
- **Arrow Keys:** Left/Right movement
- **Down Arrow:** Soft drop
- **Up Arrow/Z:** Rotate clockwise
- **X:** Rotate counter-clockwise
- **Spacebar:** Hard drop
- **P:** Pause

## 4. Win/Loss Conditions

### Victory Conditions
- **Classic Mode:** Achieve target score within time limit
- **Marathon Mode:** Survive as long as possible (no win state)
- **Puzzle Mode:** Clear predetermined board layouts
- **Challenge Mode:** Complete specific objectives (e.g., "Create 5 combos in 2 minutes")

### Loss Conditions
- **Game Over:** Blocks reach the top of the play field
- **Time Out:** Timer expires in timed modes
- **Move Limit:** Exceed maximum moves in puzzle mode

## 5. Visual Style

### Art Direction
- **Theme:** Modern, minimalist with vibrant neon colors
- **Blocks:** Glossy, semi-transparent with subtle particle effects
- **Background:** Dynamic gradient that shifts based on performance
- **UI:** Clean, flat design with smooth animations

### Visual Effects
- **Match Effects:** Blocks shatter into particles with color-matched explosions
- **Combo Effects:** Lightning bolts connect chain reactions
- **Special Effects:** Screen shake for mega clears, rainbow trails for special blocks

### Audio Design
- **Music:** Upbeat electronic soundtrack that intensifies with gameplay
- **SFX:** Satisfying "pop" sounds for matches, escalating pitch for combos
- **Feedback:** Audio cues for rotation, placement, and danger states

## 6. Target Audience

### Primary Audience
- **Age:** 13-35 years old
- **Demographics:** Casual gamers, puzzle enthusiasts
- **Platform Preference:** Mobile-first, secondary PC players
- **Gaming Experience:** Familiar with match-3 mechanics

### Secondary Audience
- **Competitive Players:** Leaderboard chasers, speedrunners
- **Nostalgic Gamers:** Fans of classic falling block puzzles
- **Quick Session Players:** Commuters, break-time gamers

## 7. Technical Requirements

### Minimum Specifications

**Mobile:**
- OS: iOS 12+ / Android 8+
- RAM: 2GB
- Storage: 150MB
- Network: Optional (for leaderboards)

**PC:**
- OS: Windows 10 / macOS 10.14 / Ubuntu 18.04
- RAM: 4GB
- Graphics: DirectX 11 compatible
- Storage: 200MB
- Resolution: 1280×720 minimum

### Development Stack
- **Engine:** Unity 2021.3 LTS
- **Programming:** C#
- **Backend:** Firebase (leaderboards, cloud saves)
- **Analytics:** Unity Analytics
- **Monetization:** Unity Ads (optional video ads for continues)

### Performance Targets
- 60 FPS on target devices
- Load time: <3 seconds
- Battery optimization for 2+ hours continuous play
- Offline mode support with cloud sync
# Game Design Document: Crystal Cosmos

## 1. Game Title and Concept

### Title: **Crystal Cosmos: Galactic Harvest**

### Concept Overview
Crystal Cosmos is a vibrant 2.5D space platformer where players control an intrepid astronaut-miner navigating through alien-infested asteroid fields and space stations to collect valuable cosmic crystals. Set in a colorful, retro-futuristic universe, players must use precision jumping, gravity manipulation, and quick reflexes to gather crystals while avoiding hostile alien creatures and environmental hazards.

### Core Gameplay Loop
1. Explore diverse space environments
2. Collect cosmic crystals to power your ship
3. Avoid or outmaneuver alien enemies
4. Reach the extraction point before oxygen runs out
5. Upgrade equipment between levels
6. Progress to more challenging sectors

## 2. Core Mechanics

### Movement Mechanics
- **Gravity Switching**: Players can reverse personal gravity to walk on ceilings and navigate complex level geometry
- **Jet-Pack Boost**: Limited fuel jet-pack for extended jumps and mid-air corrections
- **Magnetic Boots**: Allows walking on metallic surfaces at any angle
- **Zero-G Sections**: Float freely in space segments with momentum-based movement

### Collection System
- **Crystal Types**:
  - Blue Crystals: Common (1 point)
  - Green Crystals: Uncommon (5 points)
  - Red Crystals: Rare (10 points)
  - Rainbow Crystals: Ultra-rare (25 points + special abilities)
- **Crystal Magnetism**: Collected crystals create a small magnetic field, attracting nearby crystals

### Enemy Behaviors
- **Blob Aliens**: Patrol platforms in predictable patterns
- **Flying Sentinels**: Chase players when detected, but have limited pursuit range
- **Spike Crawlers**: Move along walls and ceilings, immune to gravity changes
- **Crystal Mimics**: Disguise as crystals, attack when approached
- **Boss Aliens**: Guard major crystal deposits with unique attack patterns

### Environmental Elements
- **Oxygen System**: Depleting oxygen meter adds urgency (refillable at O2 stations)
- **Force Fields**: Block paths until specific crystal quotas are met
- **Moving Platforms**: Navigate timing-based challenges
- **Warp Portals**: Teleport between sections of larger levels
- **Asteroid Fields**: Dynamic obstacles that move through levels

## 3. Player Controls

### Keyboard Controls (Default)
| Action | Key |
|--------|-----|
| Move Left/Right | A/D or Arrow Keys |
| Jump | Spacebar |
| Gravity Switch | W or Up Arrow |
| Jet-Pack Boost | Hold Shift |
| Interact | E |
| Pause | ESC |

### Gamepad Controls
| Action | Button |
|--------|--------|
| Move | Left Analog Stick |
| Jump | A/Cross Button |
| Gravity Switch | Y/Triangle Button |
| Jet-Pack Boost | Right Trigger |
| Interact | X/Square Button |
| Pause | Start/Options |

### Touch Controls (Mobile)
- Virtual D-Pad for movement
- On-screen buttons for jump, gravity, and boost
- Swipe gestures for quick gravity switches

## 4. Win/Loss Conditions

### Level Victory Conditions
- **Primary**: Reach the extraction point with minimum crystal quota (varies by level)
- **Secondary**: Collect all crystals in a level (100% completion)
- **Tertiary**: Complete level within time/oxygen limit for bonus rewards

### Level Failure Conditions
- Oxygen depletes completely
- Contact with lethal alien enemies (3 hit points system)
- Falling into space voids
- Crushed by moving obstacles

### Game Progression
- **Campaign Mode**: 50 levels across 5 different space sectors
- **Star Rating System**: 
  - 1 Star: Complete level
  - 2 Stars: Collect 75% of crystals
  - 3 Stars: Collect 100% crystals + time challenge
- **Endless Mode**: Procedurally generated levels with increasing difficulty

## 5. Visual Style

### Art Direction
**Style**: Vibrant, cartoon-inspired pixel art with modern lighting effects
- Bold, contrasting colors with neon accents
- Character designs inspired by 1950s retro-futurism
- Alien designs blend cute and menacing elements
- Backgrounds feature parallax scrolling nebulae and distant planets

### Visual Elements
- **Player Character**: Chunky astronaut suit with customizable colors
- **Crystals**: Glowing, faceted gems with particle effects
- **Aliens**: Bioluminescent creatures with smooth animations
- **Environments**: 
  - Metallic space stations with industrial details
  - Organic alien hives with pulsating walls
  - Crystalline caves with reflective surfaces
  - Abandoned mining facilities with rust and decay

### UI/UX Design
- **HUD**: Minimalist design showing oxygen, health, crystal count
- **Menus**: Holographic interfaces with subtle animations
- **Transitions**: Warp-style effects between levels
- **Feedback**: Screen shake, particle bursts, and color flashes for impacts

## 6. Target Audience

### Primary Audience
- **Age**: 10-35 years
- **Gaming Experience**: Casual to intermediate platformer players
- **Interests**: Retro gaming, space themes, collection-based gameplay

### Secondary Audience
- **Speedrunners**: Players seeking to optimize routes and times
- **Completionists**: Players who enjoy 100% collection challenges
- **Nostalgic Gamers**: Those who grew up with classic platformers

### Accessibility Features
- Colorblind modes for crystal differentiation
- Difficulty settings (Easy, Normal, Hard, Cosmic)
- Checkpoint system for younger players
- Optional aim-assist for jet-pack navigation

## 7. Technical Requirements

### Minimum System Requirements (PC)
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Processor**: Dual-core 2.0 GHz
- **Memory**: 4 GB RAM
- **Graphics**: DirectX 11 compatible, 1GB VRAM
- **Storage**: 2 GB available space
- **Sound**: DirectX compatible

### Recommended System Requirements (PC)
- **OS**: Windows 11, macOS 12, Ubuntu 22.04
- **Processor**: Quad-core 3.0 GHz
- **Memory**: 8 GB RAM
- **Graphics**: DirectX 12 compatible, 2GB VRAM
- **Storage**: 4 GB available space
- **Network**: Broadband for leaderboards and updates

### Platform Targets
- **Primary**: PC (Steam, Epic Games Store)
- **Secondary**: Nintendo Switch, PlayStation 5, Xbox Series X/S
- **Mobile**: iOS 14+, Android 10+

### Engine and Tools
- **Game Engine**: Unity 2022.3 LTS
- **Programming Languages**: C#
- **Art Pipeline**: Aseprite for pixel art, Spine for animations
- **Audio**: FMOD for dynamic sound implementation
- **Version Control**: Git with GitHub

### Performance Targets
- 60 FPS on recommended specifications
- 30 FPS minimum on minimum specifications
- Load times under 10 seconds between levels
- Instant respawn at checkpoints (<1 second)

---

**Document Version**: 1.0  
**Last Updated**: Current Date  
**Next Review**: After Alpha Milestone
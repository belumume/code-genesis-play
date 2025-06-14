# Game Design Document: Crystal Voyager

## 1. Game Title and Concept

### Title
**Crystal Voyager: Alien Frontier**

### Concept Overview
Crystal Voyager is a 2.5D space platformer where players control an intrepid astronaut explorer navigating through diverse alien worlds to collect rare energy crystals while avoiding hostile extraterrestrial creatures. Set in the year 2157, players must gather these crystals to power humanity's first intergalactic colony ship before the Earth's resources are depleted.

### Core Gameplay Loop
- Explore alien environments with varying gravity levels
- Collect energy crystals scattered throughout each level
- Avoid or outmaneuver alien enemies using platforming skills
- Unlock new abilities and equipment to access previously unreachable areas
- Complete levels within time limits to maximize rewards

## 2. Core Mechanics

### Movement Mechanics
- **Gravity Manipulation**: Each planet has different gravity levels (0.5x to 2x Earth gravity)
- **Jet Pack System**: Limited fuel that regenerates when grounded
- **Wall Jumping**: Stick to certain surfaces and leap between walls
- **Momentum Conservation**: Physics-based movement in low-gravity environments

### Crystal Collection System
- **Common Crystals** (Blue): 10 points each, abundant throughout levels
- **Rare Crystals** (Purple): 50 points each, hidden in challenging locations
- **Ultra Crystals** (Gold): 100 points each, one per level in extremely dangerous areas
- **Crystal Magnetism**: Collected crystals create a temporary magnetic field that attracts nearby crystals

### Enemy AI Behaviors
- **Patrollers**: Move in predictable patterns along platforms
- **Hunters**: Actively pursue the player when spotted
- **Ambushers**: Hide in environmental features and surprise attack
- **Swarmers**: Weak individually but attack in groups
- **Guardians**: Protect crystal clusters and have unique attack patterns

### Environmental Hazards
- Toxic atmosphere zones requiring timed traversal
- Unstable platforms that crumble after contact
- Energy barriers that pulse on and off
- Gravitational anomalies that alter movement
- Asteroid showers in space levels

## 3. Player Controls

### Keyboard Controls (Default)
| Action | Key |
|--------|-----|
| Move Left/Right | A/D or Arrow Keys |
| Jump | Spacebar |
| Double Jump | Spacebar (in air) |
| Jet Pack Boost | Hold Shift |
| Crouch/Slide | S or Down Arrow |
| Interact | E |
| Pause Menu | ESC |

### Gamepad Controls
| Action | Button |
|--------|--------|
| Move | Left Analog Stick |
| Jump | A/X Button |
| Double Jump | A/X (in air) |
| Jet Pack Boost | Right Trigger |
| Crouch/Slide | B/Circle |
| Interact | X/Square |
| Pause Menu | Start/Options |

### Special Abilities (Unlockable)
- **Phase Dash**: Quick teleport through thin walls (Right Mouse/R1)
- **Crystal Shield**: Temporary invincibility using collected crystals (Q/L1)
- **Gravity Flip**: Reverse personal gravity for 3 seconds (F/Triangle)

## 4. Win/Loss Conditions

### Level Victory Conditions
- **Primary**: Reach the extraction point with minimum crystal quota (varies by level)
- **Secondary**: Collect all crystals in the level (100% completion)
- **Tertiary**: Complete level under par time for speed bonus

### Level Failure Conditions
- Health depleted to zero (3 hits without shields)
- Fall into environmental void
- Timer expires (in timed challenge levels)
- Fail to meet minimum crystal quota at extraction

### Game Progression
- **Campaign Mode**: 5 worlds with 8 levels each (40 total levels)
- **Star Rating System**: 1-3 stars based on crystals collected, time, and no-damage bonus
- **Unlock System**: New worlds unlock after collecting enough total stars
- **New Game+**: Replay with increased difficulty and new crystal placements

## 5. Visual Style

### Art Direction
- **Overall Style**: Vibrant, stylized sci-fi with hand-painted textures
- **Color Palette**: Each world has distinct color themes
  - World 1 (Ice Moon): Blues, whites, and cyan
  - World 2 (Toxic Jungle): Greens, purples, and yellows
  - World 3 (Crystal Caverns): Deep purples, pinks, and bioluminescent accents
  - World 4 (Desert Planet): Oranges, reds, and sandy browns
  - World 5 (Space Station): Metallics, grays, and neon highlights

### Character Design
- **Player Character**: Sleek astronaut suit with customizable colors and patterns
- **Alien Enemies**: Diverse designs ranging from crystalline creatures to organic blob-like entities
- **Animation Style**: Smooth, fluid movements with exaggerated physics for gameplay clarity

### Environmental Design
- **Foreground**: Detailed platforms and interactive elements
- **Midground**: Main gameplay layer with parallax scrolling
- **Background**: Stunning alien vistas with multiple parallax layers
- **Lighting**: Dynamic lighting system with glowing crystals and atmospheric effects

### UI/UX Design
- **HUD**: Minimalist design showing health, crystal count, timer, and jet pack fuel
- **Menus**: Holographic interface style with smooth transitions
- **Visual Feedback**: Particle effects for collection, damage, and abilities

## 6. Target Audience

### Primary Audience
- **Age Range**: 10-35 years old
- **Gaming Experience**: Casual to intermediate platformer players
- **Interests**: Sci-fi themes, exploration, collection-based gameplay

### Secondary Audience
- **Speedrunners**: Players who enjoy optimizing routes and beating time records
- **Completionists**: Players who aim for 100% collection achievements
- **Nostalgic Gamers**: Those who enjoyed classic platformers like Mario, Sonic, and Metroid

### Accessibility Features
- Colorblind modes for crystal differentiation
- Difficulty settings (Easy, Normal, Hard, Nightmare)
- Control remapping options
- Optional aim assistance for jet pack navigation
- Subtitle options for story elements

## 7. Technical Requirements

### Minimum System Requirements
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Processor**: Intel Core i3-4340 / AMD FX-6300
- **Memory**: 4 GB RAM
- **Graphics**: NVIDIA GTX 660 / AMD Radeon HD 7870
- **DirectX**: Version 11
- **Storage**: 2 GB available space
- **Additional**: Controller support recommended

### Recommended System Requirements
- **OS**: Windows 11, macOS 12, Ubuntu 20.04
- **Processor**: Intel Core i5-8400 / AMD Ryzen 5 2600
- **Memory**: 8 GB RAM
- **Graphics**: NVIDIA GTX 1060 / AMD RX 580
- **DirectX**: Version 12
- **Storage**: 4 GB available space
- **Additional**: SSD for faster loading times

### Platform Targets
- **Primary**: PC (Steam, Epic Games Store)
- **Secondary**: Nintendo Switch, PlayStation 5, Xbox Series X/S
- **Future Consideration**: Mobile (iOS/Android) with adapted controls

### Engine and Tools
- **Game Engine**: Unity 2022.3 LTS
- **Programming Language**: C#
- **Version Control**: Git with GitHub
- **Art Pipeline**: Photoshop, Aseprite for sprites, Blender for 3D elements
- **Audio**: FMOD for dynamic audio implementation

### Performance Targets
- 60 FPS on recommended specifications
- 30 FPS minimum on minimum specifications
- Load times under 10 seconds between levels
- Support for 1080p, 1440p, and 4K resolutions
- Widescreen and ultrawide monitor support
# Asset Specifications: Crystal Cosmos: Galactic Harvest

## 1. Visual Assets

### Character Sprites

#### Player Character - Astronaut
- **Sprite Dimensions**: 64x64 pixels (base size)
- **Animation States**:
  - Idle (8 frames)
  - Walk (12 frames)
  - Jump (6 frames)
  - Fall (4 frames)
  - Jet-pack boost (8 frames)
  - Death (12 frames)
  - Gravity flip (6 frames)
  - Oxygen depleted (8 frames)
- **Color Palette**:
  - Primary Suit: #F5F5F5 (Off-white)
  - Secondary Suit: #FF6B35 (Orange accents)
  - Visor: #00D4FF (Cyan blue) with #FFFFFF highlight
  - Jet-pack: #808080 (Gray) with #FFD700 (Gold) flame
- **Customization Layers**:
  - Base suit (10 color variations)
  - Helmet decals (15 options)
  - Jet-pack models (5 variations)

#### Enemy Sprites

**Blob Aliens**
- **Dimensions**: 32x32 pixels
- **Animations**: Idle (6 frames), Move (8 frames), Attack (4 frames)
- **Colors**: 
  - Base: #7FFF00 (Chartreuse) with #90EE90 (Light green) highlights
  - Eyes: #FF1493 (Deep pink)
  - Translucency: 80% opacity

**Flying Sentinels**
- **Dimensions**: 48x48 pixels
- **Animations**: Patrol (12 frames), Chase (8 frames), Attack (6 frames)
- **Colors**:
  - Body: #9400D3 (Violet) with #DDA0DD (Plum) accents
  - Energy core: #00FFFF (Cyan) with glow effect
  - Wings: #4B0082 (Indigo) with transparency

**Spike Crawlers**
- **Dimensions**: 40x24 pixels
- **Animations**: Crawl (10 frames), Turn (4 frames), Strike (6 frames)
- **Colors**:
  - Carapace: #DC143C (Crimson) with #8B0000 (Dark red) shadows
  - Spikes: #C0C0C0 (Silver) with metallic sheen
  - Eyes: #FFFF00 (Yellow) dots

**Crystal Mimics**
- **Dimensions**: 32x32 pixels (crystal form), 48x48 pixels (revealed form)
- **Animations**: Disguised (subtle 4-frame shimmer), Transform (8 frames), Attack (6 frames)
- **Colors**: Match crystal colors until revealed, then #FF00FF (Magenta) with #8B008B (Dark magenta)

### Crystal Assets

**Crystal Specifications**
- **Base Dimensions**: 24x24 pixels
- **Glow Effect**: Additional 8-pixel radius soft glow
- **Animation**: 8-frame floating bob, 12-frame sparkle effect

| Crystal Type | Primary Color | Secondary Color | Glow Color | Particle Color |
|-------------|---------------|-----------------|------------|----------------|
| Blue | #0080FF | #004080 | #80C0FF | #FFFFFF |
| Green | #00FF00 | #008000 | #80FF80 | #C0FFC0 |
| Red | #FF0000 | #800000 | #FF8080 | #FFC0C0 |
| Rainbow | Animated gradient | #FFFFFF shine | Prismatic | Multi-color |

### Environmental Assets

#### Tileset Specifications
- **Tile Size**: 32x32 pixels
- **Tileset Categories**:

**Space Station Tiles**
- Metal floor variants (16 tiles)
- Wall sections (24 tiles including corners)
- Machinery details (20 tiles)
- **Color Scheme**: #4A4A4A (Dark gray), #7A7A7A (Medium gray), #ADADAD (Light gray)
- **Accent Colors**: #00FF00 (Green lights), #FF0000 (Red warnings), #0080FF (Blue panels)

**Alien Hive Tiles**
- Organic floor (12 tiles)
- Pulsating walls (16 tiles)
- Membrane barriers (8 tiles)
- **Color Scheme**: #4B0082 (Indigo), #8B008B (Dark magenta), #9932CC (Dark orchid)
- **Bioluminescence**: #00FFFF (Cyan), #7FFF00 (Chartreuse)

**Crystal Cave Tiles**
- Crystal formations (20 tiles)
- Rocky surfaces (16 tiles)
- Reflective floors (8 tiles)
- **Color Scheme**: #1C1C1C (Near black), #363636 (Dark gray)
- **Crystal Colors**: Match collectible crystal palette

#### Background Layers
- **Layer 1 (Far)**: 1920x1080 pixels, nebula and stars
- **Layer 2 (Mid)**: 1920x540 pixels, distant planets and asteroids
- **Layer 3 (Near)**: 1920x270 pixels, floating debris
- **Parallax Speeds**: 0.25x, 0.5x, 0.75x respectively

### UI Elements

#### HUD Components
- **Oxygen Meter**: 200x40 pixels
  - Frame: #C0C0C0 (Silver) with #808080 (Gray) border
  - Fill: Gradient from #00FF00 (Full) to #FF0000 (Empty)
- **Health Display**: 32x32 pixel heart icons
  - Full: #FF1493 (Deep pink)
  - Empty: #4A4A4A (Dark gray)
- **Crystal Counter**: 180x60 pixels
  - Font: Pixel font, 24pt
  - Color: #FFFFFF with #000000 outline

#### Menu Elements
- **Button States**: Normal, Hover, Pressed
- **Button Dimensions**: 240x60 pixels
- **Colors**:
  - Normal: #1E90FF (Dodger blue) with #FFFFFF text
  - Hover: #00BFFF (Deep sky blue) with #FFFFFF text
  - Pressed: #4169E1 (Royal blue) with #F0F0F0 text

## 2. Audio Assets

### Sound Effects

#### Player SFX
| Sound | Duration | Format | Description |
|-------|----------|---------|-------------|
| Jump | 0.3s | WAV 44.1kHz 16-bit | Pneumatic hiss |
| Land | 0.2s | WAV 44.1kHz 16-bit | Metallic thud |
| Jet-pack activate | 0.5s | WAV 44.1kHz 16-bit | Rocket ignition |
| Jet-pack loop | 2s loop | OGG | Continuous thrust |
| Gravity switch | 0.4s | WAV 44.1kHz 16-bit | Electronic whoosh |
| Footstep (metal) | 0.15s | WAV 44.1kHz 16-bit | 6 variations |
| Oxygen warning | 1s | WAV 44.1kHz 16-bit | Alarm beep |
| Death | 1.5s | WAV 44.1kHz 16-bit | Suit decompression |

#### Crystal SFX
| Sound | Duration | Format | Description |
|-------|----------|---------|-------------|
| Crystal collect (Blue) | 0.4s | WAV 44.1kHz 16-bit | Chime C5 |
| Crystal collect (Green) | 0.4s | WAV 44.1kHz 16-bit | Chime E5 |
| Crystal collect (Red) | 0.4s | WAV 44.1kHz 16-bit | Chime G5 |
| Crystal collect (Rainbow) | 0.8s | WAV 44.1kHz 16-bit | Arpeggio |
| Crystal magnetism | 0.6s | WAV 44.1kHz 16-bit | Electrical hum |

#### Enemy SFX
| Sound | Duration | Format | Description |
|-------|----------|---------|-------------|
| Blob movement | 0.3s | WAV 44.1kHz 16-bit | Wet squish |
| Sentinel alert | 0.6s | WAV 44.1kHz 16-bit | Digital screech |
| Crawler scuttle | 0.2s | WAV 44.1kHz 16-bit | Metallic clicks |
| Mimic reveal | 0.8s | WAV 44.1kHz 16-bit | Crystal shatter |
| Enemy damage | 0.4s | WAV 44.1kHz 16-bit | Alien squeal |

### Music Tracks

#### Background Music Specifications
- **Format**: OGG Vorbis, 192kbps
- **Style**: Synthwave/Chiptune hybrid
- **Tempo**: 120-140 BPM

| Track Name | Duration | Usage | Key Elements |
|------------|----------|-------|--------------|
| Main Theme | 3:30 | Title screen | Heroic melody, space ambience |
| Space Station | 2:45 loop | Station levels | Industrial, rhythmic |
| Alien Hive | 2:30 loop | Hive levels | Mysterious, organic |
| Crystal Caves | 2:45 loop | Cave levels | Ethereal, crystalline |
| Boss Battle | 2:00 loop | Boss encounters | Intense, driving |
| Victory Fanfare | 0:10 | Level complete | Triumphant chord |
| Game Over | 0:08 | Death screen | Descending melody |

## 3. Technical Specifications

### File Organization Structure
```
Assets/
├── Sprites/
│   ├── Player/
│   ├── Enemies/
│   ├── Crystals/
│   └── Effects/
├── Backgrounds/
│   ├── Parallax/
│   └── Static/
├── Tilesets/
│   ├── SpaceStation/
│   ├── AlienHive/
│   └── CrystalCave/
├── UI/
│   ├── HUD/
│   ├── Menus/
│   └── Icons/
├── Audio/
│   ├── SFX/
│   ├── Music/
│   └── Ambience/
└── Fonts/
```

### Sprite Sheet Specifications
- **Format**: PNG with transparency
- **Compression**: Lossless
- **Color Mode**: RGBA 32-bit
- **Max Texture Size**: 2048x2048 pixels
- **Padding**: 2 pixels between sprites

### Animation Guidelines
- **Frame Rate**: 12 FPS for character animations
- **Easing**: Use ease-in-out for organic movement
- **Looping**: Seamless loops for idle and movement animations

### Particle System Assets
- **Particle Sprites**: 8x8, 16x16, 32x32 pixels
- **Types**: Dust, sparkles, jet exhaust, crystal shards
- **Color Modes**: Additive blending for glows, normal for solids

## 4. Style Guidelines

### Visual Consistency Rules
1. **Pixel Density**: Maintain consistent pixel size across all assets
2. **Outline Style**: 1-pixel black outlines for characters, no outlines for backgrounds
3. **Shading**: 3-4 color ramp per surface, dithering for gradients
4. **Highlights**: Always from top-left light source
5. **Glow Effects**: Use additive blending, never pure white

### Color Usage Guidelines
1. **Saturation Levels**:
   - Characters: 80-100% saturation
   - Backgrounds: 40-60% saturation
   - UI Elements: 70-90% saturation
2. **Contrast Requirements**:
   - Minimum 4.5:1 for text
   - 3:1 for interactive elements
3. **Color Accessibility**:
   - Avoid pure red/green combinations
   - Include shape/pattern differentiation

### Audio Mixing Guidelines
1. **Volume Levels**:
   - SFX: -6 to -12 dB
   - Music: -12 to -18 dB
   - UI sounds: -9 to -15 dB
2. **Frequency Ranges**:
   - Keep critical SFX in 1-4 kHz range
   - Bass frequencies below 200 Hz for impact
3. **Spatial Audio**:
   - Pan enemy sounds based on position
   - Center player sounds
   - Subtle reverb for cave environments

### Quality Assurance Checklist
- [ ] All sprites align to pixel grid
- [ ] Animations loop seamlessly
- [ ] No color banding in gradients
- [ ] Audio files normalized to consistent levels
- [ ] File names follow naming convention
- [ ] Transparency properly implemented
- [ ] Compression artifacts minimal
- [ ] Color-blind modes tested

---

**Document Version**: 1.0  
**Last Updated**: Current Date  
**Asset Pipeline Contact**: [Art Director Name]  
**Technical Contact**: [Technical Artist Name]
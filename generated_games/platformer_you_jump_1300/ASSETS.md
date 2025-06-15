# Cloud Hopper Asset Specifications

## 1. Visual Assets

### Character Sprite: Luna
- **Type:** 2D Animated Sprite
- **Dimensions:** 256x256 pixels
- **Frames:** 12 (idle), 16 (running), 8 (jumping)
- **Color Palette:** 
  - Primary Robe: Soft Lavender (#B57EDC)
  - Secondary Trim: Pale Gold (#E6BE8A)
- **Animation Style:** Flowing, ethereal movements
- **File Format:** PNG with transparent background
- **Sprite Sheet:** 2048x2048 pixels

### Cloud Types
- **Cumulus Cloud**
  - Dimensions: 512x256 pixels
  - Color: Soft White (#F0F0F0) with subtle blue tint
  - Opacity: 80-90%
  - Physics: Solid platform sprite

- **Cirrus Cloud**
  - Dimensions: 384x192 pixels
  - Color: Translucent White (#FFFFFF with 50% opacity)
  - Fade Effect: 2-second dissolve animation

- **Storm Cloud**
  - Dimensions: 512x256 pixels
  - Color: Dark Gray (#708090) with electric blue highlights
  - Special Effect: Lightning particle system

### Background Layers
- **Layer 1 (Distant Stars):** 
  - Resolution: 2560x1440 pixels
  - Parallax Speed: 0.1x
  - Star Colors: Soft Gold, Silver, Pale Blue

- **Layer 2 (Cloud Backdrop):**
  - Resolution: 2560x1440 pixels
  - Parallax Speed: 0.3x
  - Color Palette: Gradient from Deep Purple (#4B0082) to Midnight Blue (#191970)

## 2. Audio Assets

### Music Tracks
- **Main Theme**
  - Genre: Ambient/Ethereal
  - Length: 3:30
  - Instruments: Soft piano, gentle synthesizers
  - File Format: OGG, WAV
  - Bitrate: 320 kbps

### Sound Effects
- **Jump Sound**
  - Duration: 0.2 seconds
  - Pitch: Slightly ascending
  - File Format: WAV
  - Volume: -12 dB

- **Star Collection**
  - Duration: 0.3 seconds
  - Effect: Twinkling chime
  - File Format: WAV
  - Volume: -10 dB

- **Cloud Interaction**
  - Different sounds for each cloud type
  - File Format: WAV
  - Bitrate: 44.1 kHz

## 3. Technical Specifications

### Sprite Technical Requirements
- **File Type:** PNG
- **Color Mode:** RGBA
- **Compression:** None/Minimal
- **Max File Size:** 2 MB per sprite sheet

### Performance Optimization
- **Texture Size:** Power of 2 (512x512, 1024x1024)
- **Draw Calls:** Minimize using sprite atlases
- **Polygon Count:** <1000 per complex sprite

## 4. Style Guidelines

### Color Palette
- **Primary Colors:**
  - Lavender: #B57EDC
  - Soft Gold: #E6BE8A
  - Midnight Blue: #191970
  - Soft White: #F0F0F0

### Typography
- **Main Font:** "Quicksand" (Google Fonts)
- **Sizes:** 
  - Header: 48px
  - Body: 24px
  - Small Text: 16px
- **Weight:** Light (300), Regular (400)

### Animation Principles
- **Easing:** Soft, dream-like transitions
- **Frame Rate:** 60 FPS for smooth animations
- **Particle Effects:** Subtle, glowing star particles

### Accessibility
- **Color Contrast Ratio:** Minimum 4.5:1
- **Colorblind Mode:** Alternative color schemes
- **Text Readability:** High contrast, clear typography
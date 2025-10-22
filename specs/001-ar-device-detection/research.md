# Research: AR Device Detection and Model Serving

**Feature**: 001-ar-device-detection
**Date**: 2025-10-19
**Purpose**: Resolve technical clarifications from Technical Context section and establish implementation approach

## Overview

This document resolves the "NEEDS CLARIFICATION" items identified in the Technical Context section of the implementation plan. Research focused on best practices for AR web applications serving USDZ (iOS) and GLB (Android) models with minimal dependencies and maximum performance.

---

## Decision 1: Frontend Approach

**Question**: Vanilla JavaScript vs minimal framework?

**Decision**: **Vanilla HTML/CSS/JavaScript** (zero external frameworks)

**Rationale**:
- **Simplicity**: No build step required, direct file editing
- **Performance**: Under 100KB total bundle size (HTML+CSS+JS)
- **Reliability**: Direct platform APIs (iOS Quick Look, Android Scene Viewer) are most reliable
- **Maintainability**: Simple code, no framework updates to track
- **Constitution Compliance**: Principle IV (Simplicity Over Cleverness) - avoid frameworks unless they solve real problems

**Alternatives Considered**:
- React/Vue/Svelte: Rejected - adds unnecessary complexity and bundle size for simple conditional rendering
- Static site generators (Eleventy, Hugo): Rejected - overkill for 3-4 static pages

**Implementation Details**:
- Feature detection using native Web APIs (`a.relList.supports("ar")`)
- Simple UA sniffing as fallback (`/iPad|iPhone|iPod/.test(navigator.userAgent)`)
- Conditional display via `style.display` manipulation
- No build tooling required

---

## Decision 2: Device Detection Library

**Question**: UAParser.js, Bowser, or alternative?

**Decision**: **No external device detection library** - use feature detection + minimal UA parsing

**Rationale**:
- **Feature Detection First**: Modern approach - `a.relList.supports("ar")` for iOS Quick Look
- **Simple UA Parsing**: `/iPad|iPhone|iPod/` regex sufficient for iOS/Android differentiation
- **Zero Dependencies**: Aligns with constitution principle IV (minimal dependencies)
- **Performance**: No library download (0 bytes overhead)
- **Privacy**: Aligns with User-Agent reduction trend in browsers

**Alternatives Considered**:
- UAParser.js (17.4M downloads/week): Rejected - comprehensive but unnecessary for basic iOS/Android detection
- Bowser (20.2M downloads/week): Rejected - simpler than UAParser but still adds 15-20KB for basic detection we can do in 5 lines

**Implementation Code**:
```javascript
// iOS detection
const iOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;

// Feature detection for Quick Look
const a = document.createElement("a");
const supportsQuickLook = iOS && a.relList && a.relList.supports("ar");

// Android detection
const Android = /Android/i.test(navigator.userAgent);
const androidVersion = parseFloat(navigator.userAgent.match(/Android (\d+\.\d+)/)?.[1]);
const supportsSceneViewer = Android && androidVersion >= 7.0;
```

---

## Decision 3: iOS Quick Look Integration

**Question**: How to trigger Quick Look from web page?

**Decision**: Use `<a rel="ar">` with `<img>` child element

**Rationale**:
- **Official Apple Standard**: Documented in AR Quick Look documentation
- **Reliability**: Direct browser support, no JavaScript required (but can be programmatic)
- **User Interaction Required**: Browsers require user tap/click for security
- **MIME Type Critical**: Must serve USDZ with `Content-Type: model/vnd.usdz+zip`

**Implementation Details**:

**Static Approach** (Simplest):
```html
<a rel="ar" href="/models/fire.usdz">
  <img src="/assets/images/fire-preview.png" alt="View Fire Model in AR">
</a>
```

**Programmatic Approach** (For conditional display):
```javascript
function launchIOSQuickLook(usdzUrl, previewImage) {
  const anchor = document.createElement('a');
  anchor.setAttribute('rel', 'ar');

  const img = document.createElement('img');
  img.src = previewImage;
  img.alt = 'View in AR';

  anchor.appendChild(img);
  anchor.setAttribute('href', usdzUrl);
  anchor.click(); // Must be in user click event handler
}
```

**Requirements**:
- HTTPS required (security context)
- USDZ MIME type must be configured on server
- `<img>` must be first child of `<a>` tag
- Compatible with iOS 12+ (iPhone 7+, iPad 5th gen+)

---

## Decision 4: Android Scene Viewer Integration

**Question**: Intent URL vs model-viewer web component?

**Decision**: **Intent URL** for direct Scene Viewer launch

**Rationale**:
- **Zero Dependencies**: No library required (model-viewer is ~500KB)
- **Direct Launch**: Launches Scene Viewer immediately without intermediate viewer
- **Performance**: No three.js overhead (model-viewer dependency)
- **Constitution Compliance**: Principle IV (minimal dependencies, no frameworks unless solving problems)

**Alternatives Considered**:
- model-viewer web component: Rejected - adds 500KB three.js dependency for preview that's not required
- Three.js custom implementation: Rejected - massive overhead for simple AR launch

**Implementation Code**:
```javascript
function launchAndroidSceneViewer(glbUrl, modelName) {
  const fileParam = encodeURIComponent(glbUrl);
  const titleParam = encodeURIComponent(modelName);
  const fallbackParam = encodeURIComponent(window.location.href);

  const intentUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${fileParam}&mode=ar_only&title=${titleParam}#Intent;scheme=https;package=com.google.android.googlequicksearchbox;action=android.intent.action.VIEW;S.browser_fallback_url=${fallbackParam};end;`;

  window.location.href = intentUrl;
}
```

**Requirements**:
- ARCore-compatible Android device (Android 7.0+)
- Google Play Services for AR installed
- GLB file format (GLTF binary)
- HTTPS required

---

## Decision 5: Fallback Strategy for Non-AR Devices

**Question**: Static images vs model-viewer vs three.js?

**Decision**: **Static preview images** with descriptive text

**Rationale**:
- **Zero Overhead**: No additional libraries or 3D rendering code
- **Fast Load**: Images can be optimized and cached
- **Accessibility**: Works with screen readers, text browsers
- **Constitution Compliance**: Principle III (progressive enhancement) and IV (simplicity)
- **Value Proposition**: For disaster scenario models, static views are sufficient for understanding content

**Alternatives Considered**:
- model-viewer: Rejected - 500KB overhead for 3D preview that doesn't add critical value
- Three.js: Rejected - even larger overhead, requires WebGL expertise
- Video previews: Considered - but larger file sizes than images for similar value

**Implementation**:
```html
<!-- Non-AR device view -->
<div class="fallback-content">
  <img src="/assets/images/fire-preview.png" alt="Fire disaster scenario 3D model">
  <h2>Fire Disaster Scenario</h2>
  <p>This 3D model demonstrates fire hazard patterns and safety zones. To view in augmented reality, scan this QR code with an iPhone (iOS 12+) or ARCore-compatible Android device.</p>
  <p class="system-requirements">AR viewing requires: iOS 12+ or Android 7.0+ with ARCore support</p>
</div>
```

**Preview Image Creation**:
- Use screenshots from AR viewers (Quick Look, Scene Viewer)
- Or render using Blender/Cinema 4D and export static images
- Optimize with WebP format (fallback to JPEG)
- Target size: Under 200KB per image

---

## Decision 6: Static Hosting Platform

**Question**: Netlify, Vercel, GitHub Pages, or Cloudflare Pages?

**Decision**: **Cloudflare Pages** (primary recommendation)

**Rationale**:
- **Unlimited Bandwidth**: Critical for 3D model downloads (fire.usdz is 37MB)
- **Large File Support**: 25MB max per file (supports existing models)
- **Global CDN**: Fast delivery worldwide
- **Free Tier**: Generous limits for educational/event use
- **MIME Type Configuration**: Supports custom headers via `_headers` file
- **Cost**: Free tier sufficient for moderate traffic

**Alternatives Considered**:
- Netlify: Good choice, but 100GB/month bandwidth limit on free tier (may be exceeded with 37MB models)
- Vercel: Good for Next.js apps, but bandwidth limits and optimized for app serving not large assets
- GitHub Pages: Rejected - no custom MIME type configuration (critical for USDZ)

**MIME Type Configuration** (Cloudflare Pages `_headers` file):
```
/*.usdz
  Content-Type: model/vnd.usdz+zip
  Cache-Control: public, max-age=31536000, immutable

/*.glb
  Content-Type: model/gltf-binary
  Cache-Control: public, max-age=31536000, immutable
```

**Alternative Architecture** (if bandwidth becomes issue):
- Host HTML/CSS/JS on Netlify/Vercel
- Store large 3D models on Cloudflare R2 (object storage) or AWS S3 + CloudFront

---

## Decision 7: Project Structure

**Question**: Build tooling vs pure static files?

**Decision**: **Pure static files** (no build step)

**Rationale**:
- **Simplicity**: Edit HTML/CSS/JS directly, deploy to hosting
- **Fast Development**: No build configuration or tooling to maintain
- **Zero Dependencies**: No package.json, node_modules, or build scripts
- **Constitution Compliance**: Principle IV (simplicity over cleverness)
- **Easy Deployment**: Drag-drop to hosting or simple git push

**File Structure**:
```
public/ (or root)
├── index.html                 # Landing page
├── fire/index.html            # Fire model AR page
├── flood/index.html           # Flood model AR page
├── quake/index.html           # Quake model AR page
├── models/
│   ├── fire.usdz              # Existing iOS model
│   ├── fire.glb               # To be created
│   ├── flood.usdz             # To be created
│   ├── flood.glb              # To be created
│   ├── quake.usdz             # Existing iOS model
│   └── quake.glb              # To be created
├── assets/
│   ├── css/styles.css
│   ├── js/ar-launcher.js      # Device detection and AR launch logic
│   └── images/
│       ├── fire-preview.png
│       ├── flood-preview.png
│       └── quake-preview.png
└── _headers                   # Cloudflare Pages MIME config
```

**Deployment**: `git push` to Cloudflare Pages or drag-drop to hosting dashboard

---

## Decision 8: Model File Preparation

**Question**: GLB conversion process for existing USDZ models?

**Decision**: Convert USDZ to GLB using Reality Converter or online tools

**Conversion Options**:

1. **Reality Converter** (macOS, free):
   - Import USDZ
   - Export as GLB
   - Apply Draco compression for smaller file size

2. **Online Tools**:
   - https://modelconverter.com/convert.html
   - Upload USDZ, download GLB

3. **Blender** (cross-platform, free):
   - Import USDZ (via USD plugin)
   - Export as GLB with Draco compression

**Optimization Targets**:
- USDZ: Under 50MB (constitution requirement)
- GLB: Under 20MB (constitution requirement)
- Current fire.usdz: 37MB (compliant)
- Target fire.glb: 10-15MB with Draco compression

**Quality Checks**:
- Test USDZ in iOS Quick Look on physical device
- Test GLB in Scene Viewer on physical Android device
- Verify scale (1 unit = 1 meter)
- Verify textures render correctly on both platforms

---

## Technical Decisions Summary

| Decision Area | Choice | Key Reason |
|--------------|--------|-----------|
| Frontend | Vanilla JS | Zero dependencies, maximum simplicity |
| Device Detection | Feature detection + basic UA parsing | No library needed, 5 lines of code |
| iOS Integration | `<a rel="ar">` with USDZ | Official Apple standard |
| Android Integration | Intent URL to Scene Viewer | Zero dependencies vs 500KB model-viewer |
| Fallback | Static preview images | Fast, accessible, sufficient value |
| Hosting | Cloudflare Pages | Unlimited bandwidth for large models |
| Build Tooling | None (pure static) | Simplicity, no build step |
| Model Format | USDZ + GLB dual format | Platform requirements (iOS/Android) |

---

## Implementation Approach

### Phase 1: Core Infrastructure
1. Create static HTML pages (`index.html`, `fire/index.html`, `flood/index.html`, `quake/index.html`)
2. Implement device detection JavaScript (`assets/js/ar-launcher.js`)
3. Add minimal CSS (`assets/css/styles.css`)
4. Configure MIME types (`_headers` file)

### Phase 2: iOS Support (P1 - MVP)
1. Link existing USDZ files from HTML
2. Add Quick Look launch buttons with feature detection
3. Create fallback preview images for iOS models
4. Test on physical iPhone devices

### Phase 3: Android Support (P2)
1. Convert USDZ to GLB (fire, flood, quake)
2. Implement Scene Viewer intent URL launch
3. Test on physical Android devices with ARCore

### Phase 4: Polish (P3)
1. Add fallback content for desktop browsers
2. Optimize preview images (WebP + JPEG fallback)
3. Add descriptive text and accessibility labels
4. Performance testing and optimization

---

## Open Questions / Future Considerations

1. **QR Code Updates**: Existing QR codes point to unknown URLs - will need to update to point to hosted pages
2. **Analytics**: May want to track AR launches (simple event tracking, no heavy analytics frameworks)
3. **Model Variants**: Future consideration - multiple scale options or customization
4. **Offline Support**: PWA/Service Worker could cache models (future enhancement if needed)

---

## Constitution Compliance Verification

✅ **Principle I (Device-Aware Serving)**: Automatic detection, appropriate format serving, no manual selection
✅ **Principle II (Performance First)**: <100KB initial load, lazy AR loading, optimized models
✅ **Principle III (Progressive Enhancement)**: Static images work everywhere, AR enhanced for capable devices
✅ **Principle IV (Simplicity)**: Zero dependencies, no framework, straightforward code
✅ **Principle V (Asset Quality)**: Dual-format validation, file size limits, version control

**All technical decisions align with project constitution.**

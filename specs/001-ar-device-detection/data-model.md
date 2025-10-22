# Data Model: AR Device Detection and Model Serving

**Feature**: 001-ar-device-detection
**Date**: 2025-10-19
**Purpose**: Define data structures and entities for AR model serving system

## Overview

This feature uses a **minimal data model** approach - no database or complex data structures required. The system operates on static files with simple JavaScript objects for runtime state management.

---

## Entity 1: AR Model Metadata

**Purpose**: Represents a 3D disaster scenario model with dual format support (iOS/Android)

**Storage**: Embedded in HTML or JavaScript as static data

**Attributes**:
```javascript
{
  id: string,              // Unique identifier (e.g., "fire", "flood", "quake")
  name: string,            // Display name (e.g., "Fire Disaster Scenario")
  description: string,     // Descriptive text for accessibility and fallback
  usdzPath: string,        // Path to iOS Quick Look model (e.g., "/models/fire.usdz")
  glbPath: string,         // Path to Android Scene Viewer model (e.g., "/models/fire.glb")
  previewImage: string,    // Path to fallback preview image (e.g., "/assets/images/fire-preview.png")
  scale: number,           // Model scale in meters (1 unit = 1 meter default)
  tested: {
    ios: boolean,          // Validated on physical iOS device
    android: boolean       // Validated on physical Android device
  }
}
```

**Example Data**:
```javascript
const models = {
  fire: {
    id: "fire",
    name: "Fire Disaster Scenario",
    description: "3D model demonstrating fire hazard patterns, spread zones, and safety evacuation routes for emergency preparedness training.",
    usdzPath: "/models/fire.usdz",
    glbPath: "/models/fire.glb",
    previewImage: "/assets/images/fire-preview.png",
    scale: 1.0,
    tested: {
      ios: true,
      android: false  // Will be true after GLB conversion and testing
    }
  },
  flood: {
    id: "flood",
    name: "Flood Disaster Scenario",
    description: "3D model showing flood water levels, affected infrastructure, and safe zones for flood emergency planning.",
    usdzPath: "/models/flood.usdz",
    glbPath: "/models/flood.glb",
    previewImage: "/assets/images/flood-preview.png",
    scale: 1.0,
    tested: {
      ios: false,  // USDZ needs to be created
      android: false
    }
  },
  quake: {
    id: "quake",
    name: "Earthquake Disaster Scenario",
    description: "3D model illustrating seismic damage patterns, structural vulnerabilities, and emergency shelter locations.",
    usdzPath: "/models/quake.usdz",
    glbPath: "/models/quake.glb",
    previewImage: "/assets/images/quake-preview.png",
    scale: 1.0,
    tested: {
      ios: true,
      android: false  // GLB needs to be created and tested
    }
  }
};
```

**Validation Rules**:
- `id` must be unique across all models
- `usdzPath` must point to valid USDZ file (<50MB)
- `glbPath` must point to valid GLB file (<20MB)
- `previewImage` must be optimized image (<200KB)
- `scale` should maintain consistency (1.0 recommended)
- Both iOS and Android `tested` flags must be `true` before production deployment

**Relationships**:
- One AR Model per disaster scenario
- No relationships between models (independent entities)

---

## Entity 2: Device Detection Result

**Purpose**: Captures device platform information and AR capability status

**Storage**: Runtime only (JavaScript object, not persisted)

**Attributes**:
```javascript
{
  platform: string,         // "ios" | "android" | "desktop" | "unknown"
  arCapable: boolean,       // Can this device launch AR experiences?
  arMethod: string | null,  // "quicklook" | "sceneviewer" | null
  userAgent: string,        // Raw user agent string (for debugging)
  features: {
    quickLookSupported: boolean,  // iOS Quick Look available
    sceneViewerSupported: boolean, // Android Scene Viewer available
    webxrSupported: boolean        // WebXR API available (future)
  }
}
```

**Detection Logic**:
```javascript
function detectDevice() {
  const ua = navigator.userAgent;
  const iOS = /iPad|iPhone|iPod/.test(ua) && !window.MSStream;
  const Android = /Android/i.test(ua);

  // iOS Quick Look feature detection
  const a = document.createElement("a");
  const quickLookSupported = iOS && a.relList && a.relList.supports("ar");

  // Android Scene Viewer support (approximate)
  const androidVersion = Android ? parseFloat(ua.match(/Android (\d+\.\d+)/)?.[1]) : 0;
  const sceneViewerSupported = Android && androidVersion >= 7.0;

  // WebXR (future consideration)
  const webxrSupported = 'xr' in navigator && 'isSessionSupported' in navigator.xr;

  // Determine platform and method
  let platform = "unknown";
  let arCapable = false;
  let arMethod = null;

  if (quickLookSupported) {
    platform = "ios";
    arCapable = true;
    arMethod = "quicklook";
  } else if (sceneViewerSupported) {
    platform = "android";
    arCapable = true;
    arMethod = "sceneviewer";
  } else if (iOS || Android) {
    platform = iOS ? "ios" : "android";
    arCapable = false;  // Device lacks AR capability
    arMethod = null;
  } else {
    platform = "desktop";
    arCapable = false;
    arMethod = null;
  }

  return {
    platform,
    arCapable,
    arMethod,
    userAgent: ua,
    features: {
      quickLookSupported,
      sceneViewerSupported,
      webxrSupported
    }
  };
}
```

**Usage**:
```javascript
const deviceInfo = detectDevice();

if (deviceInfo.arCapable) {
  if (deviceInfo.arMethod === "quicklook") {
    showIOSARButton();
  } else if (deviceInfo.arMethod === "sceneviewer") {
    showAndroidARButton();
  }
} else {
  showFallbackContent();
}
```

**Validation**:
- `platform` must be one of: "ios", "android", "desktop", "unknown"
- `arCapable` must be boolean
- `arMethod` must be one of: "quicklook", "sceneviewer", null
- `features` flags must all be boolean

---

## Entity 3: AR Launch Event

**Purpose**: Tracks AR launch attempts for debugging and analytics (optional)

**Storage**: Client-side only (console logging or optional analytics)

**Attributes**:
```javascript
{
  timestamp: Date,          // When AR launch was triggered
  modelId: string,          // Which model was launched (e.g., "fire")
  platform: string,         // "ios" | "android"
  method: string,           // "quicklook" | "sceneviewer"
  success: boolean,         // Did the launch succeed? (approximation)
  errorMessage: string | null,  // Error if launch failed
  userAgent: string         // Device UA for debugging
}
```

**Example Event**:
```javascript
{
  timestamp: new Date("2025-10-19T14:30:00Z"),
  modelId: "fire",
  platform: "ios",
  method: "quicklook",
  success: true,
  errorMessage: null,
  userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)..."
}
```

**Usage** (Optional Analytics):
```javascript
function trackARLaunch(modelId, deviceInfo) {
  const event = {
    timestamp: new Date(),
    modelId,
    platform: deviceInfo.platform,
    method: deviceInfo.arMethod,
    success: true,  // Assume success if no error thrown
    errorMessage: null,
    userAgent: deviceInfo.userAgent
  };

  // Log to console (development)
  console.log("AR Launch Event:", event);

  // Optional: Send to analytics (future)
  // analytics.track("ar_launch", event);
}
```

**Notes**:
- This entity is **optional** and not required for MVP
- Useful for debugging device compatibility issues
- Could be extended to actual analytics service in future
- No persistence required (ephemeral events)

---

## Data Flow

### User Journey: iOS Device

```
1. User scans QR code → loads /fire/ page
   └─> Page loads HTML with embedded model metadata

2. JavaScript detects device
   └─> detectDevice() returns {platform: "ios", arCapable: true, arMethod: "quicklook"}

3. Page shows Quick Look button
   └─> <a rel="ar" href="/models/fire.usdz">View in AR</a>

4. User taps button
   └─> iOS launches Quick Look with fire.usdz

5. (Optional) Log AR launch event
   └─> trackARLaunch("fire", deviceInfo)
```

### User Journey: Android Device

```
1. User scans QR code → loads /fire/ page
   └─> Page loads HTML with embedded model metadata

2. JavaScript detects device
   └─> detectDevice() returns {platform: "android", arCapable: true, arMethod: "sceneviewer"}

3. Page shows Scene Viewer button
   └─> <button onclick="launchSceneViewer()">View in AR</button>

4. User taps button
   └─> JavaScript constructs intent URL with /models/fire.glb
   └─> window.location.href = intent URL
   └─> Android launches Scene Viewer

5. (Optional) Log AR launch event
   └─> trackARLaunch("fire", deviceInfo)
```

### User Journey: Desktop Browser

```
1. User visits /fire/ page directly
   └─> Page loads HTML with embedded model metadata

2. JavaScript detects device
   └─> detectDevice() returns {platform: "desktop", arCapable: false, arMethod: null}

3. Page shows fallback content
   └─> Static preview image + descriptive text

4. No AR launch (no button shown)
```

---

## File System Data Structure

Since this is a static site, the "data model" is primarily represented through the file system structure:

```
models/
├── fire.usdz           # Binary USDZ file (37MB) - iOS format
├── fire.glb            # Binary GLB file (~15MB target) - Android format
├── flood.usdz          # To be created
├── flood.glb           # To be created
├── quake.usdz          # Binary USDZ file (46MB) - iOS format
└── quake.glb           # To be created

assets/images/
├── fire-preview.png    # Static fallback (target: <200KB)
├── flood-preview.png   # To be created
└── quake-preview.png   # To be created

Fire page: /fire/index.html
Flood page: /flood/index.html
Quake page: /quake/index.html
```

**File Naming Convention**:
- Model files: `{model-id}.{extension}` (lowercase, no spaces)
- Preview images: `{model-id}-preview.{extension}`
- Page directories: `/{model-id}/` (clean URL routing)

---

## State Management

**No complex state management required.** The system operates with:

1. **Static configuration** (AR model metadata in HTML/JS)
2. **Runtime detection** (device capabilities, computed once on page load)
3. **Conditional rendering** (show/hide AR buttons based on capabilities)

**Example State in HTML**:
```html
<!-- fire/index.html -->
<script>
  // Static model data (embedded in page)
  const MODEL = {
    id: "fire",
    name: "Fire Disaster Scenario",
    description: "3D model demonstrating fire hazard patterns...",
    usdzPath: "/models/fire.usdz",
    glbPath: "/models/fire.glb",
    previewImage: "/assets/images/fire-preview.png"
  };

  // Runtime device detection (computed on load)
  const device = detectDevice();

  // Conditional UI (based on device capabilities)
  window.addEventListener('DOMContentLoaded', () => {
    if (device.arMethod === "quicklook") {
      document.getElementById('ios-ar-button').style.display = 'block';
      document.getElementById('ios-ar-button').href = MODEL.usdzPath;
    } else if (device.arMethod === "sceneviewer") {
      document.getElementById('android-ar-button').style.display = 'block';
      document.getElementById('android-ar-button').onclick = () => {
        launchSceneViewer(MODEL.glbPath, MODEL.name);
      };
    } else {
      document.getElementById('fallback-content').style.display = 'block';
    }
  });
</script>
```

---

## Validation Requirements

Before deploying to production, validate:

### Model Files
- [ ] All USDZ files exist and are <50MB
- [ ] All GLB files exist and are <20MB
- [ ] Models maintain consistent scale (1 unit = 1 meter)
- [ ] Textures render correctly in both formats

### Preview Images
- [ ] All preview images exist
- [ ] Images are optimized (<200KB each)
- [ ] Images accurately represent the AR models

### Device Testing
- [ ] iOS Quick Look tested on physical iPhone (iOS 12+)
- [ ] Android Scene Viewer tested on physical ARCore device (Android 7.0+)
- [ ] Fallback content tested on desktop browser
- [ ] Fallback content tested on older mobile devices without AR

### Metadata Completeness
- [ ] All models have descriptive text
- [ ] All descriptions include accessibility information
- [ ] All pages have unique titles and meta tags

---

## Future Extensions (Out of Scope for MVP)

Potential data model additions for future features:

1. **User Preferences**: Remember user's preferred view mode
2. **Analytics Data**: Aggregate AR launch metrics
3. **Model Variants**: Multiple scale options or customization
4. **Offline Cache**: Service Worker cache manifest for PWA support
5. **CMS Integration**: Dynamic model library with admin interface

**Current Decision**: Keep it simple - static data only for MVP

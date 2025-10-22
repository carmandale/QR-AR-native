# API Contracts: AR Device Detection and Model Serving

**Feature**: 001-ar-device-detection
**Date**: 2025-10-19
**Type**: Static Web Application (No Backend API)

## Overview

This feature is a **pure static website** with **no traditional backend API**. There are no REST endpoints, GraphQL queries, or server-side processing. However, there are important "contracts" in the form of:

1. **File Serving Contracts** - How static files must be served
2. **Client-Side Interfaces** - JavaScript module APIs
3. **Platform Integration Contracts** - iOS Quick Look and Android Scene Viewer requirements

---

## 1. File Serving Contracts

These are the critical requirements for how the static hosting platform must serve files.

### Contract: USDZ File Serving

**Purpose**: Ensure iOS Quick Look can properly load AR models

**HTTP Headers Required**:
```http
Content-Type: model/vnd.usdz+zip
Cache-Control: public, max-age=31536000, immutable
Content-Length: [file size in bytes]
```

**URL Pattern**: `/models/{model-id}.usdz`

**Examples**:
- `/models/fire.usdz`
- `/models/flood.usdz`
- `/models/quake.usdz`

**Requirements**:
- Files MUST be served over HTTPS
- MIME type MUST be exactly `model/vnd.usdz+zip` (iOS requirement)
- Files MUST be accessible without authentication
- Files MUST support range requests for streaming (optional but recommended)
- Maximum file size: 50MB (constitution requirement)

**Validation**:
```bash
# Check MIME type
curl -I https://example.com/models/fire.usdz

# Expected response:
HTTP/2 200
content-type: model/vnd.usdz+zip
cache-control: public, max-age=31536000, immutable
content-length: 38797312
```

---

### Contract: GLB File Serving

**Purpose**: Ensure Android Scene Viewer can properly load AR models

**HTTP Headers Required**:
```http
Content-Type: model/gltf-binary
Cache-Control: public, max-age=31536000, immutable
Content-Length: [file size in bytes]
```

**URL Pattern**: `/models/{model-id}.glb`

**Examples**:
- `/models/fire.glb`
- `/models/flood.glb`
- `/models/quake.glb`

**Requirements**:
- Files MUST be served over HTTPS
- MIME type MUST be `model/gltf-binary` (Android recommendation)
- Files MUST be accessible without authentication
- Files MUST support CORS headers if served from different origin
- Maximum file size: 20MB (constitution requirement)

**CORS Headers** (if needed):
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET
```

**Validation**:
```bash
# Check MIME type
curl -I https://example.com/models/fire.glb

# Expected response:
HTTP/2 200
content-type: model/gltf-binary
cache-control: public, max-age=31536000, immutable
access-control-allow-origin: *
content-length: 15728640
```

---

### Contract: Preview Image Serving

**Purpose**: Serve fallback preview images for non-AR devices

**HTTP Headers Required**:
```http
Content-Type: image/png (or image/jpeg, image/webp)
Cache-Control: public, max-age=31536000, immutable
Content-Length: [file size in bytes]
```

**URL Pattern**: `/assets/images/{model-id}-preview.{extension}`

**Examples**:
- `/assets/images/fire-preview.png`
- `/assets/images/flood-preview.webp`
- `/assets/images/quake-preview.jpg`

**Requirements**:
- Images MUST be optimized (<200KB each)
- Images SHOULD support WebP with JPEG/PNG fallback
- Images MUST have descriptive alt text in HTML
- Images MUST be served over HTTPS

---

## 2. Client-Side JavaScript Interfaces

These are the contracts for JavaScript modules used in the application.

### Interface: Device Detection Module

**File**: `assets/js/device-detection.js`

**Exported Functions**:

#### `detectDevice(): DeviceInfo`

Detects device platform and AR capabilities.

**Returns**: `DeviceInfo` object
```typescript
interface DeviceInfo {
  platform: "ios" | "android" | "desktop" | "unknown";
  arCapable: boolean;
  arMethod: "quicklook" | "sceneviewer" | null;
  userAgent: string;
  features: {
    quickLookSupported: boolean;
    sceneViewerSupported: boolean;
    webxrSupported: boolean;
  };
}
```

**Example Usage**:
```javascript
import { detectDevice } from './device-detection.js';

const device = detectDevice();
console.log(device);
// {
//   platform: "ios",
//   arCapable: true,
//   arMethod: "quicklook",
//   userAgent: "Mozilla/5.0 (iPhone; ...)",
//   features: {
//     quickLookSupported: true,
//     sceneViewerSupported: false,
//     webxrSupported: false
//   }
// }
```

**Contract Guarantees**:
- MUST return a valid `DeviceInfo` object
- `platform` MUST be one of the specified string literals
- `arCapable` MUST correctly reflect device AR capability
- `arMethod` MUST match platform (quicklook for iOS, sceneviewer for Android)
- MUST be safe to call multiple times (idempotent)
- MUST work without external dependencies (pure vanilla JS)

---

### Interface: AR Launcher Module

**File**: `assets/js/ar-launcher.js`

**Exported Functions**:

#### `launchIOSQuickLook(usdzUrl: string, previewImage?: string): void`

Launches iOS Quick Look with the specified USDZ model.

**Parameters**:
- `usdzUrl` (required): Absolute or relative URL to USDZ file
- `previewImage` (optional): URL to preview image (shown while loading)

**Behavior**:
- Creates temporary `<a rel="ar">` element
- Programmatically triggers click event
- MUST be called within user interaction event (security requirement)
- Throws error if not on iOS device or Quick Look not supported

**Example Usage**:
```javascript
import { launchIOSQuickLook } from './ar-launcher.js';

document.getElementById('ar-button').addEventListener('click', () => {
  launchIOSQuickLook('/models/fire.usdz', '/assets/images/fire-preview.png');
});
```

**Error Handling**:
```javascript
try {
  launchIOSQuickLook('/models/fire.usdz');
} catch (error) {
  console.error('Quick Look launch failed:', error);
  // Fallback: show error message to user
}
```

---

#### `launchAndroidSceneViewer(glbUrl: string, modelName: string): void`

Launches Android Scene Viewer with the specified GLB model.

**Parameters**:
- `glbUrl` (required): Absolute or relative URL to GLB file (will be converted to absolute)
- `modelName` (required): Display name for the model (shown in Scene Viewer)

**Behavior**:
- Constructs `intent://` URL for Scene Viewer
- Redirects browser to intent URL (launches native app)
- MUST be called within user interaction event
- Falls back to current page if Scene Viewer not available

**Example Usage**:
```javascript
import { launchAndroidSceneViewer } from './ar-launcher.js';

document.getElementById('ar-button').addEventListener('click', () => {
  launchAndroidSceneViewer('/models/fire.glb', 'Fire Disaster Scenario');
});
```

**Intent URL Format**:
```
intent://arvr.google.com/scene-viewer/1.0
  ?file={encoded_glb_url}
  &mode=ar_only
  &title={encoded_model_name}
#Intent;
  scheme=https;
  package=com.google.android.googlequicksearchbox;
  action=android.intent.action.VIEW;
  S.browser_fallback_url={encoded_current_page};
end;
```

---

## 3. Platform Integration Contracts

These define how the application integrates with native AR platforms.

### Contract: iOS Quick Look Integration

**Platform**: iOS 12+ (iPhone 7+, iPad 5th gen+)

**Trigger Mechanism**: HTML `<a rel="ar">` element

**Required HTML Structure**:
```html
<a rel="ar" href="/models/fire.usdz">
  <img src="/assets/images/fire-preview.png" alt="View in AR">
</a>
```

**Requirements**:
- `rel="ar"` attribute MUST be present on anchor element
- `<img>` element MUST be first child of anchor
- `href` MUST point to valid USDZ file with correct MIME type
- User interaction (tap/click) required to launch
- HTTPS required for security

**Optional URL Parameters**:
```html
<!-- Disable content scaling -->
<a rel="ar" href="/models/fire.usdz?allowsContentScaling=0">

<!-- Set canonical web page URL -->
<a rel="ar" href="/models/fire.usdz?canonicalWebPageURL=https://example.com/fire">
```

**Feature Detection**:
```javascript
const a = document.createElement("a");
const supported = a.relList && a.relList.supports("ar");
```

**Success Criteria**:
- Quick Look launches full-screen AR viewer
- Model displays at correct scale (1 unit = 1 meter)
- Textures render correctly
- User can place model in physical space
- User can take screenshots/videos within Quick Look

---

### Contract: Android Scene Viewer Integration

**Platform**: Android 7.0+ with ARCore support

**Trigger Mechanism**: Intent URL redirect

**Intent URL Structure**:
```
intent://arvr.google.com/scene-viewer/1.0
  ?file={absolute_url_to_glb}
  &mode=ar_only
  &title={model_title}
#Intent;
  scheme=https;
  package=com.google.android.googlequicksearchbox;
  action=android.intent.action.VIEW;
  S.browser_fallback_url={fallback_url};
end;
```

**Parameters**:
- `file`: URL-encoded absolute URL to GLB file (required)
- `mode`: `ar_only` (AR mode) or `3d_preferred` (3D viewer with AR option)
- `title`: URL-encoded model name (optional, shown in Scene Viewer)
- `browser_fallback_url`: URL to return to if Scene Viewer unavailable (required)

**Requirements**:
- GLB file MUST be accessible via absolute HTTPS URL
- User interaction required to trigger redirect
- ARCore MUST be installed on device
- Google Play Services for AR required

**Example JavaScript**:
```javascript
function launchSceneViewer(glbPath, modelName) {
  // Convert relative to absolute URL
  const absoluteUrl = new URL(glbPath, window.location.href).href;

  const fileParam = encodeURIComponent(absoluteUrl);
  const titleParam = encodeURIComponent(modelName);
  const fallbackParam = encodeURIComponent(window.location.href);

  const intentUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${fileParam}&mode=ar_only&title=${titleParam}#Intent;scheme=https;package=com.google.android.googlequicksearchbox;action=android.intent.action.VIEW;S.browser_fallback_url=${fallbackParam};end;`;

  window.location.href = intentUrl;
}
```

**Success Criteria**:
- Scene Viewer launches in AR mode
- Model displays at correct scale (1 unit = 1 meter)
- Textures render correctly
- User can place model in physical space
- User can capture photos/videos in Scene Viewer

---

## 4. URL Routing Contract

**Pattern**: Directory-based clean URLs

### Landing Page
- **URL**: `/` or `/index.html`
- **Purpose**: Model gallery with links to individual AR pages
- **Response**: 200 OK, HTML page

### Model Pages
- **URL Pattern**: `/{model-id}/` or `/{model-id}/index.html`
- **Examples**:
  - `/fire/`
  - `/flood/`
  - `/quake/`
- **Purpose**: AR launcher page for specific model
- **Response**: 200 OK, HTML page with embedded device detection and AR launch logic

### Model Assets
- **USDZ**: `/models/{model-id}.usdz`
- **GLB**: `/models/{model-id}.glb`
- **Preview Images**: `/assets/images/{model-id}-preview.{ext}`

### Static Assets
- **CSS**: `/assets/css/styles.css`
- **JavaScript**: `/assets/js/{module-name}.js`

**404 Handling**:
- Invalid model IDs (e.g., `/invalid-model/`) SHOULD return 404
- Missing model files SHOULD return 404 with helpful error message

---

## 5. Performance Contracts

Based on constitution requirements (Principle II: Performance First).

### Page Load Performance
- **Initial HTML load**: <2 seconds on 4G connection
- **Time to Interactive**: <3 seconds
- **Total page weight** (HTML+CSS+JS): <100KB
- **Preview images**: <200KB each

### AR Model Launch Performance
- **Time to AR launch** (after page load): <3 seconds
- **Total time** (QR scan to AR display): <5 seconds (95th percentile)

### Asset Optimization
- **USDZ files**: <50MB (constitution requirement)
- **GLB files**: <20MB (constitution requirement)
- **Compression**: Use Draco compression for GLB files
- **Caching**: Long-term caching headers (31536000 seconds = 1 year)

---

## 6. Accessibility Contracts

Based on constitution Principle III (Progressive Enhancement).

### Minimum Requirements
- All model pages MUST have descriptive `<title>` and `<meta>` tags
- All images MUST have meaningful `alt` text
- All AR buttons MUST have accessible labels
- Fallback content MUST be readable without AR capability
- Keyboard navigation MUST work for all interactive elements
- Color contrast MUST meet WCAG AA standards

### Screen Reader Support
```html
<!-- Good example -->
<button aria-label="View Fire Disaster Scenario in Augmented Reality">
  View in AR
</button>

<img src="/assets/images/fire-preview.png"
     alt="3D model preview showing fire spread patterns and safety zones">
```

---

## 7. Testing Contracts

### Device Testing Requirements
- [ ] Test iOS Quick Look on physical iPhone (iOS 12+ minimum)
- [ ] Test Android Scene Viewer on physical ARCore device (Android 7.0+ minimum)
- [ ] Test fallback content on desktop browser (Chrome, Firefox, Safari)
- [ ] Test fallback content on older mobile devices (no AR support)

### Performance Testing
- [ ] Measure page load time on 4G connection (target <2s)
- [ ] Measure AR launch time (target <3s after page load)
- [ ] Verify model file sizes (<50MB USDZ, <20MB GLB)

### Accessibility Testing
- [ ] Run Lighthouse accessibility audit (target score >90)
- [ ] Test with screen reader (VoiceOver on iOS, TalkBack on Android)
- [ ] Test keyboard navigation

---

## Contract Validation Checklist

Before deployment to production:

### File Serving
- [ ] USDZ files served with correct MIME type (`model/vnd.usdz+zip`)
- [ ] GLB files served with correct MIME type (`model/gltf-binary`)
- [ ] All files served over HTTPS
- [ ] Cache headers configured (1 year)

### Platform Integration
- [ ] iOS Quick Look launches successfully on test device
- [ ] Android Scene Viewer launches successfully on test device
- [ ] Fallback content displays on non-AR devices

### Performance
- [ ] Page load <2s on 4G
- [ ] AR launch <3s after page load
- [ ] Total <5s from QR scan to AR display

### Accessibility
- [ ] All images have alt text
- [ ] All buttons have labels
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility verified

---

## Future Contract Extensions

Potential contracts for future features:

1. **Analytics API**: Track AR launch events
2. **CMS API**: Manage models dynamically
3. **User Preferences API**: Save/load user settings
4. **WebXR API**: Direct browser-based AR (when iOS supports it)

**Current Decision**: Keep it simple - no backend API for MVP

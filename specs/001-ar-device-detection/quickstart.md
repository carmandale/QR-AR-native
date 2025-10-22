# Quickstart: AR Device Detection and Model Serving

**Feature**: 001-ar-device-detection
**Last Updated**: 2025-10-19
**Estimated Setup Time**: 30 minutes

## Overview

This quickstart guide walks you through building and deploying the AR model serving web application from scratch. By the end, you'll have a working site that automatically detects iOS/Android devices and launches AR experiences with disaster scenario models.

---

## Prerequisites

### Required Tools
- **Web Browser**: Chrome, Firefox, or Safari for testing
- **Text Editor**: VS Code, Sublime, or any code editor
- **Model Conversion Tool** (one of):
  - Reality Converter (macOS, free) - Recommended
  - Blender (cross-platform, free)
  - Online converter: https://modelconverter.com

### Required Accounts
- **Cloudflare Pages** account (free): https://pages.cloudflare.com
  - Alternative: Netlify or Vercel account

### Testing Devices (Highly Recommended)
- **iOS device**: iPhone 7+ with iOS 12+ for Quick Look testing
- **Android device**: ARCore-compatible device with Android 7.0+

### Existing Assets
- ✅ `models/fire.usdz` (37MB) - already in repo
- ✅ `models/quake.usdz` (46MB) - already in repo
- ✅ `QR-codes/fire.png` - already in repo
- ✅ `QR-codes/flood.png` - already in repo
- ✅ `QR-codes/quake.png` - already in repo

### Assets to Create
- ⚠️ `models/fire.glb` - convert from fire.usdz
- ⚠️ `models/flood.usdz` - needs to be created/sourced
- ⚠️ `models/flood.glb` - needs to be created/sourced
- ⚠️ `models/quake.glb` - convert from quake.usdz

---

## Step 1: Create Project Structure (5 minutes)

Create the following directory structure in your repository root:

```bash
# Create directories
mkdir -p public/{fire,flood,quake,assets/{css,js,images}}
mkdir -p public/models

# Move existing models
cp models/fire.usdz public/models/
cp models/quake.usdz public/models/

# QR codes are for reference only (not served)
# Keep in /QR-codes/ directory
```

**Result**: You should have:
```
public/
├── fire/
├── flood/
├── quake/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── models/
    ├── fire.usdz (37MB - copied)
    └── quake.usdz (46MB - copied)
```

---

## Step 2: Convert Models to GLB Format (15 minutes)

### Option A: Using Reality Converter (macOS)

1. Download Reality Converter from Apple: https://developer.apple.com/augmented-reality/tools/
2. Open Reality Converter
3. Drag `fire.usdz` into the app
4. Click "Export" → Choose "GLTF Binary (.glb)"
5. Enable "Compress with Draco" option
6. Save as `fire.glb` to `public/models/`
7. Repeat for `quake.usdz`

**Target file sizes**:
- `fire.glb`: Aim for 10-15MB (down from 37MB USDZ)
- `quake.glb`: Aim for 15-20MB (down from 46MB USDZ)

### Option B: Using Online Converter

1. Visit https://modelconverter.com/convert.html
2. Upload `fire.usdz`
3. Select output format: GLB
4. Enable Draco compression if available
5. Download converted `fire.glb`
6. Save to `public/models/`
7. Repeat for `quake.usdz`

### Option C: Using Blender

```bash
# Install USD plugin for Blender
# Then in Blender:
# File → Import → Universal Scene Description (.usd, .usda, .usdc, .usdz)
# Select fire.usdz
# File → Export → glTF 2.0 (.glb)
# Enable "Draco mesh compression"
# Save as fire.glb
```

**Validation**: Check file sizes
```bash
ls -lh public/models/*.glb

# Expected:
# fire.glb: 10-15MB
# quake.glb: 15-20MB
```

---

## Step 3: Create Preview Images (10 minutes)

Generate fallback preview images for each model:

### Option A: Screenshot from AR Viewers

1. **iOS Quick Look**:
   - Transfer USDZ to iPhone via AirDrop
   - Open in Files app → tap USDZ → Quick Look opens
   - Take screenshot (Volume Up + Power button)
   - AirDrop screenshot back to Mac

2. **Save screenshots**:
   ```bash
   # Resize and optimize
   # Using ImageMagick (or any image editor):
   convert fire-screenshot.png -resize 1024x1024 -quality 85 public/assets/images/fire-preview.jpg

   # Or use online tools:
   # https://squoosh.app - Google's image optimizer
   ```

### Option B: Render from 3D Software

Use Blender, Cinema 4D, or similar to render static views of each model.

**Target specs**:
- Dimensions: 1024x1024px or 1920x1080px
- Format: JPEG (or WebP with JPEG fallback)
- File size: <200KB each
- Content: Clear view of the model showing key features

**Required images**:
- `public/assets/images/fire-preview.jpg`
- `public/assets/images/flood-preview.jpg` (after flood model is created)
- `public/assets/images/quake-preview.jpg`

---

## Step 4: Create HTML Pages (10 minutes)

### Create Landing Page

**File**: `public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="View disaster scenario 3D models in augmented reality">
  <title>AR Disaster Scenarios</title>
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
  <header>
    <h1>AR Disaster Scenarios</h1>
    <p>View 3D disaster models in augmented reality on your mobile device</p>
  </header>

  <main class="model-gallery">
    <div class="model-card">
      <img src="/assets/images/fire-preview.jpg" alt="Fire disaster scenario">
      <h2>Fire Disaster</h2>
      <p>3D model demonstrating fire hazard patterns and safety zones</p>
      <a href="/fire/" class="view-button">View in AR</a>
    </div>

    <div class="model-card">
      <img src="/assets/images/quake-preview.jpg" alt="Earthquake disaster scenario">
      <h2>Earthquake Disaster</h2>
      <p>3D model illustrating seismic damage patterns and emergency shelters</p>
      <a href="/quake/" class="view-button">View in AR</a>
    </div>

    <!-- Flood card commented out until model is ready -->
    <!--
    <div class="model-card">
      <img src="/assets/images/flood-preview.jpg" alt="Flood disaster scenario">
      <h2>Flood Disaster</h2>
      <p>3D model showing flood water levels and safe zones</p>
      <a href="/flood/" class="view-button">View in AR</a>
    </div>
    -->
  </main>

  <footer>
    <p>AR viewing requires iOS 12+ or ARCore-compatible Android device</p>
  </footer>
</body>
</html>
```

### Create Model AR Pages

**File**: `public/fire/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="View fire disaster scenario in augmented reality">
  <title>Fire Disaster Scenario - AR View</title>
  <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
  <main class="ar-page">
    <!-- Preview image (always visible) -->
    <img id="preview-image"
         src="/assets/images/fire-preview.jpg"
         alt="Fire disaster scenario 3D model">

    <h1>Fire Disaster Scenario</h1>
    <p class="description">
      This 3D model demonstrates fire hazard patterns, spread zones, and safety
      evacuation routes for emergency preparedness training.
    </p>

    <!-- iOS AR Button (hidden by default, shown by JS if supported) -->
    <a id="ios-ar-button"
       rel="ar"
       href="/models/fire.usdz"
       style="display: none;"
       class="ar-button">
      <img src="/assets/images/fire-preview.jpg" alt="Launch AR">
      View in AR (iOS)
    </a>

    <!-- Android AR Button (hidden by default, shown by JS if supported) -->
    <button id="android-ar-button"
            style="display: none;"
            class="ar-button">
      View in AR (Android)
    </button>

    <!-- Fallback message (shown if AR not supported) -->
    <div id="fallback-message" style="display: none;" class="fallback">
      <p><strong>AR viewing requires:</strong></p>
      <ul>
        <li>iPhone with iOS 12+ (Quick Look)</li>
        <li>Android 7.0+ with ARCore support</li>
      </ul>
      <p>You're viewing the preview image above.</p>
    </div>

    <p class="back-link"><a href="/">← Back to gallery</a></p>
  </main>

  <!-- Device detection and AR launcher -->
  <script src="/assets/js/ar-launcher.js"></script>
  <script>
    // Model data for this page
    const MODEL = {
      id: "fire",
      name: "Fire Disaster Scenario",
      usdzPath: "/models/fire.usdz",
      glbPath: "/models/fire.glb"
    };
  </script>
</body>
</html>
```

**Repeat for `public/quake/index.html`** (change MODEL data and paths)

---

## Step 5: Create JavaScript (15 minutes)

**File**: `public/assets/js/ar-launcher.js`

```javascript
// Device detection
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

  return {
    platform: iOS ? "ios" : (Android ? "android" : "desktop"),
    quickLookSupported,
    sceneViewerSupported,
    arCapable: quickLookSupported || sceneViewerSupported
  };
}

// Android Scene Viewer launcher
function launchSceneViewer(glbPath, modelName) {
  // Convert relative to absolute URL
  const absoluteUrl = new URL(glbPath, window.location.href).href;

  const fileParam = encodeURIComponent(absoluteUrl);
  const titleParam = encodeURIComponent(modelName);
  const fallbackParam = encodeURIComponent(window.location.href);

  const intentUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${fileParam}&mode=ar_only&title=${titleParam}#Intent;scheme=https;package=com.google.android.googlequicksearchbox;action=android.intent.action.VIEW;S.browser_fallback_url=${fallbackParam};end;`;

  window.location.href = intentUrl;
}

// Initialize page on load
window.addEventListener('DOMContentLoaded', () => {
  const device = detectDevice();

  const iosButton = document.getElementById('ios-ar-button');
  const androidButton = document.getElementById('android-ar-button');
  const fallbackMessage = document.getElementById('fallback-message');

  if (device.quickLookSupported && iosButton) {
    // Show iOS Quick Look button
    iosButton.style.display = 'block';
  } else if (device.sceneViewerSupported && androidButton) {
    // Show Android Scene Viewer button
    androidButton.style.display = 'block';

    // Attach click handler
    androidButton.addEventListener('click', () => {
      if (typeof MODEL !== 'undefined') {
        launchSceneViewer(MODEL.glbPath, MODEL.name);
      }
    });
  } else if (fallbackMessage) {
    // Show fallback message for non-AR devices
    fallbackMessage.style.display = 'block';
  }

  // Log device info for debugging
  console.log('Device detection:', device);
});
```

---

## Step 6: Create CSS (5 minutes)

**File**: `public/assets/css/styles.css`

```css
/* Reset and base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Landing page gallery */
.model-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin: 40px 0;
}

.model-card {
  background: #f8f8f8;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.model-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 15px;
}

.view-button {
  display: inline-block;
  background: #007aff;
  color: white;
  padding: 12px 30px;
  border-radius: 8px;
  text-decoration: none;
  margin-top: 15px;
  transition: background 0.2s;
}

.view-button:hover {
  background: #0051d5;
}

/* AR page */
.ar-page {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.ar-page img {
  width: 100%;
  max-width: 500px;
  height: auto;
  border-radius: 12px;
  margin: 20px 0;
}

.ar-button {
  display: block;
  width: 100%;
  max-width: 300px;
  margin: 30px auto;
  padding: 16px 40px;
  font-size: 18px;
  font-weight: 600;
  background: #34c759;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.ar-button:hover {
  background: #2da84c;
  transform: scale(1.05);
}

.fallback {
  background: #fff3cd;
  padding: 20px;
  border-radius: 8px;
  margin: 30px 0;
  text-align: left;
}

.back-link {
  margin-top: 40px;
}

.back-link a {
  color: #007aff;
  text-decoration: none;
}

footer {
  text-align: center;
  margin-top: 60px;
  padding-top: 20px;
  border-top: 1px solid #ddd;
  color: #666;
  font-size: 14px;
}
```

---

## Step 7: Configure MIME Types (2 minutes)

**File**: `public/_headers`

```
/*.usdz
  Content-Type: model/vnd.usdz+zip
  Cache-Control: public, max-age=31536000, immutable

/*.glb
  Content-Type: model/gltf-binary
  Cache-Control: public, max-age=31536000, immutable

/*.jpg
  Cache-Control: public, max-age=31536000, immutable

/*.png
  Cache-Control: public, max-age=31536000, immutable
```

---

## Step 8: Deploy to Cloudflare Pages (10 minutes)

### Option A: GitHub Integration (Recommended)

1. **Push code to GitHub**:
   ```bash
   git add public/
   git commit -m "Add AR model serving web app"
   git push origin 001-ar-device-detection
   ```

2. **Connect to Cloudflare Pages**:
   - Go to https://dash.cloudflare.com
   - Click "Pages" → "Create a project"
   - Connect your GitHub account
   - Select your repository
   - Configure build:
     - Build command: (leave empty)
     - Build output directory: `public`
   - Click "Save and Deploy"

3. **Wait for deployment** (1-2 minutes)

4. **Get your URL**: `https://qr-ar-native.pages.dev` (or custom domain)

### Option B: Direct Upload

1. **Install Wrangler** (Cloudflare CLI):
   ```bash
   npm install -g wrangler
   ```

2. **Login**:
   ```bash
   wrangler login
   ```

3. **Deploy**:
   ```bash
   wrangler pages deploy public --project-name=qr-ar-native
   ```

4. **Get your URL** from output

---

## Step 9: Test on Devices (15 minutes)

### Test iOS Quick Look

1. **Generate QR code** for your deployed fire page:
   - URL: `https://your-site.pages.dev/fire/`
   - Use QR code generator: https://qr-code-generator.com

2. **Scan with iPhone**:
   - Open Camera app
   - Point at QR code
   - Tap notification to open link
   - Verify "View in AR (iOS)" button appears
   - Tap button → Quick Look should launch with fire model

3. **Validate**:
   - Model displays at correct scale
   - Textures render correctly
   - Can place in AR space
   - Screenshots work

### Test Android Scene Viewer

1. **Scan QR code with Android device**
   - URL: `https://your-site.pages.dev/fire/`

2. **Tap "View in AR (Android)" button**
   - Scene Viewer should launch
   - Model should load from GLB file

3. **Validate**:
   - Model displays at correct scale
   - Textures render correctly
   - Can place in AR space
   - Photos work

### Test Fallback (Desktop)

1. **Visit page on desktop browser**:
   - URL: `https://your-site.pages.dev/fire/`

2. **Verify**:
   - Preview image displays
   - Fallback message shows
   - No AR buttons visible

---

## Step 10: Update QR Codes (Optional)

If you want to update the existing QR code images to point to your deployed site:

1. **Generate new QR codes**:
   - Fire: `https://your-site.pages.dev/fire/`
   - Quake: `https://your-site.pages.dev/quake/`

2. **Replace images**:
   ```bash
   # Save new QR codes as:
   # QR-codes/fire.png (updated)
   # QR-codes/quake.png (updated)
   ```

3. **Print new QR codes** for physical locations

---

## Verification Checklist

Before considering the feature complete:

### Files Created
- [ ] `public/index.html` - Landing page
- [ ] `public/fire/index.html` - Fire AR page
- [ ] `public/quake/index.html` - Quake AR page
- [ ] `public/assets/js/ar-launcher.js` - Device detection
- [ ] `public/assets/css/styles.css` - Styling
- [ ] `public/_headers` - MIME type configuration

### Models Prepared
- [ ] `public/models/fire.usdz` (37MB - existing)
- [ ] `public/models/fire.glb` (10-15MB target)
- [ ] `public/models/quake.usdz` (46MB - existing)
- [ ] `public/models/quake.glb` (15-20MB target)

### Preview Images
- [ ] `public/assets/images/fire-preview.jpg` (<200KB)
- [ ] `public/assets/images/quake-preview.jpg` (<200KB)

### Deployment
- [ ] Site deployed to Cloudflare Pages (or alternative)
- [ ] HTTPS working
- [ ] MIME types configured correctly

### Device Testing
- [ ] iOS Quick Look tested on physical iPhone
- [ ] Android Scene Viewer tested on physical Android device
- [ ] Desktop fallback tested in browser

### Performance
- [ ] Page load <2s on 4G
- [ ] Total size <100KB (HTML+CSS+JS)
- [ ] AR models under size limits

---

## Next Steps

### Phase 1 Complete: Fire and Quake Models ✅

You now have a working AR web app with two disaster models!

### Phase 2: Add Flood Model

1. Create or source flood.usdz model
2. Convert to flood.glb
3. Create flood-preview.jpg
4. Create `public/flood/index.html`
5. Uncomment flood card in `public/index.html`
6. Test on both platforms

### Phase 3: Enhancements (Optional)

- Add analytics to track AR launches
- Create custom 404 page
- Add meta tags for social sharing
- Optimize images with WebP format
- Add PWA features (offline support)
- Custom domain setup

---

## Troubleshooting

### iOS Quick Look Not Launching

**Problem**: Button appears but Quick Look doesn't launch

**Solutions**:
1. Check MIME type: `curl -I https://your-site.pages.dev/models/fire.usdz`
   - Must return `content-type: model/vnd.usdz+zip`
2. Verify HTTPS (required for AR)
3. Check iOS version (iOS 12+ required)
4. Try on different iPhone model

### Android Scene Viewer Not Launching

**Problem**: Button appears but Scene Viewer doesn't launch

**Solutions**:
1. Check ARCore installation: Google Play Store → "Google Play Services for AR"
2. Verify Android version (7.0+ required)
3. Check GLB file is accessible: Visit URL directly in browser
4. Check browser console for errors

### Models Too Large

**Problem**: Models exceed file size limits

**Solutions**:
1. Apply Draco compression during GLB export
2. Reduce texture resolution (1024x1024 max)
3. Simplify geometry (reduce polygon count)
4. Use Reality Converter optimization settings

### MIME Type Not Working

**Problem**: `_headers` file not being respected

**Solutions**:
1. Cloudflare Pages: File must be in build output directory (`public/_headers`)
2. Netlify: Use `netlify.toml` instead of `_headers`
3. Verify file is being deployed: Check build logs

---

## Support

**Documentation**: See `/specs/001-ar-device-detection/` for detailed specs

**Constitution**: See `.specify/memory/constitution.md` for project principles

**Testing**: See `contracts/README.md` for validation requirements

**Questions**: Open an issue in the repository

---

**Estimated Total Time**: 2-3 hours (including model conversion and testing)

**Status**: ✅ Ready to build! Follow steps 1-10 above.
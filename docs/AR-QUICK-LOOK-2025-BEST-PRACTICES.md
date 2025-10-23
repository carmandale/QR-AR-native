# AR Quick Look & Spatial Web - 2025 Best Practices

**Last Updated**: October 2025
**Apple Documentation References**: WWDC23, WWDC25, Safari 17+/visionOS

---

## 🚨 What Changed from Old Implementation

### ❌ Old Pattern (2018-2019)
```html
<!-- WRONG: Hidden image, text inside anchor -->
<a rel="ar" href="model.usdz" class="btn">
    <img src="preview.png" style="display:none;">
    📱 View in AR
</a>
```

**Problems**:
- Hidden `<img>` breaks AR Quick Look
- Text/emoji inside anchor violates Apple requirements
- No support for spatial web (visionOS)
- No inline 3D preview capability

---

## ✅ 2025 Best Practices Implementation

### 1. Modern HTML `<model>` Element (Safari 17+/visionOS)

```html
<!-- BEST: Modern spatial web with inline 3D preview -->
<model stagemode="orbit" style="width: 100%; height: 400px;">
    <source src="model.usdz" type="model/vnd.usdz+zip">
    <img src="preview.png" alt="Model preview">
</model>
```

**Benefits**:
- **Inline 3D preview** - Users can rotate/inspect before AR launch
- **Spatial computing** - Stereoscopic rendering on Vision Pro
- **Progressive enhancement** - Fallback image for older browsers
- **Standard HTML** - Works like `<video>` or `<audio>` elements
- **Interactive controls** - Orbit, scale, rotation via JavaScript API

**Browser Support**:
- Safari 17+ (iOS 17+, macOS Sonoma+)
- visionOS (all versions)

---

### 2. Legacy AR Quick Look Pattern (iOS 12-16)

```html
<!-- GOOD: Legacy pattern for older iOS devices -->
<a rel="ar" href="model.usdz#allowsContentScaling=0">
    <img
        src="preview.png"
        alt="View in AR"
        style="width: 100%; max-width: 400px; border-radius: 8px; cursor: pointer;"
    >
</a>
```

**Critical Requirements** (per Apple docs):
1. ✅ `rel="ar"` attribute on `<a>` tag
2. ✅ **Visible** `<img>` as **first child** (no `display:none`)
3. ✅ **No text/emojis** inside anchor tag
4. ✅ MIME type: `model/vnd.usdz+zip` (set in server headers)

**URL Fragment Customization**:
- `#allowsContentScaling=0` - Disable pinch-to-zoom (shows actual scale)
- `#canonicalWebPageURL=https://...` - For sharing
- `#checkoutTitle=Product%20Name` - For Apple Pay integration
- `#checkoutSubtitle=Price` - For Apple Pay

---

### 3. Progressive Enhancement Strategy

```javascript
// Detect modern browser support
const supportsModelElement = typeof HTMLModelElement !== 'undefined';

if (supportsModelElement) {
    // Show <model> element for inline 3D preview
    modelElement.style.display = 'block';

    // Handle model loading
    modelElement.ready.then(() => {
        console.log('3D model loaded');
    }).catch(() => {
        // Fallback to legacy AR link
        modelElement.style.display = 'none';
    });
}

// Legacy <a rel="ar"> is always visible as fallback
```

**Why Both Patterns?**
- Modern browsers get rich 3D preview + AR launch
- Older iOS devices (12-16) still get AR Quick Look
- Graceful degradation for all Safari versions

---

## 📋 USDZ File Optimization (2025 Guidelines)

### File Size Limits
- **Maximum polygons**: 100,000 triangles
- **Texture resolution**: 2048×2048 PBR textures (single set)
- **Animation length**: ≤10 seconds
- **Recommended detail levels**: "Reduced" or "Medium" (in Reality Converter)

### Quality Best Practices
1. **Avoid high-frequency normal maps** - Causes aliasing artifacts
2. **Test in motion** - View model while moving to check quality
3. **Balance visual fidelity vs file size**
4. **Use Draco compression** for GLB files (Android)

### Conversion Tools
- **Reality Converter** (macOS) - Official Apple tool
- **Reality Composer Pro** (Xcode) - For visionOS apps
- **Blender with USD export** - Cross-platform
- **Command line**: `xcrun usdz_converter input.obj output.usdz`

---

## 🌐 Server Configuration (Critical)

### MIME Types (in `_headers` file for Cloudflare Pages)

```
/*.usdz
  Content-Type: model/vnd.usdz+zip

/*.reality
  Content-Type: model/vnd.reality

/*.glb
  Content-Type: model/gltf-binary
```

**Without correct MIME types, AR Quick Look will silently fail!**

### Cache Headers (Performance)

```
/models/*
  Cache-Control: public, max-age=31536000, immutable
```

---

## 📱 Platform Support Matrix

| Feature | iOS 12-16 | iOS 17+ | visionOS | Android |
|---------|-----------|---------|----------|---------|
| `<a rel="ar">` | ✅ | ✅ | ✅ | ❌ |
| `<model>` element | ❌ | ✅ | ✅ | ❌ |
| Inline 3D preview | ❌ | ✅ | ✅ | ❌ |
| Stereoscopic view | ❌ | ❌ | ✅ | ❌ |
| Scene Viewer (GLB) | ❌ | ❌ | ❌ | ✅ |

---

## 🎯 Implementation Checklist

### HTML Structure
- [ ] Add `<model>` element with `stagemode="orbit"`
- [ ] Include fallback `<img>` inside `<model>`
- [ ] Add legacy `<a rel="ar">` with **visible** `<img>` (first child)
- [ ] No text/emojis inside `<a>` tag
- [ ] Proper `type="model/vnd.usdz+zip"` on `<source>`

### JavaScript
- [ ] Feature detection: `typeof HTMLModelElement !== 'undefined'`
- [ ] Handle `modelElement.ready` Promise
- [ ] Fallback to legacy link on error
- [ ] Show appropriate UI based on device capabilities

### Server Config
- [ ] MIME type: `model/vnd.usdz+zip` for `.usdz`
- [ ] MIME type: `model/gltf-binary` for `.glb`
- [ ] Cache headers for model files
- [ ] HTTPS required (AR won't work over HTTP)

### USDZ Files
- [ ] ≤100k polygons
- [ ] 2048×2048 textures max
- [ ] Test on iPhone (iOS 12+)
- [ ] Test on Vision Pro (visionOS)
- [ ] Verify scale (1 unit = 1 meter)

### Testing
- [ ] Safari iOS 12-16 (legacy pattern)
- [ ] Safari iOS 17+ (modern `<model>` element)
- [ ] visionOS Simulator (spatial computing)
- [ ] Android Chrome (Scene Viewer with GLB)
- [ ] Desktop Safari (fallback content)

---

## 📚 Additional Resources

### Official Apple Documentation
- [AR Quick Look Gallery](https://developer.apple.com/augmented-reality/quick-look/)
- [WWDC23: Discover Quick Look for spatial computing](https://developer.apple.com/videos/play/wwdc2023/10085/)
- [WWDC23: Create 3D models for Quick Look](https://developer.apple.com/videos/play/wwdc2023/10274/)
- [WWDC25: What's new for the spatial web](https://developer.apple.com/videos/play/wwdc2025/237/)
- [WebKit Blog: HTML model element](https://webkit.org/blog/17118/)

### Tools
- [Reality Converter](https://developer.apple.com/augmented-reality/tools/) (macOS)
- [Reality Composer Pro](https://developer.apple.com/augmented-reality/tools/) (Xcode)
- [Blender USD Export](https://www.blender.org/) (Cross-platform)

---

## 🔍 Common Issues & Solutions

### Issue: AR doesn't launch on iOS
**Solutions**:
1. Check MIME type is `model/vnd.usdz+zip`
2. Ensure `<img>` is **visible** (no `display:none`)
3. Verify HTTPS (AR won't work over HTTP)
4. Confirm `rel="ar"` is on `<a>` tag
5. Test USDZ file in Reality Converter

### Issue: Model doesn't load in `<model>` element
**Solutions**:
1. Check browser is Safari 17+ or visionOS
2. Verify `type="model/vnd.usdz+zip"` on `<source>`
3. Listen for `modelElement.ready` Promise rejection
4. Fallback to legacy `<a rel="ar">` pattern

### Issue: Model appears too large/small in AR
**Solutions**:
1. Verify scale in USDZ (1 unit = 1 meter)
2. Use `#allowsContentScaling=0` to disable pinch zoom
3. Test with physical object for scale reference
4. Check model units in 3D software before export

---

**Implementation Status**: ✅ Updated fire/index.html with 2025 best practices
**Next Steps**: Update flood/index.html and quake/index.html with same pattern

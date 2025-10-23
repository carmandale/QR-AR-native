# AR Preview Image Specifications

**Last Updated**: October 2025
**Purpose**: Fallback images for devices without `<model>` element support (iOS 12-16, desktop browsers)

---

## 📋 Quick Reference

| Property | Specification |
|----------|--------------|
| **Format** | PNG (preferred) or JPEG |
| **Dimensions** | 1200×900 pixels (4:3 aspect ratio) |
| **File Size** | <200KB each (optimize heavily) |
| **Minimum Resolution** | 800×600 pixels |
| **Color Depth** | 8-bit (24-bit RGB + alpha) |
| **Compression** | PNG with moderate compression |

---

## 📂 File Locations

```
public/assets/images/
├── fire-preview.png      (1200×900, ~26KB, orange background)
├── flood-preview.png     (1200×900, ~35KB, blue background)
└── quake-preview.png     (1200×900, ~36KB, brown background)
```

---

## 🎨 Current Implementation

### HTML Usage Pattern
```html
<!-- Legacy AR Quick Look (iOS 12-16) -->
<a rel="ar" href="/models/fire.usdz#allowsContentScaling=0">
    <img
        src="/assets/images/fire-preview.png"
        alt="View fire disaster scenario in AR"
        style="width: 100%; max-width: 400px; border-radius: 8px;"
    >
</a>
```

### Apple Requirements
1. ✅ Image must be **visible** (no `display:none`)
2. ✅ Image must be **first child** of `<a rel="ar">` tag
3. ✅ No text/emojis inside anchor with image
4. ✅ Proper `alt` text for accessibility

---

## 🔨 How to Create Better Preview Images

### Method 1: Extract from USDZ (Mac Only)

**Using Reality Converter:**
```bash
1. Open fire.usdz in Reality Converter
2. Rotate model to best viewing angle
3. Take screenshot: Cmd+Shift+4
4. Crop to 1200×900 in Preview
5. Export as PNG
6. Optimize: ImageOptim or TinyPNG
```

**Using Quick Look:**
```bash
1. Select fire.usdz in Finder
2. Press Space (Quick Look preview)
3. Rotate to best angle
4. Screenshot (Cmd+Shift+4) and crop
5. Optimize file size
```

### Method 2: Blender (Cross-Platform)

```bash
# Install USDZ addon
1. Edit → Preferences → Add-ons
2. Search "USDZ" and enable

# Import and render
1. File → Import → USDZ
2. Select fire.usdz
3. Set camera angle (Numpad 0)
4. Render → Render Image (F12)
5. Image → Save As → PNG (1200×900)
```

### Method 3: Online Conversion

**3D Model Viewers:**
- https://3dviewer.net/
- https://threejs.org/editor/
- Upload USDZ → Screenshot → Crop

### Method 4: Manual Screenshots from AR

**On iPhone/iPad:**
```bash
1. Open fire.usdz in Files app
2. Tap to launch AR Quick Look
3. Position model in AR
4. Take screenshot (Volume Up + Power)
5. AirDrop to Mac
6. Crop to 1200×900
7. Optimize file size
```

---

## 🖼️ Image Optimization

### Using ImageMagick
```bash
# Resize to exact dimensions
magick input.png -resize 1200x900! -quality 85 output.png

# Reduce file size (lossy)
magick input.png -strip -resize 1200x900 -quality 85 output.png

# Create thumbnail (400×300 for faster loading)
magick input.png -resize 400x300! -quality 85 thumb.png
```

### Using Web Tools
- **TinyPNG**: https://tinypng.com/ (smart compression)
- **Squoosh**: https://squoosh.app/ (browser-based)
- **ImageOptim** (Mac): https://imageoptim.com/

---

## 🎯 Best Practices

### Composition
- **Show the whole model** from a recognizable angle
- **Use neutral background** (white or light gray)
- **Center the model** in frame
- **Avoid clipping** edges

### Lighting
- **Even lighting** - no harsh shadows
- **Proper exposure** - not too dark or bright
- **Match AR appearance** - similar to what users see in AR

### Branding (Optional)
- Small logo in corner (max 10% of image)
- Watermark if needed (subtle, bottom right)
- Keep text minimal

---

## 📱 Responsive Sizing

### CSS Implementation
```css
.ar-preview {
    width: 100%;
    max-width: 400px;
    height: auto;
    border-radius: 8px;
    display: block;
    margin: 0 auto;
}

/* Retina displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .ar-preview {
        /* 1200×900 PNG handles retina well */
    }
}
```

---

## 🚀 Advanced: Multiple Formats

### Progressive Enhancement
```html
<picture>
    <!-- Modern: WebP (best compression) -->
    <source srcset="/assets/images/fire-preview.webp" type="image/webp">

    <!-- Fallback: PNG (wider compatibility) -->
    <img src="/assets/images/fire-preview.png"
         alt="Fire disaster scenario">
</picture>
```

### Generate WebP Versions
```bash
# Using ImageMagick
magick fire-preview.png -quality 80 fire-preview.webp

# Or cwebp (better for WebP)
cwebp -q 80 fire-preview.png -o fire-preview.webp
```

---

## ✅ Quality Checklist

Before deploying preview images:

- [ ] Dimensions are 1200×900 (4:3 ratio)
- [ ] File size <200KB each
- [ ] Model is centered and fully visible
- [ ] Background is clean (no distractions)
- [ ] Image is sharp (not blurry)
- [ ] Colors match model appearance
- [ ] PNG transparency (if needed) works
- [ ] Tested on retina displays
- [ ] Tested on mobile devices
- [ ] Alt text is descriptive

---

## 🐛 Troubleshooting

### Image not showing
- **Check path**: `/assets/images/fire-preview.png` (case-sensitive)
- **Check MIME type**: Server should send `image/png`
- **Check permissions**: File readable by web server
- **Network tab**: Verify 200 OK response

### AR Quick Look not launching
- **Image visible**: Remove `display:none` or `visibility:hidden`
- **rel="ar"**: Must be on `<a>` tag
- **No text**: Remove text/emojis from anchor
- **HTTPS**: AR Quick Look requires HTTPS

### Large file sizes
- **Use PNG-8**: For images with limited colors
- **Optimize**: Use TinyPNG or ImageOptim
- **Reduce dimensions**: 800×600 is minimum
- **Consider WebP**: Better compression ratio

---

**Status**: ✅ Placeholder images generated (26-36KB each)
**Next Step**: Replace with actual USDZ screenshots for better quality

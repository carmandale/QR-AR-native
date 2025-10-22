<!--
Sync Impact Report:
Version: 0.0.0 → 1.0.0
- Initial constitution creation (MAJOR version for first ratification)
- New principles: 5 core principles established
- Added sections: Technical Standards, Development Workflow
- Templates requiring updates:
  ✅ spec-template.md - aligned with user story priorities and device detection requirements
  ✅ plan-template.md - Constitution Check section references this file
  ✅ tasks-template.md - task organization matches web app structure
  ⚠ No agent-specific references found - templates use generic guidance
- Follow-up: Monitor Quick Look and Scene Viewer API changes
-->

# QR-AR-Native Constitution

## Core Principles

### I. Device-Aware Serving

The system MUST detect device platform and serve appropriate AR formats automatically.

**Rules**:
- iOS devices receive USDZ files and launch Quick Look
- Android devices receive GLB files and launch Scene Viewer
- Detection happens server-side OR client-side (user agent parsing)
- Fallback to static preview for unsupported devices
- No manual format selection by users

**Rationale**: Users scan QR codes expecting instant AR - they should never need to choose formats or understand technical differences between platforms. The system abstracts platform complexity.

### II. Performance First

Page load and AR launch MUST be fast - users won't wait.

**Rules**:
- Initial page load: <2 seconds on 4G
- AR model launch: <3 seconds after page load
- Model file sizes: USDZ <50MB, GLB <20MB (compressed)
- Progressive loading: Show preview while model loads
- No unnecessary dependencies or frameworks

**Rationale**: QR codes are scanned in physical spaces (museums, events, classrooms). Slow loading breaks the experience and users abandon. Optimized assets and minimal code are non-negotiable.

### III. Progressive Enhancement

The system MUST work for all visitors, with enhanced AR for supported devices.

**Rules**:
- Base experience: Static image/video preview (works everywhere)
- Enhanced experience: AR model viewer (iOS/Android with AR support)
- Feature detection: Check for AR capability before offering AR launch
- Graceful degradation: Never show broken AR buttons on unsupported devices
- Accessible fallback: Screen reader descriptions for all models

**Rationale**: Not all devices support AR (desktop browsers, older phones). The site must provide value to everyone while delivering premium AR experiences where possible.

### IV. Simplicity Over Cleverness

Keep the codebase minimal, readable, and maintainable.

**Rules**:
- Single-purpose pages: One model per URL (e.g., `/fire`, `/flood`, `/quake`)
- Straightforward detection: Use proven user agent libraries, no custom regex
- Minimal dependencies: Avoid frameworks unless they solve real problems
- Clear file structure: `/models/[name].usdz` and `/models/[name].glb` convention
- No premature optimization: Start simple, measure, then optimize if needed

**Rationale**: This is a gateway application, not a complex platform. Overengineering (custom detection, unnecessary abstractions, framework bloat) makes maintenance harder without improving user experience.

### V. Asset Quality and Management

AR models MUST be optimized, tested, and version-controlled.

**Rules**:
- Source formats preserved: Keep original high-quality models
- Optimized exports: Compressed, textured, tested before deployment
- Validation required: Test both USDZ (iOS) and GLB (Android) before release
- Model metadata: Include descriptions, attribution, disaster type tags
- Version tracking: Model files in git or asset CDN with versioning

**Rationale**: Poor quality models (broken textures, incorrect scale, performance issues) destroy trust. Models are the core value - they must work perfectly on both platforms.

## Technical Standards

**Frontend Stack**:
- HTML/CSS/JavaScript (vanilla or minimal framework)
- Device detection library (e.g., UAParser.js or server-side headers)
- Responsive design (mobile-first)

**Backend Stack**:
- Static hosting (Netlify, Vercel) OR lightweight server (Node.js, Python)
- Model serving: Direct file serving or CDN
- URL routing: Clean paths (`/fire` not `/index.html?model=fire`)

**AR Model Requirements**:
- iOS: USDZ format, Quick Look compatible, tested on iPhone
- Android: GLB format, Scene Viewer compatible, tested on ARCore device
- Scale: Consistent across models (1 unit = 1 meter recommended)
- Textures: Embedded or properly referenced, optimized for mobile

**Testing Requirements**:
- Manual testing on physical iOS device (iPhone with AR support)
- Manual testing on physical Android device (ARCore compatible)
- Automated checks: File size validation, format validation
- User acceptance: QR code scan → AR launch in <5 seconds total

## Development Workflow

**Feature Development**:
1. Specify requirements (user story, device support, performance targets)
2. Design approach (detection method, file structure, routing)
3. Implement incrementally (one model/page at a time)
4. Test on real devices (both iOS and Android)
5. Deploy and validate with QR codes

**Model Pipeline**:
1. Receive or create source model (3D file)
2. Export optimized USDZ for iOS
3. Export optimized GLB for Android
4. Test both files in native AR viewers
5. Add to `/models/` directory with consistent naming
6. Update routing/pages to serve new model
7. Generate/update QR code

**Quality Gates**:
- All new models tested on physical devices before merge
- Performance regression checks (page load, file size)
- Accessibility review (alt text, fallback content)
- QR code validation (scan → AR launch works)

## Governance

**Constitution Authority**: This constitution defines non-negotiable practices for QR-AR-Native. All code reviews, feature specifications, and implementation plans MUST comply with these principles.

**Amendment Process**:
1. Propose change with rationale and impact analysis
2. Review against existing principles (is this truly necessary?)
3. Update constitution version (semantic versioning)
4. Update dependent templates and documentation
5. Communicate changes to all contributors

**Versioning Policy**:
- MAJOR: Remove/redefine core principles (breaks governance contract)
- MINOR: Add new principle or expand existing guidance significantly
- PATCH: Clarify wording, fix typos, refine without changing meaning

**Compliance Review**:
- Every PR MUST pass Constitution Check in implementation plan
- Violations require documented justification (added to plan.md Complexity Tracking)
- Recurring violations trigger constitution review (is principle too strict?)

**Version**: 1.0.0 | **Ratified**: 2025-10-19 | **Last Amended**: 2025-10-19

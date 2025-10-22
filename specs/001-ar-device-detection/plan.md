# Implementation Plan: AR Device Detection and Model Serving

**Branch**: `001-ar-device-detection` | **Date**: 2025-10-19 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-ar-device-detection/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a web application that automatically detects mobile device platform (iOS/Android) and serves appropriate AR model formats (USDZ for iOS Quick Look, GLB for Android Scene Viewer) for three disaster scenario models (fire, flood, quake). System must provide graceful fallback for non-AR devices, load pages in <2s, and launch AR in <3s after page load.

## Technical Context

**Language/Version**: NEEDS CLARIFICATION - HTML/CSS/JavaScript (vanilla) OR minimal framework (React, Vue, etc.) for frontend; Node.js, Python, or static site generator for backend/routing
**Primary Dependencies**: NEEDS CLARIFICATION - Device detection library (UAParser.js, Bowser, or similar); optional 3D fallback viewer (model-viewer, three.js)
**Storage**: Static file serving - AR models stored in `/models/` directory (USDZ and GLB files); no database required
**Testing**: Manual device testing on physical iOS and Android devices (required by constitution); automated file validation (size, format); optional: Playwright/Selenium for web flow testing
**Target Platform**: Web browsers on mobile devices (iOS 12+, ARCore-compatible Android) and desktop browsers (fallback experience)
**Project Type**: Web application (static frontend preferred for simplicity, optional lightweight backend for routing)
**Performance Goals**: <2s page load on 4G, <3s AR model launch after page load, <5s total time from QR scan to AR display (95th percentile)
**Constraints**: Model file sizes (USDZ <50MB, GLB <20MB), minimal dependencies (constitution principle IV), clean URL routing (`/fire`, `/flood`, `/quake`)
**Scale/Scope**: 3 disaster models (fire, flood, quake), 3 user stories (iOS, Android, fallback), moderate traffic (educational/event usage)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Device-Aware Serving ✅

**Compliance**: PASS

- ✅ Spec requires automatic iOS/Android detection (FR-001)
- ✅ USDZ for iOS, GLB for Android (FR-002, FR-003)
- ✅ No manual format selection (FR-005, SC-007)
- ✅ Fallback for unsupported devices (FR-006, User Story 3)

### Principle II: Performance First ✅

**Compliance**: PASS

- ✅ Page load <2s on 4G (FR-010, SC-006)
- ✅ AR launch <3s after page load (FR-011)
- ✅ Total time <5s QR to AR (SC-001)
- ✅ Model file size limits specified (Assumptions: USDZ <50MB, GLB <20MB)
- ✅ Minimal dependencies required (Technical Context: vanilla or minimal framework)

### Principle III: Progressive Enhancement ✅

**Compliance**: PASS

- ✅ Base experience: fallback content for all devices (FR-006, User Story 3)
- ✅ Enhanced experience: AR for iOS/Android (User Story 1, 2)
- ✅ Feature detection implied in device detection (FR-001)
- ✅ Graceful degradation: desktop/older devices get preview (User Story 3, SC-004)
- ✅ Accessibility: descriptive text for models (FR-012)

### Principle IV: Simplicity Over Cleverness ✅

**Compliance**: PASS

- ✅ Single-purpose pages: one model per URL (FR-004, Constraints: `/fire`, `/flood`, `/quake`)
- ✅ Straightforward detection: proven user agent libraries (Technical Context: NEEDS CLARIFICATION for specific library)
- ✅ Minimal dependencies: vanilla or minimal framework (Technical Context, constitution requirement)
- ✅ Clear file structure: `/models/[name].usdz` and `/models/[name].glb` (Project Structure TBD in Phase 0)
- ✅ No premature optimization: start simple (constitution principle)

### Principle V: Asset Quality and Management ✅

**Compliance**: PASS

- ✅ Source formats preserved: existing .usdz and .glb files in repo (Assumptions)
- ✅ Optimized exports: file size limits enforced (Assumptions, Performance Goals)
- ✅ Validation required: test both platforms before release (Testing: manual device testing)
- ✅ Model metadata: descriptive text for each model (FR-012)
- ✅ Version tracking: models in git (Assumptions, existing files in repo)

### Technical Standards Compliance ✅

**Frontend Stack**: PASS (HTML/CSS/JavaScript, device detection library, mobile-first design)
**Backend Stack**: PASS (static hosting or lightweight server, clean URL routing)
**AR Model Requirements**: PASS (USDZ/GLB formats, scale consistency, texture preservation)
**Testing Requirements**: PASS (manual physical device testing, automated file validation, QR code validation)

### Development Workflow Compliance ✅

**Feature Development**: PASS (spec → design → implement → test → deploy)
**Model Pipeline**: PASS (models already exist, routing to be implemented)
**Quality Gates**: PASS (device testing, performance checks, accessibility review, QR validation)

### Gates Summary

**Pre-Phase 0**: ✅ PASS - All constitution principles satisfied, proceed to research phase
**Identified Clarifications Needed**:
1. Frontend approach: vanilla JS vs minimal framework
2. Device detection library: UAParser.js, Bowser, or alternatives
3. Fallback viewer: static images vs interactive 3D viewer (model-viewer, three.js)
4. Backend: static site generator vs lightweight server vs pure static hosting

**No Violations** - All requirements align with constitution

---

### Post-Phase 1 Re-Evaluation ✅

**All clarifications resolved in research.md. Final constitution check:**

**Technical Decisions Made**:
1. ✅ Frontend: Vanilla HTML/CSS/JavaScript (zero frameworks) - COMPLIANT with Principle IV
2. ✅ Device Detection: No library, feature detection + basic UA parsing - COMPLIANT with Principle IV
3. ✅ Fallback: Static preview images - COMPLIANT with Principles III & IV
4. ✅ Hosting: Cloudflare Pages (unlimited bandwidth) - COMPLIANT with Principle II

**Updated Technical Context** (all NEEDS CLARIFICATION items resolved):
- Language/Version: HTML5, CSS3, JavaScript ES6+ (vanilla, no framework)
- Primary Dependencies: Zero external dependencies
- Storage: Static file serving (no database)
- Testing: Manual device testing + automated file validation
- Project Type: Static web application
- Performance: <100KB HTML+CSS+JS, <5s QR to AR (constitution compliant)

**Final Verdict**: ✅ **APPROVED** - All constitution principles satisfied with completed design

## Project Structure

### Documentation (this feature)

```
specs/001-ar-device-detection/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── checklists/
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

**Selected Structure**: Static web application (Option 2 simplified)

```
# Root-level static site structure
public/ or dist/          # Built output (if using build step)
├── index.html            # Landing page with model gallery
├── fire/
│   └── index.html        # Fire model AR launcher page
├── flood/
│   └── index.html        # Flood model AR launcher page
├── quake/
│   └── index.html        # Quake model AR launcher page
├── models/               # AR model files
│   ├── fire.usdz         # Existing iOS model
│   ├── fire.glb          # Android model (to be created/converted)
│   ├── flood.usdz        # Existing iOS model
│   ├── flood.glb         # Android model (to be created/converted)
│   ├── quake.usdz        # Existing iOS model
│   └── quake.glb         # Android model (to be created/converted)
├── assets/               # Images, CSS, JS
│   ├── css/
│   │   └── styles.css    # Minimal styling
│   ├── js/
│   │   ├── device-detection.js  # UA parsing and AR launch logic
│   │   └── vendor/              # Third-party libraries (if needed)
│   └── images/
│       ├── fire-preview.png     # Fallback preview images
│       ├── flood-preview.png
│       └── quake-preview.png
└── QR-codes/             # Existing QR code images (reference only)
    ├── fire.png
    ├── flood.png
    └── quake.png

# Alternative: If using build tooling
src/                      # Source files (pre-build)
├── pages/
│   ├── index.html
│   ├── fire.html
│   ├── flood.html
│   └── quake.html
├── scripts/
│   └── device-detection.js
└── styles/
    └── main.css

tests/                    # Testing structure
├── device-detection/     # Unit tests for UA parsing
│   └── test-detection.js
├── integration/          # Manual device test checklists
│   ├── ios-testing.md
│   └── android-testing.md
└── validation/           # Automated file validation
    └── model-validation.js
```

**Structure Decision**: Pure static website approach selected for maximum simplicity and performance (constitution principle IV). No backend server required - static hosting (Netlify, Vercel, GitHub Pages) can serve HTML pages and model files directly. Device detection happens client-side via JavaScript. Each model gets its own clean URL path (`/fire/`, `/flood/`, `/quake/`) via directory-based routing.

**Rationale**:
- Simplest possible architecture (constitution principle IV)
- Fastest performance (static file serving, no server processing)
- Easy deployment (any static host)
- Low maintenance (no server to manage)
- Meets all requirements (device detection can happen client-side)

**Alternative Considered**: Lightweight Node.js/Python server for server-side detection - rejected because client-side detection is sufficient and adds unnecessary complexity.

## Complexity Tracking

*No constitutional violations - section not required.*


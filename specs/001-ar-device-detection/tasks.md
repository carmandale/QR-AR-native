# Tasks: AR Device Detection and Model Serving

**Input**: Design documents from `/specs/001-ar-device-detection/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not explicitly requested in feature specification - no test tasks included. Focus on manual device testing per constitution requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- **Static web application**: `public/` at repository root (as defined in plan.md)
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md decisions (vanilla JS, zero dependencies, pure static site)

- [x] T001 Create static site directory structure: `public/`, `public/models/`, `public/assets/css/`, `public/assets/js/`, `public/assets/images/`
- [x] T002 [P] Create model-specific page directories: `public/fire/`, `public/flood/`, `public/quake/`
- [x] T003 [P] Configure MIME type headers in `public/_headers` file for USDZ and GLB serving
- [x] T004 [P] Create `.gitignore` to exclude build artifacts and OS files

**Checkpoint**: Basic project structure ready for content and code

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core JavaScript modules and CSS that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create device detection module in `public/assets/js/device-detection.js` with `detectDevice()` function (feature detection for iOS Quick Look, UA parsing for Android)
- [x] T006 Create AR launcher module in `public/assets/js/ar-launcher.js` with stub functions for iOS and Android (will be implemented per story)
- [x] T007 [P] Create base CSS styles in `public/assets/css/styles.css` with mobile-first responsive design, dark mode support, and button styles
- [x] T008 [P] Create landing page HTML in `public/index.html` with model gallery and links to individual AR pages

**Checkpoint**: Foundation ready - device detection works, base styling complete, user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - iOS User Views AR Model (Priority: P1) 🎯 MVP

**Goal**: iOS users can scan QR codes and launch USDZ models in Quick Look for all three disaster scenarios (fire, flood, quake)

**Independent Test**: Scan QR code with iPhone, verify USDZ launches in Quick Look within 5 seconds, model displays at correct scale with textures

### Implementation for User Story 1

- [x] T009 [P] [US1] Create Fire AR page HTML in `public/fire/index.html` with iOS Quick Look `<a rel="ar">` element, device detection script, and fallback content structure
- [x] T010 [P] [US1] Create Flood AR page HTML in `public/flood/index.html` with iOS Quick Look `<a rel="ar">` element, device detection script, and fallback content structure
- [x] T011 [P] [US1] Create Quake AR page HTML in `public/quake/index.html` with iOS Quick Look `<a rel="ar">` element, device detection script, and fallback content structure
- [x] T012 [US1] Implement `launchIOSQuickLook(usdzUrl, previewImage)` function in `public/assets/js/ar-launcher.js` to programmatically trigger Quick Look
- [x] T013 [US1] Integrate device detection in all three AR page HTMLs to conditionally show iOS Quick Look button vs fallback content
- [x] T014 [P] [US1] Link existing USDZ models: verify `models/fire.usdz` (37MB) and `models/quake.usdz` (46MB) are accessible and properly served with correct MIME type
- [ ] T015 [US1] Create or convert flood USDZ model: generate `public/models/flood.usdz` (<50MB) from existing source or create new **[MANUAL: Requires 3D modeling software]**
- [ ] T016 [P] [US1] Generate fire preview image: create `public/assets/images/fire-preview.png` (<200KB) from USDZ screenshot or render **[MANUAL: Use Reality Converter or Blender]**
- [ ] T017 [P] [US1] Generate flood preview image: create `public/assets/images/flood-preview.png` (<200KB) from USDZ screenshot or render **[MANUAL: Use Reality Converter or Blender]**
- [ ] T018 [P] [US1] Generate quake preview image: create `public/assets/images/quake-preview.png` (<200KB) from USDZ screenshot or render **[MANUAL: Use Reality Converter or Blender]**
- [x] T019 [US1] Add descriptive accessibility text to all three AR pages explaining disaster scenarios and system requirements
- [ ] T020 [US1] Test iOS Quick Look on physical iPhone device for all three models, verify scale (1 unit = 1 meter), textures, and <5s load time

**Checkpoint**: User Story 1 complete - iOS users can view all three disaster models in AR via Quick Look

---

## Phase 4: User Story 2 - Android User Views AR Model (Priority: P2)

**Goal**: Android users can scan QR codes and launch GLB models in Scene Viewer for all three disaster scenarios

**Independent Test**: Scan QR code with ARCore-compatible Android device, verify GLB launches in Scene Viewer within 5 seconds, model displays at correct scale with textures

### Implementation for User Story 2

- [x] T021 [P] [US2] Convert fire USDZ to GLB: create `public/models/fire.glb` (<20MB) using Reality Converter or Blender with Draco compression
- [ ] T022 [P] [US2] Convert flood USDZ to GLB: create `public/models/flood.glb` (<20MB) using Reality Converter or Blender with Draco compression **[MANUAL: Requires conversion from flood.usdz]**
- [ ] T023 [P] [US2] Convert quake USDZ to GLB: create `public/models/quake.glb` (<20MB) using Reality Converter or Blender with Draco compression **[MANUAL: Requires conversion from quake.usdz]**
- [x] T024 [US2] Implement `launchAndroidSceneViewer(glbUrl, modelName)` function in `public/assets/js/ar-launcher.js` to construct intent URL and redirect
- [x] T025 [US2] Update device detection integration in `public/fire/index.html` to show Android Scene Viewer button when Android detected
- [x] T026 [P] [US2] Update device detection integration in `public/flood/index.html` to show Android Scene Viewer button when Android detected
- [x] T027 [P] [US2] Update device detection integration in `public/quake/index.html` to show Android Scene Viewer button when Android detected
- [x] T028 [US2] Verify GLB files are served with correct MIME type (`model/gltf-binary`) and CORS headers in `public/_headers`
- [ ] T029 [US2] Test Android Scene Viewer on physical ARCore device for all three models, verify scale (1 unit = 1 meter), textures, and <5s load time **[REQUIRES DEVICE: ARCore-compatible Android]**

**Checkpoint**: User Stories 1 AND 2 complete - Both iOS and Android users can view AR models

---

## Phase 5: User Story 3 - Non-AR Device Shows Fallback Preview (Priority: P3)

**Goal**: Users without AR capability see helpful preview images and descriptive text instead of broken functionality

**Independent Test**: Visit URL from desktop browser or older smartphone, verify static preview image displays with descriptive text explaining AR requirements

### Implementation for User Story 3

- [x] T030 [US3] Update device detection integration in `public/fire/index.html` to show fallback preview image and descriptive text when no AR capability detected
- [x] T031 [P] [US3] Update device detection integration in `public/flood/index.html` to show fallback preview image and descriptive text when no AR capability detected
- [x] T032 [P] [US3] Update device detection integration in `public/quake/index.html` to show fallback preview image and descriptive text when no AR capability detected
- [x] T033 [US3] Add system requirements message to fallback content: "AR viewing requires iOS 12+ or ARCore-compatible Android device"
- [ ] T034 [P] [US3] Optimize preview images with WebP format and JPEG fallback for faster load times on slow connections **[MANUAL: Requires preview images to be created first]**
- [x] T035 [US3] Add comprehensive disaster scenario descriptions to fallback content for accessibility and non-AR users
- [ ] T036 [US3] Test fallback content on desktop browsers (Chrome, Firefox, Safari) and verify no AR buttons are shown **[REQUIRES TESTING: Desktop browsers]**
- [ ] T037 [US3] Test fallback content on older smartphone without AR capability and verify helpful messaging **[REQUIRES TESTING: Non-AR mobile device]**

**Checkpoint**: All three user stories complete - System works for iOS, Android, and non-AR devices

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Performance optimization, documentation, and validation across all user stories

- [ ] T038 [P] Run Lighthouse performance audit on all AR pages, optimize to meet <2s page load target on 4G **[REQUIRES DEPLOYMENT: Site must be live]**
- [ ] T039 [P] Run Lighthouse accessibility audit on all AR pages, target score >90 with WCAG AA compliance **[REQUIRES DEPLOYMENT: Site must be live]**
- [x] T040 [P] Validate USDZ file sizes are all <50MB per constitution requirement (fire: 37MB ✅, quake: 46MB ✅)
- [x] T041 [P] Validate GLB file sizes are all <20MB per constitution requirement (fire: 1.8MB ✅)
- [x] T042 Validate total HTML+CSS+JS bundle is <100KB per performance contract (20KB total ✅)
- [x] T043 [P] Add cache headers to `public/_headers` for long-term caching (1 year) of models and assets
- [ ] T044 Test page load performance on actual 4G mobile connection, verify <2s initial load **[REQUIRES DEPLOYMENT: Test on deployed site]**
- [ ] T045 Test AR launch performance on actual devices, verify <3s from page load to AR display **[REQUIRES DEVICE TESTING]**
- [x] T046 [P] Create README.md in repository root with project overview, setup instructions, and deployment guide
- [ ] T047 Update QR codes to point to deployed production URLs (fire, flood, quake pages) **[REQUIRES DEPLOYMENT: Get production URLs first]**
- [ ] T048 Run through quickstart.md validation checklist to ensure all steps work correctly **[REQUIRES MANUAL VALIDATION]**

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if team capacity allows)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1, but typically follows P1 in priority order
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1/US2 fallback structures but independently testable

### Within Each User Story

- Preview images can be created in parallel (marked [P])
- Model files can be created/converted in parallel (marked [P])
- HTML pages can be created in parallel (marked [P])
- Device detection integration happens after launcher functions are complete
- Physical device testing happens after all code and assets are ready

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004)
- All Foundational tasks marked [P] can run in parallel (T007, T008)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within US1: Preview images (T016-T018) can be generated in parallel
- Within US1: HTML pages (T009-T011) can be created in parallel
- Within US2: GLB conversions (T021-T023) can run in parallel
- Within US2: HTML updates (T026-T027) can run in parallel
- Polish tasks (T038-T041) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all preview image generation together:
Task: "Generate fire preview image: create public/assets/images/fire-preview.png"
Task: "Generate flood preview image: create public/assets/images/flood-preview.png"
Task: "Generate quake preview image: create public/assets/images/quake-preview.png"

# Launch all HTML page creation together:
Task: "Create Fire AR page HTML in public/fire/index.html"
Task: "Create Flood AR page HTML in public/flood/index.html"
Task: "Create Quake AR page HTML in public/quake/index.html"
```

---

## Parallel Example: User Story 2

```bash
# Launch all USDZ to GLB conversions together:
Task: "Convert fire USDZ to GLB: create public/models/fire.glb"
Task: "Convert flood USDZ to GLB: create public/models/flood.glb"
Task: "Convert quake USDZ to GLB: create public/models/quake.glb"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup → Project structure ready
2. Complete Phase 2: Foundational → Device detection and base styling ready
3. Complete Phase 3: User Story 1 → iOS AR viewing complete
4. **STOP and VALIDATE**: Test on physical iPhone with all three QR codes
5. Deploy to Cloudflare Pages for initial demo/validation

**This delivers immediate value**: iOS users (significant AR market) can view all disaster models in AR

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (~2 hours per quickstart.md)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! iOS AR working)
3. Add User Story 2 → Test independently → Deploy/Demo (Full cross-platform AR)
4. Add User Story 3 → Test independently → Deploy/Demo (Complete accessibility)
5. Add Polish → Final production optimization and documentation

Each story adds value without breaking previous stories.

### Sequential Strategy (Single Developer)

**Recommended path for one developer**:

1. **Week 1**: Setup + Foundational + User Story 1
   - Get iOS AR working end-to-end
   - Validate on physical iPhone
   - Deploy MVP to Cloudflare Pages

2. **Week 2**: User Story 2
   - Convert models to GLB
   - Implement Android Scene Viewer
   - Validate on physical Android device

3. **Week 3**: User Story 3 + Polish
   - Add fallback content
   - Performance optimization
   - Documentation and QR code updates

### Parallel Team Strategy

With multiple developers:

1. **All team members**: Complete Setup + Foundational together (1 day)
2. **Once Foundational is done**:
   - Developer A: User Story 1 (iOS Quick Look)
   - Developer B: User Story 2 (Android Scene Viewer) - can start model conversions immediately
   - Developer C: User Story 3 (Fallback content) + Polish tasks
3. Stories complete and integrate independently

---

## Constitution Compliance Checkpoints

After each phase, verify:

### After User Story 1:
- ✅ **Principle I (Device-Aware)**: iOS detection working, USDZ served automatically
- ✅ **Principle II (Performance)**: Page load <2s, AR launch <3s on iPhone
- ✅ **Principle IV (Simplicity)**: Zero dependencies used, vanilla JS only

### After User Story 2:
- ✅ **Principle I (Device-Aware)**: Android detection working, GLB served automatically
- ✅ **Principle V (Asset Quality)**: GLB models <20MB, tested on Android device

### After User Story 3:
- ✅ **Principle III (Progressive Enhancement)**: Fallback content works on all devices
- ✅ Accessibility: Descriptive text, alt attributes, screen reader compatible

### After Polish:
- ✅ **Principle II (Performance)**: All metrics validated (<2s page, <3s AR, <5s total)
- ✅ **Principle V (Asset Quality)**: All models validated, version controlled, documented
- ✅ All 12 Functional Requirements (FR-001 through FR-012) verified

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Physical device testing is REQUIRED per constitution (not optional)
- Model file sizes are constitutional constraints, not suggestions
- Stop at any checkpoint to validate story independently
- Manual testing on physical devices is more important than automated tests for AR experiences
- Commit after each task or logical group
- Deploy frequently to Cloudflare Pages for validation

---

## Edge Case Handling (from spec.md)

Tasks above implicitly handle these edge cases:

- **Camera permission denied**: Native AR viewers (Quick Look, Scene Viewer) handle this - web app shows appropriate buttons
- **Slow network**: Long-term cache headers (T043) and optimized file sizes help; native viewers show loading states
- **Quick Look fails to launch**: Fallback content ensures user still gets value (US3)
- **Invalid QR URLs**: Standard 404 handling from static host
- **Missing models**: File validation tasks (T040-T041) prevent deployment with missing files
- **Borderline AR devices**: Feature detection (T005) is conservative; if device claims AR support, we trust it


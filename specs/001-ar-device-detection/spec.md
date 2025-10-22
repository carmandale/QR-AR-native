# Feature Specification: AR Device Detection and Model Serving

**Feature Branch**: `001-ar-device-detection`
**Created**: 2025-10-19
**Status**: Draft
**Input**: User description: "build a simple web app that will host the models and detect if the mobile device is ios or android and display the model using native ar device tools, quicklook or the equivalent for android."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - iOS User Views AR Model (Priority: P1)

A user with an iPhone scans a QR code at a physical location (museum, event, classroom) and immediately sees a 3D AR model launch in their native AR viewer without any manual configuration or format selection.

**Why this priority**: This is the core MVP functionality - iOS devices represent a significant portion of mobile AR-capable devices, and Quick Look provides the best native AR experience on these devices. This story alone delivers immediate value.

**Independent Test**: Can be fully tested by scanning a QR code with an iPhone and verifying that the USDZ model launches in Quick Look within 5 seconds total time.

**Acceptance Scenarios**:

1. **Given** a user has an iPhone with AR capability, **When** they scan the QR code for the "fire" disaster model, **Then** the web page detects iOS and automatically triggers Quick Look to display the fire model in AR
2. **Given** a user has an iPhone with AR capability, **When** they scan the QR code for the "flood" disaster model, **Then** the web page detects iOS and automatically triggers Quick Look to display the flood model in AR
3. **Given** a user has an iPhone with AR capability, **When** they scan the QR code for the "quake" disaster model, **Then** the web page detects iOS and automatically triggers Quick Look to display the quake model in AR
4. **Given** a user's iPhone successfully launches Quick Look, **When** they view the AR model, **Then** the model appears at correct scale (1 unit = 1 meter) with all textures properly rendered

---

### User Story 2 - Android User Views AR Model (Priority: P2)

A user with an Android phone scans a QR code at a physical location and immediately sees a 3D AR model launch in their native AR viewer (Scene Viewer or equivalent) without any manual configuration or format selection.

**Why this priority**: Android devices represent the other major mobile platform. While iOS (P1) provides the MVP, adding Android support makes the system accessible to the majority of mobile users and completes the cross-platform experience.

**Independent Test**: Can be fully tested by scanning a QR code with an ARCore-compatible Android device and verifying that the GLB model launches in Scene Viewer within 5 seconds total time.

**Acceptance Scenarios**:

1. **Given** a user has an ARCore-compatible Android device, **When** they scan the QR code for the "fire" disaster model, **Then** the web page detects Android and automatically triggers Scene Viewer to display the fire model in AR
2. **Given** a user has an ARCore-compatible Android device, **When** they scan the QR code for the "flood" disaster model, **Then** the web page detects Android and automatically triggers Scene Viewer to display the flood model in AR
3. **Given** a user has an ARCore-compatible Android device, **When** they scan the QR code for the "quake" disaster model, **Then** the web page detects Android and automatically triggers Scene Viewer to display the quake model in AR
4. **Given** a user's Android device successfully launches Scene Viewer, **When** they view the AR model, **Then** the model appears at correct scale (1 unit = 1 meter) with all textures properly rendered

---

### User Story 3 - Non-AR Device Shows Fallback Preview (Priority: P3)

A user with a device that doesn't support AR (desktop browser, older smartphone) scans or visits a QR code URL and sees a helpful preview image or message explaining what the AR experience would show, ensuring they still get value from visiting the page.

**Why this priority**: While AR is the primary experience, providing graceful degradation ensures accessibility and prevents user frustration. Desktop users researching the models, older device users, and accessibility tools all benefit from fallback content.

**Independent Test**: Can be fully tested by visiting the URL from a desktop browser and verifying that a static preview image or 3D viewer fallback is displayed instead of a broken AR button.

**Acceptance Scenarios**:

1. **Given** a user visits the page from a desktop browser, **When** the page loads, **Then** they see a static preview image or interactive 3D viewer showing the model (not an AR launch button)
2. **Given** a user has a smartphone without AR capability, **When** they scan the QR code, **Then** they see a message explaining "AR viewing requires iOS 12+ or ARCore-compatible Android device" with a preview of the model
3. **Given** a user views the fallback content, **When** they read the page, **Then** they can understand what disaster scenario the model represents through descriptive text and images

---

### Edge Cases

- What happens when a user's device has AR capability but denies camera permissions?
- How does the system handle slow network connections where the model file takes >10 seconds to download?
- What happens if a user's iOS version supports AR but Quick Look fails to launch?
- How does the system handle QR codes that are damaged or partially obscured (invalid URLs)?
- What happens when a user scans a QR code for a model that doesn't exist (404)?
- How does the system handle devices that are borderline AR-capable (e.g., older ARCore devices with limited support)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST detect the device platform (iOS vs Android vs other) when a user visits a model URL
- **FR-002**: System MUST serve USDZ format models to detected iOS devices
- **FR-003**: System MUST serve GLB format models to detected Android devices
- **FR-004**: System MUST provide unique URLs for each disaster model (fire, flood, quake)
- **FR-005**: System MUST automatically trigger the native AR viewer (Quick Look for iOS, Scene Viewer for Android) without requiring user interaction beyond the initial QR code scan
- **FR-006**: System MUST display fallback content (preview image or 3D viewer) for devices that don't support AR
- **FR-007**: System MUST handle all three existing disaster models: fire, flood, and quake
- **FR-008**: System MUST preserve model scale consistency across platforms (1 unit = 1 meter)
- **FR-009**: System MUST preserve model textures and visual quality when serving to both platforms
- **FR-010**: System MUST load the initial page within 2 seconds on 4G mobile connections
- **FR-011**: System MUST initiate AR model launch within 3 seconds after page load
- **FR-012**: System MUST provide descriptive text for each model explaining the disaster scenario (for accessibility and fallback content)

### Key Entities

- **AR Model**: Represents a 3D disaster scenario asset with dual formats (USDZ for iOS, GLB for Android), metadata (disaster type, description), and validation status (tested on both platforms)
- **Model URL**: Represents a unique web endpoint that maps to a specific AR model and handles device detection and format serving
- **Device Detection Result**: Represents the outcome of platform detection including platform type (iOS/Android/Other), AR capability status, and format to serve

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can launch AR models from QR code scan to AR viewer display in under 5 seconds total time (95th percentile)
- **SC-002**: 90% of iOS users successfully launch Quick Look without errors on first attempt
- **SC-003**: 90% of Android users successfully launch Scene Viewer without errors on first attempt
- **SC-004**: 100% of non-AR devices receive appropriate fallback content instead of broken functionality
- **SC-005**: All three disaster models (fire, flood, quake) display correctly on both iOS and Android platforms with consistent scale and textures
- **SC-006**: Page load time remains under 2 seconds on 4G mobile connections
- **SC-007**: Zero manual format selection required - all platform detection and format serving happens automatically

## Assumptions

- Users have internet connectivity when scanning QR codes (models require download)
- QR codes will be generated externally and point to the correct model URLs (QR generation is out of scope)
- Existing model files (fire.usdz, fire.glb, etc.) are properly formatted and optimized
- iOS devices running iOS 12+ support Quick Look AR viewing
- Android devices with ARCore installed support Scene Viewer
- Model files are within acceptable size limits: USDZ <50MB, GLB <20MB
- Device detection can be accomplished via user agent string parsing (standard approach)
- Static hosting or lightweight server can handle expected traffic volume (exact traffic not specified, assuming moderate educational/event usage)


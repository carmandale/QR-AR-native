/**
 * AR Launcher Module
 *
 * Provides functions to launch native AR viewers:
 * - iOS Quick Look (USDZ files)
 * - Android Scene Viewer (GLB files)
 *
 * Constitution Principle IV: Simplicity Over Cleverness
 * - Direct platform APIs (no frameworks)
 * - Minimal, focused functions
 * - Clear error handling
 */

/**
 * Launches iOS Quick Look with the specified USDZ model
 *
 * Requirements:
 * - Must be called within user interaction event (click, touch)
 * - Device must support Quick Look (check with detectDevice() first)
 * - USDZ file must be served with Content-Type: model/vnd.usdz+zip
 *
 * @param {string} usdzUrl - Absolute or relative URL to USDZ file
 * @param {string} [previewImage] - Optional URL to preview image (shown while loading)
 * @throws {Error} If Quick Look is not supported
 *
 * @example
 * button.addEventListener('click', () => {
 *   launchIOSQuickLook('/models/fire.usdz', '/assets/images/fire-preview.png');
 * });
 */
function launchIOSQuickLook(usdzUrl, previewImage) {
	// Feature detection
	const a = document.createElement("a");
	if (!a.relList || !a.relList.supports("ar")) {
		throw new Error("iOS Quick Look is not supported on this device");
	}

	// Create temporary anchor element with Quick Look attributes
	const anchor = document.createElement('a');
	anchor.setAttribute('rel', 'ar');
	anchor.setAttribute('href', usdzUrl);

	// Add preview image if provided
	if (previewImage) {
		const img = document.createElement('img');
		img.src = previewImage;
		img.alt = 'View in AR';
		anchor.appendChild(img);
	}

	// Programmatically trigger click
	// IMPORTANT: This MUST be called within a user interaction event
	// Browsers block programmatic clicks outside of user gestures
	anchor.click();
}

/**
 * Launches Android Scene Viewer with the specified GLB model
 *
 * Requirements:
 * - Must be called within user interaction event (click, touch)
 * - Device must have ARCore installed (Android 7.0+)
 * - GLB file must be accessible via absolute HTTPS URL
 *
 * @param {string} glbUrl - Absolute or relative URL to GLB file
 * @param {string} modelName - Display name for the model (shown in Scene Viewer)
 *
 * @example
 * button.addEventListener('click', () => {
 *   launchAndroidSceneViewer('/models/fire.glb', 'Fire Disaster Scenario');
 * });
 */
function launchAndroidSceneViewer(glbUrl, modelName) {
	// Convert relative URL to absolute URL
	const absoluteUrl = new URL(glbUrl, window.location.href).href;

	// Encode parameters for intent URL
	const fileParam = encodeURIComponent(absoluteUrl);
	const titleParam = encodeURIComponent(modelName);
	const fallbackParam = encodeURIComponent(window.location.href);

	// Construct Android intent URL for Scene Viewer
	// Documentation: https://developers.google.com/ar/develop/scene-viewer
	const intentUrl = `intent://arvr.google.com/scene-viewer/1.0?file=${fileParam}&mode=ar_only&title=${titleParam}#Intent;scheme=https;package=com.google.android.googlequicksearchbox;action=android.intent.action.VIEW;S.browser_fallback_url=${fallbackParam};end;`;

	// Redirect to intent URL (launches Scene Viewer or falls back to current page)
	window.location.href = intentUrl;
}

// Export for use in HTML pages (ES5 compatible - no modules)
// Usage:
//   launchIOSQuickLook('/models/fire.usdz');
//   launchAndroidSceneViewer('/models/fire.glb', 'Fire Model');

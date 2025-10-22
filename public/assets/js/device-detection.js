/**
 * Device Detection Module
 *
 * Detects device platform and AR capabilities using feature detection
 * and minimal user agent parsing (zero dependencies).
 *
 * Constitution Principle IV: Simplicity Over Cleverness
 * - No external libraries (UAParser.js, Bowser, etc.)
 * - Feature detection first, UA parsing as fallback
 * - Clear, straightforward code
 */

/**
 * Detects device platform and AR capabilities
 *
 * @returns {Object} Device information
 * @returns {string} .platform - "ios" | "android" | "desktop" | "unknown"
 * @returns {boolean} .arCapable - Can this device launch AR experiences?
 * @returns {string|null} .arMethod - "quicklook" | "sceneviewer" | null
 * @returns {string} .userAgent - Raw user agent string (for debugging)
 * @returns {Object} .features - Detailed feature detection results
 * @returns {boolean} .features.quickLookSupported - iOS Quick Look available
 * @returns {boolean} .features.sceneViewerSupported - Android Scene Viewer available
 * @returns {boolean} .features.webxrSupported - WebXR API available (future)
 */
function detectDevice() {
	const ua = navigator.userAgent;

	// iOS detection (iPad|iPhone|iPod)
	// !window.MSStream excludes IE11 on Windows Phone
	const iOS = /iPad|iPhone|iPod/.test(ua) && !window.MSStream;

	// Android detection
	const Android = /Android/i.test(ua);

	// iOS Quick Look feature detection (most reliable method)
	const a = document.createElement("a");
	const quickLookSupported = iOS && a.relList && a.relList.supports("ar");

	// Android Scene Viewer support detection (approximate)
	// Scene Viewer requires Android 7.0+ with ARCore
	const androidVersion = Android ? parseFloat(ua.match(/Android (\d+\.\d+)/)?.[1]) : 0;
	const sceneViewerSupported = Android && androidVersion >= 7.0;

	// WebXR support detection (future consideration)
	const webxrSupported = 'xr' in navigator && 'isSessionSupported' in navigator.xr;

	// Determine platform and AR method
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
		// Device is iOS or Android but lacks AR capability
		platform = iOS ? "ios" : "android";
		arCapable = false;
		arMethod = null;
	} else {
		// Desktop or unknown device
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

// Export for use in HTML pages (ES5 compatible - no modules)
// Usage: const device = detectDevice();

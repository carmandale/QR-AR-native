#!/usr/bin/env python3
"""
Process all USDZ files: compress textures and create GLB versions.
"""

import subprocess
import sys
from pathlib import Path

# Configuration
BLENDER_PATH = "/Applications/Blender4.5.app/Contents/MacOS/Blender"
SCRIPT_DIR = Path(__file__).parent
BLENDER_SCRIPT = SCRIPT_DIR / "compress_and_convert.py"
PROJECT_ROOT = SCRIPT_DIR.parent
TEXTURE_QUALITY = 85  # JPEG quality 0-100

# Directories to process
MODEL_DIRS = [
	PROJECT_ROOT / "models",
	PROJECT_ROOT / "public" / "models"
]

def process_usdz_file(usdz_path: Path, quality: int = TEXTURE_QUALITY):
	"""Process a single USDZ file: create compressed GLB version."""
	print(f"\n{'='*60}")
	print(f"Processing: {usdz_path.name}")
	print(f"{'='*60}")

	# Create GLB output path (same directory as USDZ)
	glb_path = usdz_path.with_suffix('.glb')

	# Run Blender conversion
	cmd = [
		BLENDER_PATH,
		"--background",
		"--python", str(BLENDER_SCRIPT),
		"--",
		str(usdz_path),
		str(glb_path),
		str(quality)
	]

	print(f"Running: {' '.join(cmd)}")

	try:
		result = subprocess.run(
			cmd,
			capture_output=True,
			text=True,
			timeout=300  # 5 minutes timeout
		)

		if result.returncode == 0:
			print(f"✓ Successfully created: {glb_path}")
			return True
		else:
			print(f"✗ Error processing {usdz_path.name}")
			print(f"STDOUT: {result.stdout}")
			print(f"STDERR: {result.stderr}")
			return False
	except subprocess.TimeoutExpired:
		print(f"✗ Timeout processing {usdz_path.name}")
		return False
	except Exception as e:
		print(f"✗ Exception processing {usdz_path.name}: {e}")
		return False

def main():
	"""Main entry point."""
	print("USDZ to GLB Converter with Texture Compression")
	print(f"Texture Quality: {TEXTURE_QUALITY}")
	print(f"Blender: {BLENDER_PATH}")

	# Check if Blender exists
	if not Path(BLENDER_PATH).exists():
		print(f"ERROR: Blender not found at {BLENDER_PATH}")
		sys.exit(1)

	# Check if Blender script exists
	if not BLENDER_SCRIPT.exists():
		print(f"ERROR: Blender script not found at {BLENDER_SCRIPT}")
		sys.exit(1)

	# Find all USDZ files
	usdz_files = []
	for model_dir in MODEL_DIRS:
		if model_dir.exists():
			usdz_files.extend(model_dir.glob("*.usdz"))

	if not usdz_files:
		print("No USDZ files found to process")
		sys.exit(0)

	print(f"\nFound {len(usdz_files)} USDZ file(s) to process:")
	for usdz_file in usdz_files:
		print(f"  - {usdz_file.relative_to(PROJECT_ROOT)}")

	# Process each file
	success_count = 0
	fail_count = 0

	for usdz_file in usdz_files:
		if process_usdz_file(usdz_file):
			success_count += 1
		else:
			fail_count += 1

	# Summary
	print(f"\n{'='*60}")
	print("Processing Summary")
	print(f"{'='*60}")
	print(f"Total files: {len(usdz_files)}")
	print(f"Successful: {success_count}")
	print(f"Failed: {fail_count}")

	sys.exit(0 if fail_count == 0 else 1)

if __name__ == "__main__":
	main()

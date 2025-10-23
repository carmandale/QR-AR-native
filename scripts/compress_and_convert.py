#!/usr/bin/env python3
"""
Blender script to compress USDZ textures and convert to GLB format.
Usage: blender --background --python compress_and_convert.py -- <input.usdz> <output.glb> [quality]
"""

import bpy
import sys
import os
from pathlib import Path

def compress_textures(quality=85):
	"""Compress all textures in the current scene."""
	for image in bpy.data.images:
		if image.source == 'FILE' and image.filepath:
			# Get the image path
			img_path = bpy.path.abspath(image.filepath)
			if os.path.exists(img_path):
				print(f"Compressing texture: {image.name}")

				# Pack the image to work with it in memory
				if not image.packed_file:
					image.pack()

				# Set file format and compression
				image.file_format = 'JPEG' if image.depth == 24 else 'PNG'

				# For JPEG, set quality
				if image.file_format == 'JPEG':
					image.quality = quality

				# For PNG, enable compression
				if image.file_format == 'PNG':
					image.compression = 90  # 0-100, higher = more compression

def convert_usdz_to_glb(input_path, output_path, texture_quality=85):
	"""Convert USDZ to GLB with compressed textures."""
	print(f"Converting: {input_path} -> {output_path}")

	# Clear the scene
	bpy.ops.wm.read_factory_settings(use_empty=True)

	# Import USDZ
	try:
		# Try importing as USD
		if hasattr(bpy.ops.wm, 'usd_import'):
			bpy.ops.wm.usd_import(filepath=str(input_path))
			print("Imported using USD importer")
		else:
			print("USD importer not available, trying alternative import")
			# Fallback to other importers if available
			if hasattr(bpy.ops.import_scene, 'usd'):
				bpy.ops.import_scene.usd(filepath=str(input_path))
			else:
				print("ERROR: No USD importer found in Blender")
				return False
	except Exception as e:
		print(f"Error importing USDZ: {e}")
		return False

	# Compress textures
	compress_textures(quality=texture_quality)

	# Export as GLB
	try:
		# Blender 4.5 compatible export parameters
		bpy.ops.export_scene.gltf(
			filepath=str(output_path),
			export_format='GLB',
			export_image_format='AUTO',  # Let Blender choose best format
			export_jpeg_quality=texture_quality,
			export_keep_originals=False,
			export_texture_dir='',  # Embed textures in GLB
		)
		print(f"Successfully exported to: {output_path}")
		return True
	except Exception as e:
		print(f"Error exporting GLB: {e}")
		return False

def main():
	"""Main entry point when run as Blender script."""
	# Get arguments after --
	argv = sys.argv
	if "--" in argv:
		argv = argv[argv.index("--") + 1:]
	else:
		print("ERROR: No arguments provided. Usage: blender --background --python compress_and_convert.py -- <input.usdz> <output.glb> [quality]")
		sys.exit(1)

	if len(argv) < 2:
		print("ERROR: Need at least input and output paths")
		print("Usage: blender --background --python compress_and_convert.py -- <input.usdz> <output.glb> [quality]")
		sys.exit(1)

	input_path = Path(argv[0])
	output_path = Path(argv[1])
	quality = int(argv[2]) if len(argv) > 2 else 85

	if not input_path.exists():
		print(f"ERROR: Input file not found: {input_path}")
		sys.exit(1)

	# Create output directory if needed
	output_path.parent.mkdir(parents=True, exist_ok=True)

	# Convert
	success = convert_usdz_to_glb(input_path, output_path, quality)
	sys.exit(0 if success else 1)

if __name__ == "__main__":
	main()

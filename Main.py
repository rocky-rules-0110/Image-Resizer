import os
import sys
import argparse
import cv2

image_path = 'Example.jpg'

# CLI: run with --nogui to skip opening image windows (useful if running headless)
parser = argparse.ArgumentParser(description='Resize an image to three sizes and save results')
parser.add_argument('--nogui', action='store_true', help='Do not open image display windows')
args = parser.parse_args()

if not os.path.exists(image_path):
	print(f"File not found: {image_path}")
	sys.exit(1)

image = cv2.imread(image_path)
if image is None:
	print(f"Failed to load image: {image_path} (cv2.imread returned None). Check the file and OpenCV build.)")
	sys.exit(1)

if not args.nogui:
	cv2.namedWindow('Loaded Image', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Loaded Image', 800, 500)
	cv2.imshow('Loaded Image', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
print(f"Image Dimensions: {image.shape}")

# Resize targets: (width, height)
resize_targets = {
	'input_image_small.jpg': (200, 200),
	'input_image_medium.jpg': (400, 400),
	'input_image_large.jpg': (600, 600),
}

for out_name, (w, h) in resize_targets.items():
	# Choose interpolation: INTER_AREA for shrinking, INTER_LINEAR for enlarging
	interp = cv2.INTER_AREA if w <= image.shape[1] and h <= image.shape[0] else cv2.INTER_LINEAR
	resized = cv2.resize(image, (w, h), interpolation=interp)
	success = cv2.imwrite(out_name, resized)
	if success:
		print(f"Saved {out_name} ({w}x{h})")
	else:
		print(f"Failed to save {out_name}")
	# Optionally show the resized image and wait for a keypress to move to the next one
	if not args.nogui:
		cv2.namedWindow(out_name, cv2.WINDOW_NORMAL)
		cv2.imshow(out_name, resized)
		print(f"Showing {out_name} - press any key to continue...")
		cv2.waitKey(0)
		cv2.destroyWindow(out_name)

# Post-run check: list the saved files and their sizes so there's a clear terminal confirmation
saved_files = [f for f in resize_targets.keys() if os.path.exists(f)]
if saved_files:
	print('\nVerification: saved files:')
	for f in saved_files:
		try:
			size = os.path.getsize(f)
			print(f" - {f}: {size} bytes")
		except OSError:
			print(f" - {f}: (could not read size)")
else:
	print('\nVerification: no resized files were found in the current directory')


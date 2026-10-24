import os
import subprocess
import csv

img_dir = "DB1_B_png"
images = sorted([f for f in os.listdir(img_dir) if f.endswith("png")])
csv_path = "nfiq_quality_scores.csv"

with open(csv_path, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["image", "nfiq_quality_score"])

    print("running nfiq assesment...")
    for img in images:
        img_path = os.path.join(img_dir, img)
        result = subprocess.run(['nfiq', img_path], capture_output=True, text=True)
        score_str = result.stdout.strip()
        score = int(score_str) if score_str.isdigit() else None
        writer.writerow([img, score])

print("saved to ", csv_path)
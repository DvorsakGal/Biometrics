import os
import subprocess
import itertools
import csv

img_dir = "DB1_B_png"
out_dir = "out"

os.makedirs(out_dir, exist_ok=True)

# 1. minutae points
png_files = [f for f in os.listdir(img_dir) if f.endswith('.png')]
print(f"Found {len(png_files)} PNG files, running mindtct")

for img in png_files:
    img_path = os.path.join(img_dir, img)
    out_path = os.path.join(out_dir, img.replace('.png', ''))
    subprocess.run(['mindtct', img_path, out_path])


# 2. bozorth3 comparisons
xyt_files = sorted([f for f in os.listdir(out_dir) if f.endswith('.xyt')])
# unique pairs
pairs = list(itertools.combinations(xyt_files, 2))
print(f"Found {len(pairs)} unique pairs, running bozorth3...")

results = []
for file1, file2 in pairs:
    path1 = os.path.join(out_dir, file1)
    path2 = os.path.join(out_dir, file2)
    result = subprocess.run(['bozorth3', path1, path2], capture_output=True, text=True)
    score_str = result.stdout.strip()
    score = int(score_str) if score_str.isdigit() else 0
    results.append({
        "img1": file1,
        "img2": file2,
        "score": score
    })

print("Comparison complete. First 5 scores:")
for r in results[:5]:
    print(f"{r['img1']} vs {r['img2']}: {r['score']}")


csv_path = "bozorth_results.csv"
with open(csv_path, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["img1", "img2", "subject1", "subject2", "score", "type"])
    
    for r in results:
        # get subject id
        sub1 = r['img1'].split('_')[0]
        sub2 = r['img2'].split('_')[0]
        
        #genuine or impostor comparison
        match_type = "genuine" if sub1 == sub2 else "impostor"
        
        writer.writerow([r['img1'], r['img2'], sub1, sub2, r['score'], match_type])

print(f"Results successfully saved to {csv_path}")
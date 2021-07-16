import os

print("Creating required directories")
for d in ['unpack', 'metrics', 'preprocessing', 'features', 'meta', 'model', 'rejected']:
    os.makedirs(os.path.join('data', d), exist_ok=True)

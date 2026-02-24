import os

def repair_file(path):
    try:
        with open(path, 'rb') as f:
            raw = f.read()
        
        # Sig: \xc3\x83 is UTF-8 for Ã, the start of almost every mangled Spanish char
        if b'\xc3\x83' in raw:
            try:
                # 1. Read as mangled UTF-8
                content = raw.decode('utf-8')
                # 2. Re-encode as CP1252 (the incorrect intermediate encoding)
                repaired_raw = content.encode('cp1252')
                # 3. Correctly decode as UTF-8
                repaired_content = repaired_raw.decode('utf-8')
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(repaired_content)
                print(f"Repaired: {path}")
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                print(f"Failed to reverse {path}: {e}")
    except Exception as e:
        print(f"Error on {path}: {e}")

for root_dir in ['proveedores/templates', 'templates']:
    if not os.path.exists(root_dir): continue
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                repair_file(os.path.join(root, file))

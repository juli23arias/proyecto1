import os

def fix_file(path, replacements):
    if not os.path.exists(path):
        print(f"Skipping {path}: Not found")
        return
    
    with open(path, 'rb') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
    
    if new_content != content:
        with open(path, 'wb') as f:
            f.write(new_content)
        print(f"Fixed {path}")
    else:
        print(f"No changes needed for {path}")

# document_list.html replacements
fix_file(r'proveedores\templates\proveedores\admin\document_list.html', [
    (b'estado_actual=="pendiente"', b'estado_actual == "pendiente"'),
    (b'estado_actual=="aprobado"', b'estado_actual == "aprobado"'),
    (b'estado_actual=="rechazado"', b'estado_actual == "rechazado"'),
    (b'tipo_actual==t.id', b'tipo_actual == t.id'),
])

# document_outbox.html replacements
fix_file(r'proveedores\templates\proveedores\admin\document_outbox.html', [
    (b'tipo_actual==t.id', b'tipo_actual == t.id'),
    # Fix the split tag (trying both CRLF and LF)
    (b'selected{% endif %}>{{\r\n                        t.nombre }}', b'selected{% endif %}>{{ t.nombre }}'),
    (b'selected{% endif %}>{{\n                        t.nombre }}', b'selected{% endif %}>{{ t.nombre }}'),
])

# document_review.html replacements
fix_file(r'proveedores\templates\proveedores\admin\document_review.html', [
    (b'object.estado=="pendiente"', b'object.estado == "pendiente"'),
    (b'object.estado=="aprobado"', b'object.estado == "aprobado"'),
    (b'object.estado=="rechazado"', b'object.estado == "rechazado"'),
])

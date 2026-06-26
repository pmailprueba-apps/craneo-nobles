import re
import os
import subprocess

def get_path_bbox(path_d):
    tokens = re.findall(r'([A-Za-z]|[-+]?\d*\.\d+|[-+]?\d+)', path_d)
    current_x = 0.0
    current_y = 0.0
    points = []
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == 'M' or token == 'm':
            val1 = float(tokens[i+1])
            val2 = float(tokens[i+2])
            if token == 'M':
                current_x = val1
                current_y = val2
            else:
                current_x += val1
                current_y += val2
            points.append((current_x, current_y))
            i += 3
        elif token == 'c':
            while i + 6 < len(tokens) and not tokens[i+1].isalpha():
                dx1 = float(tokens[i+1])
                dy1 = float(tokens[i+2])
                dx2 = float(tokens[i+3])
                dy2 = float(tokens[i+4])
                dx3 = float(tokens[i+5])
                dy3 = float(tokens[i+6])
                
                points.append((current_x + dx1, current_y + dy1))
                points.append((current_x + dx2, current_y + dy2))
                current_x += dx3
                current_y += dy3
                points.append((current_x, current_y))
                i += 6
            i += 1
        elif token == 'l':
            while i + 2 < len(tokens) and not tokens[i+1].isalpha():
                dx = float(tokens[i+1])
                dy = float(tokens[i+2])
                current_x += dx
                current_y += dy
                points.append((current_x, current_y))
                i += 2
            i += 1
        elif token == 'z' or token == 'Z':
            i += 1
        else:
            i += 1
            
    if not points:
        return None
        
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)

def process_vector(threshold, output_name):
    img_w, img_h = 821, 1024
    
    os.makedirs("trace_temp", exist_ok=True)
    
    bmp_path = f"trace_temp/processed_v7_{threshold}.bmp"
    png_path = f"trace_temp/processed_v7_{threshold}.png"
    svg_temp_path = f"trace_temp/raw_v7_{threshold}.svg"
    
    # ImageMagick: 
    # 1. Negar imagen (para tener fondo claro y cráneo oscuro).
    # 2. Flat-field division (para normalizar iluminación sin quemar/clampear el contraste).
    # 3. Escala de grises + Binarizar (threshold).
    # 4. Enmascarar bordes, tornillos, watermark y texto con color BLANCO (para que potrace no los trace).
    # 5. Salvar como BMP para potrace.
    cmd_magick = [
        "magick", "original_design.jpg",
        "-negate",
        "(", "+clone", "-blur", "0x50", ")",
        "-compose", "Divide", "-composite",
        "-colorspace", "gray",
        "-threshold", f"{threshold}%",
        "-fill", "white",
        "-draw", "rectangle 0,0 821,20",            # Borde superior
        "-draw", "rectangle 0,0 20,1024",           # Borde izquierdo
        "-draw", "rectangle 801,0 821,1024",         # Borde derecho
        "-draw", "rectangle 0,1004 821,1024",       # Borde inferior
        "-draw", "rectangle 730,0 821,80",          # Tornillo superior derecho
        "-draw", "rectangle 200,20 230,40",         # Ruido pequeño superior
        "-draw", "rectangle 0,625 821,1024",        # Borrar textos, marcas y tornillo inferior completo
        bmp_path
    ]
    
    print(f"Ejecutando ImageMagick para umbral {threshold}%...")
    subprocess.run(cmd_magick, check=True)
    
    # También generamos una versión PNG del BMP procesado para la vista previa HTML
    subprocess.run(["magick", bmp_path, png_path], check=True)
    
    # Vectorizar con potrace
    subprocess.run(["potrace", "-s", "-o", svg_temp_path, bmp_path], check=True)
    
    # Leer SVG temporal y limpiar caminos de ruido
    with open(svg_temp_path, 'r') as f:
        content = f.read()
        
    paths = re.findall(r'<path[^>]*d="([^"]+)"[^>]*>', content)
    
    cleaned_paths = []
    for p in paths:
        if len(p) >= 80: # Ignorar ruido pequeño
            cleaned_paths.append(p)
            
    print(f"Caminos filtrados para umbral {threshold}%: {len(cleaned_paths)} de {len(paths)}")
    
    # Calcular Bounding Box en espacio transformado
    all_points_trans = []
    for p in cleaned_paths:
        bbox = get_path_bbox(p)
        if bbox:
            min_x, min_y, max_x, max_y = bbox
            tx1 = min_x * 0.1
            tx2 = max_x * 0.1
            ty1 = img_h - max_y * 0.1
            ty2 = img_h - min_y * 0.1
            all_points_trans.extend([(tx1, ty1), (tx2, ty2)])
            
    if not all_points_trans:
        print(f"No se encontraron caminos válidos para umbral {threshold}%.")
        return
        
    xs_trans = [p[0] for p in all_points_trans]
    ys_trans = [p[1] for p in all_points_trans]
    
    min_tx, max_tx = min(xs_trans), max(xs_trans)
    min_ty, max_ty = min(ys_trans), max(ys_trans)
    
    w_trans = max_tx - min_tx
    h_trans = max_ty - min_ty
    cx_trans = min_tx + w_trans / 2.0
    cy_trans = min_ty + h_trans / 2.0
    
    print(f"Cráneo original (umbral {threshold}%): ancho={w_trans:.2f}, alto={h_trans:.2f}, centro=({cx_trans:.2f}, {cy_trans:.2f})")
    
    # Escalar y centrar
    # Usamos 530px de ancho objetivo en el viewBox de 800x1000.
    target_w = 530.0
    s = target_w / w_trans
    
    target_cx = 400.0
    target_cy = 380.0
    
    final_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="100%" height="100%">
  <defs>
    <!-- Gradiente metálico dorado premium de alta definición -->
    <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f6ebd0" />
      <stop offset="20%" stop-color="#dfc593" />
      <stop offset="45%" stop-color="#a67e35" />
      <stop offset="55%" stop-color="#835c16" />
      <stop offset="80%" stop-color="#dfc593" />
      <stop offset="100%" stop-color="#a67e35" />
    </linearGradient>
    <filter id="subtle-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <!-- Fondo oscuro premium metalizado -->
  <rect width="100%" height="100%" fill="#131210"/>
  
  <!-- Resplandor sutil radial -->
  <radialGradient id="radial-glow" cx="50%" cy="40%" r="65%">
    <stop offset="0%" stop-color="#2a261f" stop-opacity="0.75" />
    <stop offset="100%" stop-color="#131210" stop-opacity="0" />
  </radialGradient>
  <rect width="100%" height="100%" fill="url(#radial-glow)" />

  <!-- Grupo del logotipo del cráneo centrado y escalado de forma perfecta -->
  <g transform="translate({target_cx}, {target_cy}) scale({s:.6f}) translate({-cx_trans:.6f}, {-cy_trans:.6f})" filter="url(#subtle-shadow)">
    <!-- Transformación de inversión de potrace sobre el lienzo de 1024 de alto -->
    <g transform="translate(0, 1024) scale(0.1, -0.1)" fill="url(#gold-gradient)" stroke="none">
"""
    
    for p in cleaned_paths:
        final_svg += f'      <path d="{p}" />\n'
        
    final_svg += """    </g>
  </g>

  <!-- Textos de marca perfectamente posicionados en la base -->
  <g id="brand-texts" fill="url(#gold-gradient)" filter="url(#subtle-shadow)">
    <!-- CRÁNEO NOBLE -->
    <text x="400" y="730" text-anchor="middle" 
          font-family="Georgia, serif" 
          font-size="44" font-weight="700" letter-spacing="14">CRÁNEO NOBLE</text>
    
    <!-- by ARCT -->
    <text x="400" y="790" text-anchor="middle" 
          font-family="Arial, sans-serif" 
          font-size="19" font-weight="300" letter-spacing="9" fill="#a09278">by ARCT</text>
          
    <!-- ARTE · RAÍZ · CARÁCTER · TRASCENDENCIA -->
    <text x="400" y="855" text-anchor="middle" 
          font-family="Arial, sans-serif" 
          font-size="11" font-weight="400" letter-spacing="7" fill="url(#gold-gradient)">ARTE • RAÍZ • CARÁCTER • TRASCENDENCIA</text>
  </g>
</svg>
"""
    
    output_path = f"logo-craneo-noble-v7-{threshold}.svg"
    with open(output_path, 'w') as f:
        f.write(final_svg)
        
    # Versión transparente
    transparent_svg = final_svg.replace('<rect width="100%" height="100%" fill="#131210"/>', '')
    transparent_svg = transparent_svg.replace('<rect width="100%" height="100%" fill="url(#radial-glow)" />', '')
    trans_output_path = f"logo-craneo-noble-v7-{threshold}-transparent.svg"
    with open(trans_output_path, 'w') as f:
        f.write(transparent_svg)
        
    print(f"Creado: {output_path} y {trans_output_path}")

def generate_preview_html():
    html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>V7 Vectorization Preview</title>
  <style>
    body { background: #131210; color: #e0e0e0; font-family: system-ui, sans-serif; margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center; }
    h1 { margin-bottom: 10px; font-weight: 300; color: #dfc593; }
    p { margin-top: 0; margin-bottom: 40px; color: #a09278; }
    .grid { display: flex; flex-direction: column; gap: 50px; width: 100%; max-width: 1200px; }
    .row { display: flex; gap: 30px; justify-content: center; width: 100%; }
    .card { background: #1a1916; border-radius: 12px; padding: 25px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); text-align: center; flex: 1; border: 1px solid #2a261f; }
    .card h3 { margin-top: 0; color: #dfc593; font-weight: 400; font-size: 1.2rem; margin-bottom: 20px; }
    img, object { width: 100%; height: 550px; border: 1px solid #2a261f; display: block; border-radius: 6px; background: #131210; object-fit: contain; }
    .original-img { object-fit: contain; background: #1c1b18; }
  </style>
</head>
<body>
  <h1>Cráneo Noble - Vectorización V7</h1>
  <p>Comparación con Corrección de Iluminación por Negación y División (Flat-Field)</p>
  
  <div class="grid">
    <!-- Fila Original -->
    <div class="row">
      <div class="card" style="max-width: 500px;">
        <h3>Diseño Original (Foto de Placa de Metal)</h3>
        <img class="original-img" src="original_design.jpg" />
      </div>
    </div>
    
    <!-- Fila Umbral 78% -->
    <div class="row">
      <div class="card">
        <h3>Binarizado (Umbral 78%)</h3>
        <img src="trace_temp/processed_v7_78.png" />
      </div>
      <div class="card">
        <h3>SVG Final (Umbral 78%)</h3>
        <object type="image/svg+xml" data="logo-craneo-noble-v7-78.svg"></object>
      </div>
    </div>

    <!-- Fila Umbral 80% -->
    <div class="row">
      <div class="card">
        <h3>Binarizado (Umbral 80%)</h3>
        <img src="trace_temp/processed_v7_80.png" />
      </div>
      <div class="card">
        <h3>SVG Final (Umbral 80%)</h3>
        <object type="image/svg+xml" data="logo-craneo-noble-v7-80.svg"></object>
      </div>
    </div>

    <!-- Fila Umbral 82% -->
    <div class="row">
      <div class="card">
        <h3>Binarizado (Umbral 82%)</h3>
        <img src="trace_temp/processed_v7_82.png" />
      </div>
      <div class="card">
        <h3>SVG Final (Umbral 82%)</h3>
        <object type="image/svg+xml" data="logo-craneo-noble-v7-82.svg"></object>
      </div>
    </div>
  </div>
</body>
</html>
"""
    with open("preview_v7.html", "w") as f:
        f.write(html_content)
    print("Creado: preview_v7.html")

if __name__ == "__main__":
    for th in [78, 80, 82]:
        process_vector(th, f"logo-craneo-noble-v7-{th}.svg")
    generate_preview_html()

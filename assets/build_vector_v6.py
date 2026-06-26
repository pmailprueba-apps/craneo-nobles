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
    
    bmp_path = f"trace_temp/processed_{threshold}.bmp"
    svg_temp_path = f"trace_temp/raw_{threshold}.svg"
    
    # ImageMagick: Procesar la imagen completa con el túnel ultra preciso (X=320 a X=350)
    # basado en el análisis de píxeles reales de la imagen.
    cmd_magick = [
        "magick", "original_design.jpg",
        "-colorspace", "gray",
        "-threshold", f"{threshold}%",
        "-fill", "black",
        "-draw", "rectangle 0,0 821,15",            # Eliminar borde superior
        "-draw", "rectangle 710,0 821,95",          # Tornillo superior derecho
        "-draw", "rectangle 0,0 80,80",             # Esquina superior izquierda
        "-draw", "rectangle 0,510 320,1024",        # Columna de texto izquierda (hasta X=320)
        "-draw", "rectangle 350,510 821,1024",      # Columna de texto derecha (desde X=350)
        "-draw", "rectangle 320,665 350,1024",      # Línea inferior bajo el hocico
        "-negate",
        bmp_path
    ]
    
    print(f"Ejecutando ImageMagick para umbral {threshold}% con túnel ultra preciso...")
    subprocess.run(cmd_magick, check=True)
    
    # Vectorizar con potrace
    subprocess.run(["potrace", "-s", "-o", svg_temp_path, bmp_path], check=True)
    
    # Leer SVG temporal y limpiar caminos de ruido
    with open(svg_temp_path, 'r') as f:
        content = f.read()
        
    paths = re.findall(r'<path[^>]*d="([^"]+)"[^>]*>', content)
    
    cleaned_paths = []
    for p in paths:
        if len(p) >= 80: # Ignorar ruido
            cleaned_paths.append(p)
            
    print(f"Caminos filtrados: {len(cleaned_paths)} de {len(paths)}")
    
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
        print("No se encontraron caminos válidos.")
        return
        
    xs_trans = [p[0] for p in all_points_trans]
    ys_trans = [p[1] for p in all_points_trans]
    
    min_tx, max_tx = min(xs_trans), max(xs_trans)
    min_ty, max_ty = min(ys_trans), max(ys_trans)
    
    w_trans = max_tx - min_tx
    h_trans = max_ty - min_ty
    cx_trans = min_tx + w_trans / 2.0
    cy_trans = min_ty + h_trans / 2.0
    
    print(f"Cráneo original: ancho={w_trans:.2f}, alto={h_trans:.2f}, centro=({cx_trans:.2f}, {cy_trans:.2f})")
    
    # Escalar y centrar
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
    
    output_path = f"../{output_name}"
    with open(output_path, 'w') as f:
        f.write(final_svg)
        
    # Versión transparente
    transparent_svg = final_svg.replace('<rect width="100%" height="100%" fill="#131210"/>', '')
    transparent_svg = transparent_svg.replace('<rect width="100%" height="100%" fill="url(#radial-glow)" />', '')
    trans_output_path = f"../{output_name.replace('.svg', '-transparent.svg')}"
    with open(trans_output_path, 'w') as f:
        f.write(transparent_svg)
        
    print(f"Creado: {output_path} y {trans_output_path}")

# Probamos umbrales de 48%, 50% y 52%
process_vector(48, "logo-craneo-noble-v5-48.svg")
process_vector(50, "logo-craneo-noble-v5-50.svg")
process_vector(52, "logo-craneo-noble-v5-52.svg")

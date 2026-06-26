import re
import os

def clean_and_normalize_svg(threshold, output_name):
    svg_path = f"trace_temp/skull_{threshold}.svg"
    if not os.path.exists(svg_path):
        print(f"File {svg_path} not found")
        return
    
    with open(svg_path, 'r') as f:
        content = f.read()
    
    # Extraer el viewBox
    viewbox_match = re.search(r'viewBox="([^"]+)"', content)
    if not viewbox_match:
        print("viewBox not found")
        return
    
    viewbox = [float(x) for x in viewbox_match.group(1).split()]
    vb_w, vb_h = viewbox[2], viewbox[3]
    
    # Extraer el transform del grupo principal si existe
    transform_match = re.search(r'<g[^>]*transform="([^"]+)"', content)
    transform = transform_match.group(1) if transform_match else ""
    
    # Encontrar todas las etiquetas <path>
    path_regex = r'<path[^>]*d="([^"]+)"[^>]*>'
    paths = re.findall(path_regex, content)
    
    print(f"Threshold {threshold}%: total paths found = {len(paths)}")
    
    # Filtrar caminos de ruido (caminos muy cortos, por ejemplo < 80 caracteres en la definición d)
    # y conservar los caminos principales que forman el cráneo y el monograma
    cleaned_paths = []
    noise_count = 0
    for p in paths:
        if len(p) < 80:
            noise_count += 1
            continue
        cleaned_paths.append(p)
    
    print(f"Threshold {threshold}%: removed {noise_count} noise paths, keeping {len(cleaned_paths)} main paths")
    
    # Crear el contenido SVG final
    # Usaremos un viewBox estándar de 800x1000 para que sea perfectamente escalable y centrado
    final_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="100%" height="100%">
  <defs>
    <!-- Gradiente metálico dorado premium -->
    <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f3e7c4" />
      <stop offset="25%" stop-color="#d8be8a" />
      <stop offset="50%" stop-color="#a6813c" />
      <stop offset="75%" stop-color="#d8be8a" />
      <stop offset="100%" stop-color="#8c6623" />
    </linearGradient>
    <filter id="subtle-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Fondo oscuro premium de metal cepillado simulado -->
  <rect width="100%" height="100%" fill="#131210"/>
  
  <!-- Círculos de fondo sutiles de diseño de metal cepillado radial -->
  <radialGradient id="radial-glow" cx="50%" cy="40%" r="60%">
    <stop offset="0%" stop-color="#2a2720" stop-opacity="0.6" />
    <stop offset="100%" stop-color="#131210" stop-opacity="0" />
  </radialGradient>
  <rect width="100%" height="100%" fill="url(#radial-glow)" />

  <!-- Grupo del logotipo del cráneo vectorizado -->
  <g transform="translate(400, 360) scale(0.72) translate(-410, -265)" filter="url(#subtle-shadow)">
    <!-- Aplicamos el transform original de potrace para escalar y posicionar correctamente los caminos -->
    <g transform="{transform}" fill="url(#gold-gradient)" stroke="none">
"""
    
    for p in cleaned_paths:
        final_svg += f'      <path d="{p}" />\n'
        
    final_svg += """    </g>
  </g>

  <!-- Textos de marca posicionados y formateados sutilmente con tipografías elegantes -->
  <g id="brand-texts" fill="url(#gold-gradient)" filter="url(#subtle-shadow)">
    <!-- CRÁNEO NOBLE -->
    <text x="400" y="700" text-anchor="middle" 
          font-family="Georgia, serif" 
          font-size="42" font-weight="700" letter-spacing="12">CRÁNEO NOBLE</text>
    
    <!-- by ARCT -->
    <text x="400" y="760" text-anchor="middle" 
          font-family="Arial, sans-serif" 
          font-size="18" font-weight="300" letter-spacing="8" fill="#a89a80">by ARCT</text>
          
    <!-- ARTE · RAÍZ · CARÁCTER · TRASCENDENCIA -->
    <text x="400" y="825" text-anchor="middle" 
          font-family="Arial, sans-serif" 
          font-size="11" font-weight="400" letter-spacing="6" fill="url(#gold-gradient)">ARTE • RAÍZ • CARÁCTER • TRASCENDENCIA</text>
  </g>
</svg>
"""
    
    output_path = f"../{output_name}"
    with open(output_path, 'w') as f:
        f.write(final_svg)
    
    # También creamos una versión con fondo transparente
    transparent_svg = final_svg.replace('<rect width="100%" height="100%" fill="#131210"/>', '')
    transparent_svg = transparent_svg.replace('<rect width="100%" height="100%" fill="url(#radial-glow)" />', '')
    
    trans_output_path = f"../{output_name.replace('.svg', '-transparent.svg')}"
    with open(trans_output_path, 'w') as f:
        f.write(transparent_svg)
        
    print(f"Created {output_path} and {trans_output_path}")

# Ejecutar para umbrales de 45%, 50% y 55%
clean_and_normalize_svg(45, "logo-craneo-noble-45.svg")
clean_and_normalize_svg(50, "logo-craneo-noble-50.svg")
clean_and_normalize_svg(55, "logo-craneo-noble-55.svg")

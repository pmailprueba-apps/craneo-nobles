import re

def main():
    # Read the base SVG (v7-80) to extract paths and transformation parameters
    base_svg_path = "logo-craneo-noble-v7-80.svg"
    with open(base_svg_path, 'r') as f:
        content = f.read()
        
    # Extract paths
    paths = re.findall(r'<path[^>]*d="([^"]+)"[^>]*>', content)
    
    # Extract transformation numbers from the translate/scale group
    # Look for: transform="translate(400.0, 380.0) scale(0.895422) translate(-331.550000, -358.650000)"
    trans_match = re.search(r'<g\s+transform="translate\(([^,]+),\s*([^)]+)\)\s+scale\(([^)]+)\)\s+translate\(([^,]+),\s*([^)]+)\)"', content)
    if trans_match:
        target_cx = float(trans_match.group(1))
        target_cy = float(trans_match.group(2))
        s = float(trans_match.group(3))
        cx_trans = -float(trans_match.group(4))
        cy_trans = -float(trans_match.group(5))
    else:
        # Fallback to standard
        target_cx = 400.0
        target_cy = 380.0
        s = 0.895422
        cx_trans = 331.55
        cy_trans = 358.65
        
    print(f"Loaded: {len(paths)} paths, scale={s}, center=({cx_trans}, {cy_trans})")
    
    # Generate the refined SVG with:
    # - Polished gold gradient with white high-shine highlight and deep shadows
    # - Concentric decorative circles centered at (400, 380)
    # - Deep multi-stage drop shadows
    refined_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="100%" height="100%">
  <defs>
    <!-- Gradiente metálico dorado pulido ultra premium de alta definición -->
    <linearGradient id="polished-gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" /> <!-- Brillo de luz directa -->
      <stop offset="12%" stop-color="#fcf6e8" />
      <stop offset="30%" stop-color="#e9d3a7" />
      <stop offset="48%" stop-color="#b69046" />
      <stop offset="60%" stop-color="#805b15" />
      <stop offset="78%" stop-color="#d8be8a" />
      <stop offset="90%" stop-color="#a6813c" />
      <stop offset="100%" stop-color="#5a3d05" /> <!-- Sombra de oclusión -->
    </linearGradient>
    
    <!-- Filtro de sombra profunda y rica -->
    <filter id="rich-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="11" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- Fondo oscuro premium metalizado -->
  <rect width="100%" height="100%" fill="#131210"/>
  
  <!-- Resplandor sutil radial -->
  <radialGradient id="radial-glow" cx="50%" cy="40%" r="65%">
    <stop offset="0%" stop-color="#2c2821" stop-opacity="0.8" />
    <stop offset="100%" stop-color="#131210" stop-opacity="0" />
  </radialGradient>
  <rect width="100%" height="100%" fill="url(#radial-glow)" />

  <!-- Elementos decorativos circulares de fondo (Emblema de Lujo) -->
  <g id="decorations" stroke="url(#polished-gold)" fill="none" opacity="0.3" filter="url(#rich-shadow)">
    <!-- Círculo interior continuo fino -->
    <circle cx="400" cy="380" r="290" stroke-width="1.2" />
    <!-- Círculo intermedio discontinuo (estilo brújula/astrolabio premium) -->
    <circle cx="400" cy="380" r="306" stroke-width="1.5" stroke-dasharray="12 8" />
    <!-- Círculo exterior extremadamente sutil -->
    <circle cx="400" cy="380" r="322" stroke-width="0.6" stroke-dasharray="2 4" opacity="0.6" />
  </g>

  <!-- Grupo del logotipo del cráneo centrado y escalado de forma perfecta -->
  <g transform="translate({target_cx}, {target_cy}) scale({s:.6f}) translate({-cx_trans:.6f}, {-cy_trans:.6f})" filter="url(#rich-shadow)">
    <!-- Transformación de inversión de potrace sobre el lienzo de 1024 de alto -->
    <g transform="translate(0, 1024) scale(0.1, -0.1)" fill="url(#polished-gold)" stroke="none">
"""
    
    for p in paths:
        refined_svg += f'      <path d="{p}" />\n'
        
    refined_svg += """    </g>
  </g>

  <!-- Textos de marca perfectamente posicionados en la base -->
  <g id="brand-texts" fill="url(#polished-gold)" filter="url(#rich-shadow)">
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
          font-size="11" font-weight="400" letter-spacing="7" fill="url(#polished-gold)">ARTE • RAÍZ • CARÁCTER • TRASCENDENCIA</text>
  </g>
</svg>
"""
    
    # Save files
    with open("logo-craneo-noble-refinado.svg", 'w') as f:
        f.write(refined_svg)
        
    # Save transparent version
    transparent_svg = refined_svg.replace('<rect width="100%" height="100%" fill="#131210"/>', '')
    transparent_svg = transparent_svg.replace('<rect width="100%" height="100%" fill="url(#radial-glow)" />', '')
    with open("logo-craneo-noble-refinado-transparent.svg", 'w') as f:
        f.write(transparent_svg)
        
    print("Refined SVGs generated successfully.")

if __name__ == "__main__":
    main()

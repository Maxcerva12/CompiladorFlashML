"""
Generador de código HTML a partir del AST de FlashML
"""
from Analizadores.parser import Elemento, NodoTexto, NodoComentario, Documento

class GeneradorHTML:

    
    def __init__(self):
        self.mapeo_etiquetas = {
            'velocista': 'div',
            'titulo': 'h1',
            'episodio': 'section',
            'temporada': 'article',  
            'escena': 'section',
            'personaje': 'figure',   
            'poder': 'span',
            'dialogo': 'p',
            'rapido': 'em',
            'accion': 'aside',       
            'imagen': 'img',
            'villanos': 'ul',
            'villano': 'li',
            
            'superspeed': 'span',
            'phasing': 'span',
            'cryokinesis': 'span',
            'vibration': 'span',
            'timetravel': 'span',
            'speedforce': 'span',
            'metahuman': 'span',
            'lugar': 'div',
            'equipo': 'div'
        }
        
        
        self.mapeo_atributos = {
            'nombre': 'data-nombre',
            'actor': 'data-actor',
            'velocidad': 'data-velocidad',
            'numero': 'data-temporada',
            'src': 'src',
            'alt': 'alt'
        }
    
    def generar(self, ast):
        """Genera código HTML a partir del AST """
        return f"""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documento FlashML</title>
        <style>
    {self._generar_estilos()}
        </style>
        <script>
            // Script para añadir interactividad
            document.addEventListener('DOMContentLoaded', function() {{
                // Animación para elementos Flash
                const flashElements = document.querySelectorAll('.superspeed, .speedforce');
                flashElements.forEach(el => {{
                    el.addEventListener('mouseover', function() {{
                        this.style.animation = 'lightning-flash 0.5s infinite';
                    }});
                    el.addEventListener('mouseout', function() {{
                        this.style.animation = '';
                    }});
                }});
                
                // Toggle para ver/ocultar episodios
                const temporadas = document.querySelectorAll('.temporada');
                temporadas.forEach(temporada => {{
                    const titulo = temporada.querySelector('h1, h2, h3') || temporada.firstElementChild;
                    if (titulo) {{
                        titulo.style.cursor = 'pointer';
                        titulo.addEventListener('click', function() {{
                            Array.from(temporada.children).forEach(child => {{
                                if (child !== titulo) {{
                                    child.style.display = child.style.display === 'none' ? '' : 'none';
                                }}
                            }});
                        }});
                    }}
                }});
                
                // Tooltip para personajes con sus nombres
                const personajes = document.querySelectorAll('.personaje[data-nombre]');
                personajes.forEach(personaje => {{
                    personaje.setAttribute('title', personaje.getAttribute('data-nombre'));
                }});
            }});
        </script>
    </head>
    <body>
        {self._generar_nodo(ast)}
    </body>
    </html>"""
    
    def _generar_estilos(self):
        
        return """
    /* Estilos modernos inspirados en The Flash */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    :root {
        --flash-red: #e63946;
        --flash-yellow: #fcbf49;
        --dark-bg: #1a1a2e;
        --dark-secondary: #16213e;
        --dark-accent: #242750;
        --light-text: #f8f9fa;
        --highlight: #f1c40f;
        --flash-blue: #4361ee;
        --flash-green: #2ecc71;
        --flash-purple: #9b59b6;
        --transition-speed: 0.3s;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: var(--dark-bg);
        color: var(--light-text);
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 0.8em;
        font-weight: 700;
    }
    
    h1 {
        color: var(--flash-red);
        border-bottom: 3px solid var(--flash-yellow);
        padding-bottom: 10px;
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
        text-shadow: 0 0 10px rgba(230, 57, 70, 0.3);
    }
    
    /* Contenedor principal */
    .velocista {
        border: none;
        padding: 25px;
        border-radius: 12px;
        background-color: var(--dark-accent);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
        transition: transform var(--transition-speed);
    }
    
    .velocista:hover {
        transform: translateY(-5px);
    }
    
    /* Temporadas y episodios */
    article.temporada {
        background-color: var(--dark-secondary);
        padding: 20px;
        margin: 20px 0;
        border-radius: 12px;
        border-left: 8px solid var(--flash-yellow);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        transition: all var(--transition-speed);
    }
    
    article.temporada:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transform: translateY(-3px);
    }
    
    section.episodio {
        margin-top: 25px;
        padding: 18px;
        border-radius: 8px;
        background-color: var(--dark-accent);
        border-left: 5px solid var(--flash-yellow);
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    }
    
    section.escena {
        margin: 20px 0;
        padding: 15px;
        background-color: var(--dark-secondary);
        border-radius: 8px;
        border-left: 5px solid var(--flash-red);
        position: relative;
    }
    
    section.escena:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to right, rgba(230, 57, 70, 0.05), transparent);
        border-radius: 8px;
        pointer-events: none;
    }
    
    /* Personajes y diálogos */
    figure.personaje {
        padding: 15px;
        margin: 15px 0;
        background-color: var(--dark-secondary);
        border: none;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        transition: all var(--transition-speed);
    }
    
    figure.personaje:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
    }
    
    figure.personaje:after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 8px;
        height: 100%;
        background: var(--flash-yellow);
        opacity: 0.7;
    }
    
    .poder {
        color: var(--flash-red);
        font-weight: bold;
        padding: 3px 6px;
        border-radius: 4px;
        background-color: rgba(230, 57, 70, 0.1);
        display: inline-block;
        margin: 2px;
    }
    
    p.dialogo {
        padding: 15px;
        margin: 12px 0;
        background-color: var(--dark-accent);
        border-radius: 10px;
        position: relative;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
    }
    
    p.dialogo:before {
        content: '❝';
        position: absolute;
        left: 8px;
        top: 0;
        color: var(--flash-yellow);
        font-size: 1.5em;
        opacity: 0.5;
    }
    
    em.rapido {
        color: var(--flash-yellow);
        font-style: italic;
        text-shadow: 0 0 3px rgba(252, 191, 73, 0.5);
        font-weight: 500;
    }
    
    /* Acciones y elementos especiales */
    aside.accion {
        color: var(--light-text);
        padding: 12px 15px;
        margin: 15px 0;
        background-color: var(--dark-secondary);
        border-left: 5px solid var(--flash-blue);
        border-radius: 8px;
        position: relative;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    }
    
    aside.accion:before {
        content: '⚡';
        position: absolute;
        right: 15px;
        top: 10px;
        color: var(--flash-blue);
        opacity: 0.5;
        font-size: 1.2em;
    }
    
    /* Villanos */
    ul.villanos {
        padding-left: 0;
        list-style-type: none;
    }
    
    li.villano {
        padding: 12px 15px;
        margin: 10px 0;
        background: linear-gradient(to right, #330000, #3a0000);
        color: #fff;
        border-radius: 8px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
        transition: all var(--transition-speed);
        position: relative;
        padding-left: 30px;
    }
    
    li.villano:before {
        content: '⚠';
        color: var(--flash-yellow);
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
    }
    
    li.villano:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
    }
    
    /* Imágenes */
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 15px auto;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        transition: transform var(--transition-speed);
    }
    
    img:hover {
        transform: scale(1.02);
    }
    
    /* Estilos para poderes específicos */
    .superspeed {
        color: var(--flash-yellow);
        font-style: italic;
        text-shadow: 0 0 5px rgba(252, 191, 73, 0.5);
        font-weight: 500;
        background: linear-gradient(to right, transparent, rgba(252, 191, 73, 0.1), transparent);
        padding: 0 5px;
    }
    
    .phasing {
        color: var(--flash-blue);
        text-shadow: 0 0 8px rgba(67, 97, 238, 0.7);
        opacity: 0.8;
        transition: opacity var(--transition-speed);
    }
    
    .phasing:hover {
        opacity: 1;
    }
    
    .cryokinesis {
        color: var(--flash-green);
        font-weight: bold;
        background: linear-gradient(to right, rgba(46, 204, 113, 0.1), transparent);
        padding: 0 5px;
        border-radius: 3px;
    }
    
    .vibration {
        color: #e91e63;
        animation: vibrate 0.3s infinite;
        display: inline-block;
    }
    
    @keyframes vibrate {
        0% { transform: translateX(0); }
        25% { transform: translateX(1px); }
        50% { transform: translateX(-1px); }
        75% { transform: translateX(1px); }
        100% { transform: translateX(0); }
    }
    
    .timetravel {
        color: var(--flash-purple);
        text-decoration: none;
        background: linear-gradient(to right, transparent, rgba(155, 89, 182, 0.2), transparent);
        padding: 0 5px;
        position: relative;
    }
    
    .timetravel:after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 1px;
        background: linear-gradient(to right, transparent, var(--flash-purple), transparent);
    }
    
    .speedforce {
        color: var(--flash-yellow);
        font-weight: bold;
        background: linear-gradient(90deg, rgba(252,191,73,0.1) 0%, rgba(252,191,73,0.2) 50%, rgba(252,191,73,0.1) 100%);
        padding: 3px 8px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(252, 191, 73, 0.3);
    }
    
    .metahuman {
        color: var(--highlight);
        font-style: italic;
        padding: 2px 5px;
        border-radius: 3px;
        background-color: rgba(241, 196, 15, 0.1);
    }
    
    /* Lugares y equipos */
    .lugar {
        background-color: var(--dark-secondary);
        padding: 15px;
        margin: 15px 0;
        border-left: 5px solid var(--flash-red);
        border-radius: 8px;
        position: relative;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    }
    
    .lugar:before {
        content: '📍';
        position: absolute;
        right: 15px;
        top: 10px;
        opacity: 0.6;
    }
    
    .equipo {
        padding: 15px;
        margin: 15px 0;
        background-color: var(--dark-accent);
        border-radius: 8px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        border-top: 3px solid var(--flash-yellow);
        position: relative;
    }
    
    .equipo:before {
        content: '👥';
        position: absolute;
        right: 15px;
        top: 10px;
        opacity: 0.6;
    }
    
    /* Animaciones para elementos interactivos */
    @keyframes lightning-flash {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 1; }
    }
    
    /* Elementos interactivos adicionales */
    [data-actor]:hover:after {
        content: 'Actor: ' attr(data-actor);
        position: absolute;
        top: -30px;
        left: 50%;
        transform: translateX(-50%);
        background-color: var(--dark-bg);
        color: var(--light-text);
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.8em;
        z-index: 10;
        white-space: nowrap;
    }
    
    [data-velocidad]:hover:after {
        content: 'Velocidad: ' attr(data-velocidad);
        position: absolute;
        top: -30px;
        left: 50%;
        transform: translateX(-50%);
        background-color: var(--dark-bg);
        color: var(--flash-yellow);
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.8em;
        z-index: 10;
        white-space: nowrap;
    }
    
    /* Diseño responsivo */
    @media (max-width: 768px) {
        body {
            padding: 15px;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        .velocista {
            padding: 15px;
        }
        
        article.temporada, section.episodio, section.escena, figure.personaje {
            padding: 12px;
            margin: 12px 0;
        }
    }
    
    @media (max-width: 480px) {
        h1 {
            font-size: 1.8rem;
        }
        
        .velocista {
            padding: 10px;
        }
        
        article.temporada, section.episodio, section.escena, figure.personaje {
            padding: 10px;
            margin: 10px 0;
        }
    }
    """
    
    def _generar_nodo(self, nodo, indentacion=0):
        """Genera el código HTML para un nodo y sus hijos"""
        html = ""
        cadena_indentacion = "  " * indentacion
        
        if isinstance(nodo, Documento):
            for hijo in nodo.hijos:
                html += self._generar_nodo(hijo, indentacion)
        
        elif isinstance(nodo, Elemento):
            
            etiqueta_html = self.mapeo_etiquetas.get(nodo.nombre_etiqueta, 'div')
            
            
            atributos = ""
            for nombre, valor in nodo.atributos.items():
                atributo_html = self.mapeo_atributos.get(nombre, nombre)
                atributos += f" {atributo_html}=\"{valor}\""
            
            
            atributos += f" class=\"{nodo.nombre_etiqueta}\""
            
            
            if etiqueta_html == 'img':
                html += f"{cadena_indentacion}<{etiqueta_html}{atributos} />\n"
            else:
                # Abrir la etiqueta
                html += f"{cadena_indentacion}<{etiqueta_html}{atributos}>"
                
                # Si hay contenido en línea, no agregar nueva línea
                tiene_solo_texto = len(nodo.hijos) == 1 and isinstance(nodo.hijos[0], NodoTexto)
                if not tiene_solo_texto and nodo.hijos:
                    html += "\n"
                
                # Generar los hijos
                for hijo in nodo.hijos:
                    html += self._generar_nodo(hijo, indentacion + 1 if not tiene_solo_texto else 0)
                
                # Cerrar la etiqueta
                if not tiene_solo_texto and nodo.hijos:
                    html += cadena_indentacion
                html += f"</{etiqueta_html}>\n"
        
        elif isinstance(nodo, NodoTexto):
            # Usar el contenido del texto directamente
            html += nodo.texto
        
        elif isinstance(nodo, NodoComentario):
            # Convertir comentarios de FlashML a comentarios HTML
            html += f"{cadena_indentacion}<!-- {nodo.texto} -->\n"
        
        return html
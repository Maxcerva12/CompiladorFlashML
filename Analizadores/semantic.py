"""
Analizador semántico para FlashML
"""
from Analizadores.parser import Elemento, NodoTexto, NodoComentario, Documento

class AnalizadorSemantico:
    """
    Realiza el análisis semántico del AST para encontrar errores y validar la estructura
    """
    
    def __init__(self):
        self.etiquetas_permitidas = {
            'velocista': {'permitido_en': None, 'requerido': [], 'opcional': ['titulo', 'episodio', 'escena', 'personaje', 'poder', 'imagen', 'villanos', 'lugar', 'equipo']},
            'titulo': {'permitido_en': ['velocista', 'episodio'], 'requerido': [], 'opcional': []},
            'episodio': {'permitido_en': ['velocista', 'temporada'], 'requerido': [], 'opcional': ['titulo', 'escena', 'personaje', 'poder', 'imagen', 'villanos', 'lugar', 'equipo']},
            'temporada': {'permitido_en': ['velocista'], 'requerido': ['numero'], 'opcional': ['episodio', 'titulo']},
            'escena': {'permitido_en': ['velocista', 'episodio'], 'requerido': [], 'opcional': ['personaje', 'dialogo', 'accion', 'poder', 'superspeed', 'phasing', 'cryokinesis', 'vibration', 'timetravel', 'speedforce', 'metahuman']},
            'personaje': {'permitido_en': ['velocista', 'episodio', 'escena', 'lugar', 'equipo'], 'requerido': ['nombre'], 'opcional': ['actor', 'poder']},  # Added lugar, equipo
            'poder': {'permitido_en': ['velocista', 'episodio', 'escena', 'personaje'], 'requerido': [], 'opcional': []},
            'dialogo': {'permitido_en': ['escena', 'personaje'], 'requerido': [], 'opcional': ['rapido', 'superspeed', 'phasing', 'cryokinesis', 'vibration', 'timetravel', 'speedforce', 'metahuman']},
            'rapido': {'permitido_en': ['dialogo'], 'requerido': [], 'opcional': []},
            'accion': {'permitido_en': ['escena', 'personaje'], 'requerido': [], 'opcional': ['velocidad', 'superspeed', 'phasing', 'cryokinesis', 'vibration', 'timetravel', 'speedforce', 'metahuman']},  # Added power tags
            'imagen': {'permitido_en': ['velocista', 'episodio', 'personaje'], 'requerido': ['src'], 'opcional': ['alt']},
            'villanos': {'permitido_en': ['velocista', 'episodio'], 'requerido': [], 'opcional': ['villano']},
            'villano': {'permitido_en': ['villanos'], 'requerido': ['nombre'], 'opcional': ['poder']},
            'superspeed': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []}, 
            'phasing': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []},     
            'cryokinesis': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []}, 
            'vibration': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []},   
            'timetravel': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []},  
            'speedforce': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []},  
            'metahuman': {'permitido_en': ['dialogo', 'escena', 'personaje', 'accion'], 'requerido': [], 'opcional': []},   
            'lugar': {'permitido_en': ['velocista', 'episodio', 'escena'], 'requerido': ['nombre'], 'opcional': ['personaje']},  
            'equipo': {'permitido_en': ['velocista', 'episodio', 'escena'], 'requerido': ['nombre'], 'opcional': ['personaje']}   
        }
        
        self.errores = []
    
    def analizar(self, ast):
        
        self.errores = []
        self._analizar_nodo(ast, None)
        return self.errores
    
    def _analizar_nodo(self, nodo, etiqueta_padre):
        """Analiza un nodo y sus hijos recursivamente"""
        if isinstance(nodo, Documento):
            
            tiene_velocista = False
            for hijo in nodo.hijos:
                if isinstance(hijo, Elemento) and hijo.nombre_etiqueta == 'velocista':
                    tiene_velocista = True
                    break
            
            if not tiene_velocista:
                self.errores.append("Error semántico: se requiere un elemento raíz 'velocista'")
            
            
            for hijo in nodo.hijos:
                self._analizar_nodo(hijo, None)
        
        elif isinstance(nodo, Elemento):
            # Verificar que la etiqueta sea válida
            if nodo.nombre_etiqueta not in self.etiquetas_permitidas:
                self.errores.append(f"Error semántico: etiqueta desconocida '{nodo.nombre_etiqueta}'")
                return
            
            # Verificar que la etiqueta sea permitida en el contexto actual
            info_etiqueta = self.etiquetas_permitidas[nodo.nombre_etiqueta]
            if etiqueta_padre and info_etiqueta['permitido_en'] and etiqueta_padre not in info_etiqueta['permitido_en']:
                self.errores.append(f"Error semántico: '{nodo.nombre_etiqueta}' no está permitido dentro de '{etiqueta_padre}'")
            
            # Verificar atributos requeridos
            for atributo_requerido in info_etiqueta['requerido']:
                if atributo_requerido not in nodo.atributos:
                    self.errores.append(f"Error semántico: el atributo '{atributo_requerido}' es requerido en '{nodo.nombre_etiqueta}'")
            
            # Verificar atributos no permitidos
            atributos_validos = info_etiqueta['requerido'] + info_etiqueta['opcional']
            for atributo in nodo.atributos:
                if atributo not in atributos_validos:
                    self.errores.append(f"Error semántico: el atributo '{atributo}' no está permitido en '{nodo.nombre_etiqueta}'")
            
            
            for hijo in nodo.hijos:
                self._analizar_nodo(hijo, nodo.nombre_etiqueta)
        
        elif isinstance(nodo, NodoTexto) or isinstance(nodo, NodoComentario):
            pass
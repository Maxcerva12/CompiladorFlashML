"""
Generador de código intermedio para FlashML
"""
from Analizadores.parser import Documento, Elemento, NodoTexto, NodoComentario

class GeneradorIntermedio:
    """
    Convierte el AST de FlashML en una representación intermedia en formato JSON
    """
    
    def generar_json(self, ast):
        
        return self._nodo_a_json(ast)
    
    def _nodo_a_json(self, nodo):
        
        if isinstance(nodo, Documento):
            return {
                "tipo": "documento",
                "hijos": [self._nodo_a_json(hijo) for hijo in nodo.hijos]
            }
        elif isinstance(nodo, Elemento):
            return {
                "tipo": "elemento",
                "etiqueta": nodo.nombre_etiqueta,
                "atributos": nodo.atributos,
                "hijos": [self._nodo_a_json(hijo) for hijo in nodo.hijos]
            }
        elif isinstance(nodo, NodoTexto):
            return {
                "tipo": "texto",
                "contenido": nodo.texto.strip() if nodo.texto.strip() else ""
            }
        elif isinstance(nodo, NodoComentario):
            return {
                "tipo": "comentario",
                "contenido": nodo.texto
            }
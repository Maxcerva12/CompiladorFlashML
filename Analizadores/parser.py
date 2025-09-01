"""
Analizador sintáctico y constructor del AST para FlashML
"""
from Analizadores.lexer import TipoToken

class NodoAST:
    """Clase base para los nodos del AST"""
    def __init__(self):
        pass
    
    def __str__(self):
        return self.__class__.__name__

class Documento(NodoAST):
    def __init__(self):
        super().__init__()
        self.hijos = []
    
    def __str__(self):
        return f"Documento({len(self.hijos)} hijos)"

class Elemento(NodoAST):
    def __init__(self, nombre_etiqueta):
        super().__init__()
        self.nombre_etiqueta = nombre_etiqueta
        self.atributos = {}
        self.hijos = []
    
    def __str__(self):
        attrs = ", ".join([f"{k}='{v}'" for k, v in self.atributos.items()])
        return f"Elemento({self.nombre_etiqueta}, atributos=[{attrs}], {len(self.hijos)} hijos)"

class NodoTexto(NodoAST):
    def __init__(self, texto):
        super().__init__()
        self.texto = texto
    
    def __str__(self):
        if len(self.texto) > 20:
            return f"NodoTexto('{self.texto[:17]}...')"
        return f"NodoTexto('{self.texto}')"

class NodoComentario(NodoAST):
    def __init__(self, texto):
        super().__init__()
        self.texto = texto
    
    def __str__(self):
        if len(self.texto) > 20:
            return f"NodoComentario('{self.texto[:17]}...')"
        return f"NodoComentario('{self.texto}')"

class AnalizadorSintactico:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice_token_actual = 0
        self.token_actual = self.tokens[0] if tokens else None
    
    def avanzar(self):
        self.indice_token_actual += 1
        if self.indice_token_actual < len(self.tokens):
            self.token_actual = self.tokens[self.indice_token_actual]
        else:
            self.token_actual = None
    
    def consumir(self, tipo_token):
        if self.token_actual and self.token_actual.tipo == tipo_token:
            token = self.token_actual
            self.avanzar()
            return token
        else:
            esperado = tipo_token.name if self.token_actual else "ninguno"
            actual = self.token_actual.tipo.name if self.token_actual else "FIN_ARCHIVO"
            raise SyntaxError(f"Error de sintaxis: se esperaba {esperado}, se encontró {actual} en la posición {self.token_actual.posicion if self.token_actual else 'desconocida'}")
    
    def analizar(self):
        documento = Documento()
        
        while self.token_actual and self.token_actual.tipo != TipoToken.FIN_ARCHIVO:
            nodo = self.analizar_nodo()
            if nodo:
                documento.hijos.append(nodo)
        
        return documento
    
    def analizar_nodo(self):
        
        if self.token_actual.tipo == TipoToken.ETIQUETA_APERTURA:
            return self.analizar_elemento()
        elif self.token_actual.tipo == TipoToken.TEXTO:
            token = self.consumir(TipoToken.TEXTO)
            return NodoTexto(token.valor)
        elif self.token_actual.tipo == TipoToken.COMENTARIO:
            token = self.consumir(TipoToken.COMENTARIO)
            return NodoComentario(token.valor)
        else:
            raise SyntaxError(f"Token inesperado: {self.token_actual}")
    
    def analizar_elemento(self):
        
        token = self.consumir(TipoToken.ETIQUETA_APERTURA)
        elemento = Elemento(token.valor)
        
        # Analizar atributos si hay alguno
        while self.token_actual and self.token_actual.tipo == TipoToken.NOMBRE_ATRIBUTO:
            nombre_atributo = self.consumir(TipoToken.NOMBRE_ATRIBUTO).valor
            valor_atributo = self.consumir(TipoToken.VALOR_ATRIBUTO).valor
            elemento.atributos[nombre_atributo] = valor_atributo
        
        # Analizar contenido del elemento hasta encontrar la etiqueta de cierre
        while self.token_actual and not (self.token_actual.tipo == TipoToken.ETIQUETA_CIERRE and self.token_actual.valor == elemento.nombre_etiqueta):
            if self.token_actual.tipo == TipoToken.FIN_ARCHIVO:
                raise SyntaxError(f"Etiqueta de cierre faltante para {elemento.nombre_etiqueta}")
            
            nodo = self.analizar_nodo()
            if nodo:
                elemento.hijos.append(nodo)
        
        
        self.consumir(TipoToken.ETIQUETA_CIERRE)
        
        return elemento

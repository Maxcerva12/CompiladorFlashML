"""
Analizador léxico para FlashML - un lenguaje de marcado basado en la serie The Flash
"""
import re
from enum import Enum, auto

class TipoToken(Enum):
    """Tipos de tokens en FlashML"""
    ETIQUETA_APERTURA = auto()   
    ETIQUETA_CIERRE = auto()       
    NOMBRE_ATRIBUTO = auto()       
    VALOR_ATRIBUTO = auto()        
    TEXTO = auto()                 
    COMENTARIO = auto()           
    FIN_ARCHIVO = auto()           

class Token:
    """Clase para representar un token"""
    def __init__(self, tipo_token, valor, posicion):
        self.tipo = tipo_token
        self.valor = valor
        self.posicion = posicion
    
    def __str__(self):
        return f"Token({self.tipo}, '{self.valor}', pos={self.posicion})"
    
    def __repr__(self):
        return self.__str__()

class SyntaxError(Exception):
    pass

class AnalizadorLexico:
    
    def __init__(self, codigo_fuente):
        self.fuente = codigo_fuente
        self.posicion = 0
        self.caracter_actual = self.fuente[0] if self.fuente else None
        self.linea = 1
        self.columna = 1
    
    def avanzar(self):
        if self.caracter_actual == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
            
        self.posicion += 1
        if self.posicion < len(self.fuente):
            self.caracter_actual = self.fuente[self.posicion]
        else:
            self.caracter_actual = None
    
    def mirar_adelante(self, adelante=1):
        posicion_mirada = self.posicion + adelante
        if posicion_mirada < len(self.fuente):
            return self.fuente[posicion_mirada]
        return None
    
    def saltar_espacios(self):
        while self.caracter_actual and self.caracter_actual.isspace():
            self.avanzar()
    
    def leer_etiqueta(self):
        """Lee una etiqueta después de encontrar @"""
        es_cierre = False
        self.avanzar()  # Consumir @
        
        if self.caracter_actual == '/':
            es_cierre = True
            self.avanzar()  # Consumir /
        
        nombre_etiqueta = ''
        while self.caracter_actual and self.caracter_actual.isalnum() or self.caracter_actual == '_':
            nombre_etiqueta += self.caracter_actual
            self.avanzar()
        
        tipo_token = TipoToken.ETIQUETA_CIERRE if es_cierre else TipoToken.ETIQUETA_APERTURA
        return Token(tipo_token, nombre_etiqueta, (self.linea, self.columna - len(nombre_etiqueta) - (2 if es_cierre else 1)))
    
    def leer_nombre_atributo(self):
        nombre_atributo = ''
        posicion_inicio = (self.linea, self.columna)
        
        while self.caracter_actual and (self.caracter_actual.isalnum() or self.caracter_actual == '_'):
            nombre_atributo += self.caracter_actual
            self.avanzar()
        
        if self.caracter_actual == '=':
            self.avanzar() 
            return Token(TipoToken.NOMBRE_ATRIBUTO, nombre_atributo, posicion_inicio)
        
        # Si no hay un =, entonces no es un atributo, retrocedemos
        return None
    
    def leer_valor_atributo(self):
        
        caracter_comilla = self.caracter_actual 
        self.avanzar()
        posicion_inicio = (self.linea, self.columna)
        
        valor = ''
        while self.caracter_actual and self.caracter_actual != caracter_comilla:
            valor += self.caracter_actual
            self.avanzar()
        
        if self.caracter_actual == caracter_comilla:
            self.avanzar()  
            return Token(TipoToken.VALOR_ATRIBUTO, valor, posicion_inicio)
        
        raise SyntaxError(f"Comilla de cierre no encontrada en la posición {self.linea}:{self.columna}")
    
    def leer_comentario(self):
        
        self.avanzar()  
        self.avanzar()  
        posicion_inicio = (self.linea, self.columna)
        
        comentario = ''
        while self.caracter_actual:
            if self.caracter_actual == '#' and self.mirar_adelante() == '#':
                self.avanzar()  
                self.avanzar()  
                return Token(TipoToken.COMENTARIO, comentario, posicion_inicio)
            
            comentario += self.caracter_actual
            self.avanzar()
        
        raise SyntaxError(f"Cierre de comentario ## no encontrado en la posición {self.linea}:{self.columna}")
    
    def leer_texto(self):
        
        texto = ''
        posicion_inicio = (self.linea, self.columna)
        
        while self.caracter_actual:
            if self.caracter_actual == '@':
                break
            if self.caracter_actual == '#' and self.mirar_adelante() == '#':
                break
                
            texto += self.caracter_actual
            self.avanzar()
        
        return Token(TipoToken.TEXTO, texto, posicion_inicio)
    
    def obtener_siguiente_token(self):
        """Obtiene el siguiente token del código fuente"""
        while self.caracter_actual:
            
            if self.caracter_actual.isspace():
                self.saltar_espacios()
                continue
            
            # Identificar diferentes tokens
            if self.caracter_actual == '@':
                return self.leer_etiqueta()
            
            if self.caracter_actual == '#' and self.mirar_adelante() == '#':
                return self.leer_comentario()
            
            if self.caracter_actual.isalpha() or self.caracter_actual == '_':
                token_nombre_atributo = self.leer_nombre_atributo()
                if token_nombre_atributo:
                    return token_nombre_atributo
            
            if self.caracter_actual == '"' or self.caracter_actual == "'":
                return self.leer_valor_atributo()
            
            # Si no es ninguno de los anteriores, es texto normal
            return self.leer_texto()
        
        # Si llegamos al final del código fuente
        return Token(TipoToken.FIN_ARCHIVO, "", (self.linea, self.columna))
    
    def tokenizar(self):
        """Convierte todo el código fuente en una lista de tokens"""
        tokens = []
        token = self.obtener_siguiente_token()
        
        while token.tipo != TipoToken.FIN_ARCHIVO:
            tokens.append(token)
            token = self.obtener_siguiente_token()
        
        tokens.append(token) 
        return tokens

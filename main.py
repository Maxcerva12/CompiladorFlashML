
import argparse
import os
import json
import logging
from Analizadores.lexer import AnalizadorLexico, SyntaxError as LexerSyntaxError
from Analizadores.parser import AnalizadorSintactico
from Analizadores.semantic import AnalizadorSemantico
from Analizadores.generator import GeneradorHTML
from Analizadores.intermedio import GeneradorIntermedio

# Configurar el logger
logging.basicConfig(
    filename='compilador_flashml.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def compilar_codigo(codigo_fuente, archivo_entrada="entrada.flashml", archivo_salida=None):
    """
    Compila un código FlashML a HTML, generando un código intermedio en JSON
    
    Args:
        codigo_fuente: Código FlashML como string
        archivo_entrada: Nombre del archivo de entrada (para logs y nombres de salida)
        archivo_salida: Ruta al archivo HTML de salida (opcional)
    
    Returns:
        dict: Resultado con 'html' (código HTML), 'intermedio' (ruta JSON), 'errores' (lista de errores)
    """
    if not archivo_salida:
        nombre_base = os.path.splitext(archivo_entrada)[0]
        archivo_salida = f"{nombre_base}.html"
        archivo_intermedio = f"{nombre_base}.json"
    else:
        nombre_base = os.path.splitext(archivo_salida)[0]
        archivo_intermedio = f"{nombre_base}.json"
    
    logging.info(f"Iniciando compilación del archivo/código: {archivo_entrada}")
    resultado = {'html': None, 'intermedio': None, 'errores': []}
    
    try:
        print(f"Compilando {archivo_entrada}...")
        print("1. Análisis léxico...")
        
        # Fase 1: Análisis léxico (tokenización)
        analizador_lexico = AnalizadorLexico(codigo_fuente)
        try:
            tokens = analizador_lexico.tokenizar()
        except LexerSyntaxError as e:
            error_msg = f"Error léxico: {str(e)}"
            resultado['errores'].append({'tipo': 'léxico', 'mensaje': error_msg})
            logging.error(error_msg)
            return resultado
        
        print(f"   Se encontraron {len(tokens)} tokens.")
        print("2. Análisis sintáctico...")
        logging.info(f"Análisis léxico completado. {len(tokens)} tokens encontrados.")
        
        # Fase 2: Análisis sintáctico (parsing)
        analizador_sintactico = AnalizadorSintactico(tokens)
        try:
            arbol_sintactico = analizador_sintactico.analizar()
        except SyntaxError as e:
            error_msg = f"Error sintáctico: {str(e)}"
            resultado['errores'].append({'tipo': 'sintáctico', 'mensaje': error_msg})
            logging.error(error_msg)
            return resultado
        
        print("   Árbol de sintaxis abstracta (AST) construido correctamente.")
        print("3. Análisis semántico...")
        logging.info("Análisis sintáctico completado. AST construido.")
        
        # Fase 3: Análisis semántico (validación)
        analizador_semantico = AnalizadorSemantico()
        errores_semanticos = analizador_semantico.analizar(arbol_sintactico)
        
        if errores_semanticos:
            print("   Se encontraron errores semánticos:")
            for error in errores_semanticos:
                print(f"   - {error}")
                resultado['errores'].append({'tipo': 'semántico', 'mensaje': error})
                logging.error(f"Error semántico: {error}")
            return resultado
        
        print("   No se encontraron errores semánticos.")
        print("4. Generación de código intermedio...")
        logging.info("Análisis semántico completado sin errores.")
        
        # Fase 4: Generación de código intermedio (JSON)
        generador_intermedio = GeneradorIntermedio()
        codigo_intermedio = generador_intermedio.generar_json(arbol_sintactico)
        with open(archivo_intermedio, 'w', encoding='utf-8') as f:
            json.dump(codigo_intermedio, f, ensure_ascii=False, indent=2)
        
        resultado['intermedio'] = archivo_intermedio
        print(f"   Código intermedio guardado en {archivo_intermedio}")
        print("5. Generación de código HTML...")
        logging.info(f"Código intermedio generado y guardado en {archivo_intermedio}")
        
        # Fase 5: Generación de código HTML
        generador_html = GeneradorHTML()
        codigo_html = generador_html.generar(arbol_sintactico)
        
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(codigo_html)
        
        resultado['html'] = codigo_html
        print(f"Compilación completada. Resultado guardado en {archivo_salida}")
        logging.info(f"Compilación completada. HTML guardado en {archivo_salida}")
        return resultado
    
    except Exception as e:
        error_msg = f"Error general durante la compilación: {str(e)}"
        resultado['errores'].append({'tipo': 'general', 'mensaje': error_msg})
        print(error_msg)
        logging.error(error_msg)
        return resultado

def compilar_archivo(archivo_entrada, archivo_salida=None):
    """
    Compila un archivo FlashML a HTML
    
    Args:
        archivo_entrada: Ruta al archivo FlashML de entrada
        archivo_salida: Ruta al archivo HTML de salida (opcional)
    """
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            codigo_fuente = f.read()
        return compilar_codigo(codigo_fuente, archivo_entrada, archivo_salida)
    except Exception as e:
        error_msg = f"Error al leer el archivo {archivo_entrada}: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        return {'html': None, 'intermedio': None, 'errores': [{'tipo': 'general', 'mensaje': error_msg}]}

def principal():
    """Función principal del programa"""
    parser = argparse.ArgumentParser(description='Compilador FlashML a HTML')
    parser.add_argument('entrada', help='Archivo FlashML de entrada')
    parser.add_argument('-s', '--salida', help='Archivo HTML de salida (opcional)')
    
    argumentos = parser.parse_args()
    compilar_archivo(argumentos.entrada, argumentos.salida)

if __name__ == "__main__":
    principal()
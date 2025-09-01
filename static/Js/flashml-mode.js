/**
 * Modo CodeMirror personalizado para el lenguaje FlashML
 */
CodeMirror.defineMode("flashml", function() {
    return {
        startState: function() {
            return { inTag: false, inComment: false };
        },
        token: function(stream, state) {
            // Ignorar espacios en blanco
            if (stream.eatSpace()) {
                return null;
            }

            // Manejar comentarios (##texto##)
            if (stream.match(/^##/, true)) {
                state.inComment = true;
                return "comment";
            }
            if (state.inComment) {
                if (stream.match(/^##/, true)) {
                    state.inComment = false;
                    return "comment";
                }
                stream.next();
                return "comment";
            }

            // Manejar etiquetas de apertura (@nombre)
            if (stream.match(/^@[\w_]+/, true)) {
                state.inTag = true;
                return "keyword";
            }

            // Manejar etiquetas de cierre (@/nombre)
            if (stream.match(/^@\/[\w_]+/, true)) {
                state.inTag = false;
                return "keyword";
            }

            // Manejar nombres de atributos (nombre=)
            if (state.inTag && stream.match(/^[\w_]+=/, true)) {
                return "attribute";
            }

            // Manejar valores de atributos ("valor" o 'valor')
            if (state.inTag && (stream.match(/^"[^"]*"/, true) || stream.match(/^'[^']*'/, true))) {
                return "string";
            }

            // Texto plano
            stream.next();
            return "text";
        }
    };
});

// Estilo para los tokens
CodeMirror.defineMIME("text/x-flashml", "flashml");
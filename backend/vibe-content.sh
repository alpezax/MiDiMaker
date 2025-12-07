#!/bin/bash

# Uso: ./vibe-content.sh [directorio] [exclusiones...]
# Ejemplo: ./vibe-content.sh . ".git" "__pycache__" ".env" ".mid"

DIR="${1:-.}"        # Directorio base, por defecto el actual
shift
EXCLUDES=("$@")      # Lista de exclusiones

# Función para comprobar si un fichero/directorio está en la lista de exclusión
is_excluded() {
    local name="$1"
    for exclude in "${EXCLUDES[@]}"; do
        if [[ "$name" == "$exclude" ]]; then
            return 0
        fi
    done
    return 1
}

# Función recursiva para mostrar la jerarquía y contenido
show_tree() {
    local path="$1"
    local indent="$2"

    for file in "$path"/* "$path"/.*; do
        # Ignorar '.' y '..'
        [[ "$(basename "$file")" == "." || "$(basename "$file")" == ".." ]] && continue
        
        if is_excluded "$(basename "$file")"; then
            continue
        fi

        if [[ -d "$file" ]]; then
            echo "${indent}📁 $(basename "$file")"
            show_tree "$file" "  $indent"
        elif [[ -f "$file" ]]; then
            echo "${indent}📄 $(basename "$file")"
            cat "$file"
            echo "----------------------------------------"
        fi
    done
}

# Ejecutar
rm vibe-content.txt
cat "./vibe-content-base.txt" > "/tmp/vibe-content.txt"
show_tree "$DIR" "" >> "/tmp/vibe-content.txt"
mv "/tmp/vibe-content.txt" .

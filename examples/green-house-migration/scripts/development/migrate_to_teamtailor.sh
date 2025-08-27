#!/bin/bash

# Script de migración automatizada: Greenhouse → TeamTailor
# Uso: ./scripts/migrate_to_teamtailor.sh

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
API_BASE="http://localhost:8000"
TT_TOKEN=${TT_TOKEN:-""}

# Funciones de logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar prerrequisitos
check_prerequisites() {
    log_info "Verificando prerrequisitos..."

    if [ -z "$TT_TOKEN" ]; then
        log_error "TT_TOKEN no está configurado"
        echo "Por favor, configura la variable de entorno:"
        echo "export TT_TOKEN='tu_token_de_teamtailor'"
        exit 1
    fi

    # Verificar que el servidor esté corriendo
    if ! curl -s "$API_BASE/" > /dev/null; then
        log_error "El servidor FastAPI no está corriendo en $API_BASE"
        echo "Por favor, inicia el servidor:"
        echo "pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        exit 1
    fi

    log_success "Prerrequisitos verificados"
}

# Crear prospect pools
create_prospect_pools() {
    log_info "Creando prospect pools..."

    # Engineering Prospects
    log_info "Creando pool 'Engineering Prospects'..."
    ENGINEERING_POOL=$(curl -s -X POST "$API_BASE/prospects/pools" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Engineering Prospects",
            "description": "Software engineering candidates from Greenhouse",
            "color": "#0076D7"
        }')

    ENGINEERING_POOL_ID=$(echo "$ENGINEERING_POOL" | jq -r '.id')
    log_success "Pool 'Engineering Prospects' creado con ID: $ENGINEERING_POOL_ID"

    # Design Prospects
    log_info "Creando pool 'Design Prospects'..."
    DESIGN_POOL=$(curl -s -X POST "$API_BASE/prospects/pools" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Design Prospects",
            "description": "UX/UI design candidates from Greenhouse",
            "color": "#FF6B35"
        }')

    DESIGN_POOL_ID=$(echo "$DESIGN_POOL" | jq -r '.id')
    log_success "Pool 'Design Prospects' creado con ID: $DESIGN_POOL_ID"

    # Product Prospects
    log_info "Creando pool 'Product Prospects'..."
    PRODUCT_POOL=$(curl -s -X POST "$API_BASE/prospects/pools" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Product Prospects",
            "description": "Product management candidates from Greenhouse",
            "color": "#4CAF50"
        }')

    PRODUCT_POOL_ID=$(echo "$PRODUCT_POOL" | jq -r '.id')
    log_success "Pool 'Product Prospects' creado con ID: $PRODUCT_POOL_ID"

    # Guardar IDs para uso posterior
    echo "$ENGINEERING_POOL_ID" > /tmp/engineering_pool_id
    echo "$DESIGN_POOL_ID" > /tmp/design_pool_id
    echo "$PRODUCT_POOL_ID" > /tmp/product_pool_id
}

# Migración de prueba
migrate_test_sample() {
    log_info "Ejecutando migración de prueba (10 candidates)..."

    TEST_RESULT=$(curl -s -X POST "$API_BASE/candidates/migrate/greenhouse?limit=10" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    CREATED=$(echo "$TEST_RESULT" | jq -r '.created')
    FAILED=$(echo "$TEST_RESULT" | jq -r '.failed')

    log_success "Migración de prueba completada: $CREATED creados, $FAILED fallidos"

    if [ "$FAILED" -gt 0 ]; then
        log_warning "Algunos candidates fallaron. Revisando errores..."
        echo "$TEST_RESULT" | jq -r '.errors[] | "Error: \(.error) - Data: \(.data)"'
    fi

    # Preguntar si continuar
    read -p "¿Continuar con la migración completa? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Migración cancelada por el usuario"
        exit 0
    fi
}

# Migración completa
migrate_all_candidates() {
    log_info "Iniciando migración completa de candidates..."

    MIGRATION_RESULT=$(curl -s -X POST "$API_BASE/candidates/migrate/greenhouse" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    CREATED=$(echo "$MIGRATION_RESULT" | jq -r '.created')
    FAILED=$(echo "$MIGRATION_RESULT" | jq -r '.failed')

    log_success "Migración completa finalizada: $CREATED creados, $FAILED fallidos"

    if [ "$FAILED" -gt 0 ]; then
        log_warning "Errores encontrados:"
        echo "$MIGRATION_RESULT" | jq -r '.errors[] | "Error: \(.error) - Data: \(.data)"'
    fi
}

# Organizar en prospect pools
organize_in_prospect_pools() {
    log_info "Organizando candidates en prospect pools..."

    # Engineering Prospects
    log_info "Migrando candidates a 'Engineering Prospects'..."
    ENGINEERING_RESULT=$(curl -s -X POST "$API_BASE/prospects/migrate/greenhouse?pool_name=Engineering%20Prospects&limit=100" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    ENGINEERING_ADDED=$(echo "$ENGINEERING_RESULT" | jq -r '.candidates_added')
    ENGINEERING_FAILED=$(echo "$ENGINEERING_RESULT" | jq -r '.candidates_failed')

    log_success "Engineering Prospects: $ENGINEERING_ADDED añadidos, $ENGINEERING_FAILED fallidos"

    # Design Prospects
    log_info "Migrando candidates a 'Design Prospects'..."
    DESIGN_RESULT=$(curl -s -X POST "$API_BASE/prospects/migrate/greenhouse?pool_name=Design%20Prospects&limit=50" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    DESIGN_ADDED=$(echo "$DESIGN_RESULT" | jq -r '.candidates_added')
    DESIGN_FAILED=$(echo "$DESIGN_RESULT" | jq -r '.candidates_failed')

    log_success "Design Prospects: $DESIGN_ADDED añadidos, $DESIGN_FAILED fallidos"

    # Product Prospects
    log_info "Migrando candidates a 'Product Prospects'..."
    PRODUCT_RESULT=$(curl -s -X POST "$API_BASE/prospects/migrate/greenhouse?pool_name=Product%20Prospects&limit=30" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    PRODUCT_ADDED=$(echo "$PRODUCT_RESULT" | jq -r '.candidates_added')
    PRODUCT_FAILED=$(echo "$PRODUCT_RESULT" | jq -r '.candidates_failed')

    log_success "Product Prospects: $PRODUCT_ADDED añadidos, $PRODUCT_FAILED fallidos"
}

# Verificación final
verify_migration() {
    log_info "Verificando migración..."

    # Contar candidates totales
    CANDIDATES_RESPONSE=$(curl -s -X GET "$API_BASE/candidates/?per_page=1" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    TOTAL_CANDIDATES=$(echo "$CANDIDATES_RESPONSE" | jq -r '.total')
    log_success "Total de candidates en TeamTailor: $TOTAL_CANDIDATES"

    # Verificar prospect pools
    POOLS_RESPONSE=$(curl -s -X GET "$API_BASE/prospects/pools" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    log_info "Prospect pools creados:"
    echo "$POOLS_RESPONSE" | jq -r '.pools[] | "- \(.name): \(.candidate_count) candidates"'

    # Buscar algunos candidates específicos
    log_info "Buscando candidates con external IDs..."
    SEARCH_RESULT=$(curl -s -X GET "$API_BASE/candidates/?search=gh_cand" \
        -H "Authorization: Token token=$TT_TOKEN" \
        -H "Content-Type: application/json")

    EXTERNAL_ID_COUNT=$(echo "$SEARCH_RESULT" | jq -r '.candidates | length')
    log_success "Candidates con external IDs encontrados: $EXTERNAL_ID_COUNT"
}

# Función principal
main() {
    echo "🚀 Iniciando migración Greenhouse → TeamTailor"
    echo "=============================================="

    check_prerequisites
    create_prospect_pools
    migrate_test_sample
    migrate_all_candidates
    organize_in_prospect_pools
    verify_migration

    echo ""
    echo "🎉 ¡Migración completada exitosamente!"
    echo ""
    echo "📊 Resumen:"
    echo "- Candidates migrados a TeamTailor"
    echo "- Prospect pools creados y organizados"
    echo "- External IDs preservados para referencia"
    echo ""
    echo "🔗 Próximos pasos:"
    echo "1. Revisar candidates en TeamTailor dashboard"
    echo "2. Verificar prospect pools"
    echo "3. Configurar workflows y stages"
    echo "4. Importar applications si es necesario"
}

# Ejecutar script
main "$@"

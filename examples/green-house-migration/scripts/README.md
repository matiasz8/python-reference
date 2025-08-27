# 📜 Scripts del Proyecto

## 📁 Estructura de Directorios

```bash
scripts/
├── README.md                    # Este archivo
├── __init__.py
├── aggressive_cleanup.py        # Limpieza agresiva del proyecto
├── teamtailor/                  # Scripts específicos de TeamTailor
│   ├── README.md               # Documentación de scripts TeamTailor
│   ├── quick_start_tagging.py  # Inicio rápido del sistema de tags
│   ├── add_candidate_tags.py   # Aplicar tags a candidatos
│   ├── fast_batch_migration.py # Migración masiva
│   ├── verify_migration.py     # Verificar migración
│   └── ...                     # Otros scripts de TeamTailor
├── dashboard/                   # Scripts de dashboard
│   ├── diagnose_dashboard.py   # Diagnóstico completo
│   └── ...                     # Scripts de mantenimiento
├── testing/                     # Scripts de testing
│   ├── test_dashboard_browser.py # Test como navegador
│   ├── test_dual_dashboard.py   # Test dashboard dual
│   ├── test_filters.py          # Test de filtros
│   └── ...                      # Otros tests
├── analysis/                    # Scripts de análisis
│   └── ...                      # Análisis de datos
├── development/                 # Scripts de desarrollo
│   ├── setup_dev_env.sh        # Setup del entorno
│   └── ...                      # Herramientas de desarrollo
├── security/                    # Scripts de seguridad
│   ├── security_analysis.py    # Análisis de seguridad
│   └── ...                      # Auditorías de seguridad
└── cleanup/                     # Scripts de limpieza
    └── ...                      # Limpieza y mantenimiento
```bash

## 🚀 Scripts Principales

### 🔧 Configuración y Setup

#### `setup-dev.sh`

**Ubicación**: `./setup-dev.sh`
**Descripción**: Script principal de configuración del proyecto

```bash
./setup-dev.sh
```bash

#### `start_server.sh`

**Ubicación**: `./scripts/start_server.sh`
**Descripción**: Iniciar el servidor de desarrollo

```bash
./scripts/start_server.sh
```text

### 🏷️ Sistema de Tags

#### `quick_start_tagging.py`

**Ubicación**: `scripts/teamtailor/quick_start_tagging.py`
**Descripción**: Menú interactivo para el sistema de tags

```bash
pipenv run python scripts/teamtailor/quick_start_tagging.py
```text

#### `add_candidate_tags.py`

**Ubicación**: `scripts/teamtailor/add_candidate_tags.py`
**Descripción**: Aplicar tags a candidatos

```bash
pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123
--tags "python,react"
```text

#### `fast_batch_migration.py`

**Ubicación**: `scripts/teamtailor/fast_batch_migration.py`
**Descripción**: Migración masiva de candidatos

```bash
pipenv run python scripts/teamtailor/fast_batch_migration.py --limit 100 --live
```bash

### 📊 Dashboards

#### `diagnose_dashboard.py`

**Ubicación**: `scripts/dashboard/diagnose_dashboard.py`
**Descripción**: Diagnóstico completo del sistema de dashboards

```bash
pipenv run python scripts/dashboard/diagnose_dashboard.py
```bash

### 🧪 Testing

#### `test_dashboard_browser.py`

**Ubicación**: `scripts/testing/test_dashboard_browser.py`
**Descripción**: Simular comportamiento del navegador

```bash
pipenv run python scripts/testing/test_dashboard_browser.py
```bash

#### `test_dual_dashboard.py`

**Ubicación**: `scripts/testing/test_dual_dashboard.py`
**Descripción**: Tests específicos del dashboard dual

```bash
pipenv run python scripts/testing/test_dual_dashboard.py
```text

### 🔒 Seguridad

#### `security_analysis.py`

**Ubicación**: `scripts/security/security_analysis.py`
**Descripción**: Análisis de seguridad del código

```bash
pipenv run python scripts/security/security_analysis.py
```text

### 🧹 Limpieza

#### `aggressive_cleanup.py`

**Ubicación**: `scripts/aggressive_cleanup.py`
**Descripción**: Limpieza agresiva del proyecto

```bash
pipenv run python scripts/aggressive_cleanup.py
```text

## 🎯 Flujos de Trabajo Comunes

### 1. Configuración Inicial

```bash
./setup-dev.sh
./scripts/start_server.sh
```text

### 2. Sistema de Tags

```bash
# Ver opciones disponibles
pipenv run python scripts/teamtailor/quick_start_tagging.py

# Aplicar tags a un candidato
pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123
--tags "python,react"

# Migración masiva
pipenv run python scripts/teamtailor/fast_batch_migration.py --limit 100 --live
```text

### 3. Diagnóstico de Problemas

```bash
# Diagnóstico completo
pipenv run python scripts/dashboard/diagnose_dashboard.py

# Test como navegador
pipenv run python scripts/testing/test_dashboard_browser.py

# Test específico
pipenv run python scripts/testing/test_dual_dashboard.py
```text

### 4. Mantenimiento

```bash
# Análisis de seguridad
pipenv run python scripts/security/security_analysis.py

# Limpieza del proyecto
pipenv run python scripts/aggressive_cleanup.py
```bash

## 📋 Categorías de Scripts

### 🔧 Configuración

- Scripts de setup y configuración del entorno
- Configuración de variables de entorno
- Instalación de dependencias

### 🏷️ TeamTailor

- Gestión del sistema de tags
- Migración de datos
- Análisis de candidatos
- Verificación de migraciones

### 📊 Dashboard

- Diagnóstico de dashboards
- Testing de funcionalidades
- Mantenimiento y limpieza
- Análisis de performance

### 🧪 Testing 2

- Tests automatizados
- Simulación de navegador
- Validación de endpoints
- Tests de carga

### 🔒 Seguridad 2

- Análisis de vulnerabilidades
- Auditorías de código
- Verificación de configuraciones
- Reportes de seguridad

### 🧹 Limpieza 2

- Limpieza de archivos temporales
- Optimización de performance
- Mantenimiento del proyecto
- Backup de datos

## ⚠️ Consideraciones

### Variables de Entorno

```bash
# Para scripts de TeamTailor
TT_TOKEN=your_token
TT_BASE_URL=https://api.teamtailor.com
TT_API_VERSION=v1

# Para modo de prueba
TEAMTAILOR_TEST_MODE=true
```

### Logs

- **Ubicación**: `logs/`
- **Rotación**: Automática por fecha
- **Nivel**: Configurable por script

### Rate Limiting

- **API Calls**: 1 segundo entre requests
- **Bulk Operations**: 5 segundos entre lotes
- **Testing**: Configurable por script

## 🔗 Enlaces Relacionados

- [Documentación Principal](../docs/README.md)
- [Sistema de Tags](../docs/features/tag-system/README.md)
- [Sistema de Dashboards](../docs/features/dashboard/README.md)
- [Scripts de TeamTailor](teamtailor/README.md)
- [Scripts de Dashboard](dashboard/README.md)

## 📞 Soporte

### Problemas Comunes

1. **Script no ejecuta**: Verificar dependencias con `pipenv install`
2. **Errores de API**: Verificar variables de entorno
3. **Problemas de permisos**: Verificar permisos de archivos

### Herramientas de Diagnóstico

- **Diagnóstico Rápido**: `scripts/dashboard/diagnose_dashboard.py`
- **Test de Navegador**: `scripts/testing/test_dashboard_browser.py`
- **Validación de Datos**: `scripts/dashboard/data_validation.py`

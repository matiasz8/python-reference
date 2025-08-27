# Scripts de Dashboard

## 📁 Ubicación

Todos los scripts se encuentran en `scripts/` y `scripts/dashboard/`

## 🚀 Scripts Principales

### 1. `diagnose_dashboard.py`

**Descripción**: Diagnóstico completo del sistema de dashboards

```bash
pipenv run python scripts/diagnose_dashboard.py
```bash

**Funcionalidades**:

- Test de todos los endpoints del dashboard
- Verificación de conectividad
- Validación de datos
- Reporte de estado completo

**Endpoints Verificados**:

- `/dashboard/` - Dashboard principal
- `/dashboard/dual` - Dashboard dual
- `/dashboard/static/dual_dashboard.js` - JavaScript
- `/api/teamtailor/local/stats` - Stats locales
- `/api/teamtailor/local/candidates` - Candidatos locales
- `/api/teamtailor/test` - Test TeamTailor
- `/api/teamtailor/stats` - Stats TeamTailor
- `/api/teamtailor/candidates` - Candidatos TeamTailor

### 2. `test_dashboard_browser.py`

**Descripción**: Simula el comportamiento del navegador

```bash
pipenv run python scripts/test_dashboard_browser.py
```bash

**Funcionalidades**:

- Carga de HTML como navegador
- Verificación de elementos JavaScript
- Test de endpoints como JavaScript
- Diagnóstico de problemas de frontend

### 3. `test_dual_dashboard.py`

**Descripción**: Tests específicos del dashboard dual

```bash
pipenv run python scripts/test_dual_dashboard.py
```text

**Funcionalidades**:

- Test de carga de datos duales
- Verificación de filtros
- Validación de comparaciones
- Performance testing

### 4. `test_filters.py`

**Descripción**: Tests de funcionalidad de filtros

```bash
pipenv run python scripts/test_filters.py
```bash

**Funcionalidades**:

- Test de filtros por texto
- Test de filtros por tags
- Test de filtros por categorías
- Validación de búsquedas

## 🔧 Scripts de Utilidad

### 5. `dashboard/performance_test.py`

**Descripción**: Tests de rendimiento del dashboard

```bash
pipenv run python scripts/dashboard/performance_test.py
```bash

**Métricas**:

- Tiempo de carga de páginas
- Tiempo de respuesta de APIs
- Uso de memoria
- Throughput de requests

### 6. `dashboard/data_validation.py`

**Descripción**: Validación de datos del dashboard

```bash
pipenv run python scripts/dashboard/data_validation.py
```bash

**Validaciones**:

- Integridad de datos JSON
- Consistencia entre fuentes
- Validación de esquemas
- Detección de duplicados

## 🧪 Scripts de Testing

### 7. `dashboard/load_test.py`

**Descripción**: Tests de carga del dashboard

```bash
pipenv run python scripts/dashboard/load_test.py --users 10 --duration 60
```bash

**Opciones**:

- `--users`: Número de usuarios simulados
- `--duration`: Duración del test en segundos
- `--endpoint`: Endpoint específico a testear

### 8. `dashboard/api_test.py`

**Descripción**: Tests de API del dashboard

```bash
pipenv run python scripts/dashboard/api_test.py
```bash

**Tests**:

- Endpoints de stats
- Endpoints de candidatos
- Endpoints de búsqueda
- Validación de respuestas

## 📊 Scripts de Análisis

### 9. `dashboard/usage_analytics.py`

**Descripción**: Análisis de uso del dashboard

```bash
pipenv run python scripts/dashboard/usage_analytics.py
```bash

**Métricas**:

- Páginas más visitadas
- Tiempo de sesión
- Errores más comunes
- Performance por endpoint

### 10. `dashboard/data_quality.py`

**Descripción**: Análisis de calidad de datos

```bash
pipenv run python scripts/dashboard/data_quality.py
```bash

**Análisis**:

- Completitud de datos
- Consistencia de formatos
- Detección de outliers
- Validación de rangos

## 🔄 Scripts de Mantenimiento

### 11. `dashboard/cleanup_cache.py`

**Descripción**: Limpieza de cache del dashboard

```bash
pipenv run python scripts/dashboard/cleanup_cache.py
```bash

**Funcionalidades**:

- Limpieza de archivos temporales
- Reset de datos en memoria
- Limpieza de logs antiguos
- Optimización de performance

### 12. `dashboard/backup_data.py`

**Descripción**: Backup de datos del dashboard

```bash
pipenv run python scripts/dashboard/backup_data.py
```bash

**Backups**:

- Datos de candidatos
- Configuraciones
- Logs importantes
- Estados del sistema

## 🎯 Flujo de Diagnóstico

### Diagnóstico Rápido

1. **Test Básico**: `diagnose_dashboard.py`
2. **Test Navegador**: `test_dashboard_browser.py`
3. **Test Específico**: `test_dual_dashboard.py`

### Diagnóstico Completo

1. **Performance**: `dashboard/performance_test.py`
2. **Datos**: `dashboard/data_validation.py`
3. **Carga**: `dashboard/load_test.py`
4. **API**: `dashboard/api_test.py`

### Mantenimiento

1. **Análisis**: `dashboard/usage_analytics.py`
2. **Calidad**: `dashboard/data_quality.py`
3. **Limpieza**: `dashboard/cleanup_cache.py`
4. **Backup**: `dashboard/backup_data.py`

## 📋 Reportes Generados

### Tipos de Reporte

- **Estado del Sistema**: Endpoints, conectividad, errores
- **Performance**: Tiempos de respuesta, throughput
- **Calidad de Datos**: Completitud, consistencia, validaciones
- **Uso**: Métricas de utilización, patrones de acceso

### Formato de Reportes

- **Consola**: Output directo en terminal
- **JSON**: Datos estructurados para análisis
- **HTML**: Reportes visuales para navegador
- **Logs**: Archivos de log para auditoría

## ⚠️ Consideraciones

### Variables de Entorno

```bash
# Para tests
TEAMTAILOR_TEST_MODE=true
DASHBOARD_DEBUG=true

# Para performance
DASHBOARD_PERFORMANCE_MODE=true
```

### Logs

- **Ubicación**: `logs/dashboard/`
- **Rotación**: Automática por fecha
- **Nivel**: Configurable por script

### Rate Limiting

- **API Calls**: 1 segundo entre requests
- **Bulk Operations**: 5 segundos entre lotes
- **Testing**: Configurable por script

## 🔗 Enlaces Relacionados

- [Sistema de Dashboards](../../features/dashboard/README.md)
- [Sistema de Tags](../../features/tag-system/README.md)
- [API de TeamTailor](../../api/TEAMTAILOR_API_ENDPOINTS.md)
- [Guías de Desarrollo](../../development/README.md)

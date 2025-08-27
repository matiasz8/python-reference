#!/usr/bin/env python3
"""
Script de ayuda interactivo para navegar por la documentación y scripts del proyecto
"""

import os
import sys
from pathlib import Path


def print_header(title):
    """Imprimir un header formateado"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)


def print_section(title):
    """Imprimir una sección"""
    print(f"\n📋 {title}")
    print("-" * 40)


def print_item(title, description, command=None):
    """Imprimir un ítem con formato"""
    print(f"• {title}")
    print(f"  {description}")
    if command:
        print(f"  💻 {command}")
    print()


def show_main_menu():
    """Mostrar menú principal"""
    print_header("SISTEMA DE AYUDA - GREENHOUSE PROJECT")

    options = [
        ("1", "🚀 Inicio Rápido", "Guías de configuración y uso básico"),
        ("2", "🏷️ Sistema de Tags", "Gestión de tags y migración de candidatos"),
        ("3", "📊 Dashboards", "Interfaces web y herramientas de visualización"),
        ("4", "🔧 Scripts", "Herramientas y utilidades disponibles"),
        ("5", "📚 Documentación", "Enlaces a documentación completa"),
        ("6", "🚨 Solución de Problemas", "Diagnóstico y troubleshooting"),
        ("7", "📋 Estado del Proyecto", "Qué está completado y qué falta"),
        ("0", "❌ Salir", "Salir del sistema de ayuda"),
    ]

    for option, title, description in options:
        print(f"{option}. {title}")
        print(f"   {description}")

    return input("\n🔍 Selecciona una opción: ")


def show_quick_start():
    """Mostrar guía de inicio rápido"""
    print_header("INICIO RÁPIDO")

    print_section("1. Configuración Inicial")
    print_item(
        "Setup Automático", "Configurar todo el entorno de desarrollo", "./setup-dev.sh"
    )

    print_item(
        "Configurar Variables de Entorno",
        "Copiar y configurar archivo .env",
        "cp .env.example .env && nano .env",
    )

    print_section("2. Ejecutar el Proyecto")
    print_item(
        "Iniciar Servidor (Desarrollo)",
        "Servidor con auto-reload",
        "./scripts/start_server.sh",
    )

    print_item(
        "Iniciar Servidor (Directo)",
        "Comando directo de uvicorn",
        "pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000",
    )

    print_section("3. Acceder a Dashboards")
    print_item(
        "Dashboard Principal",
        "Dashboard original con datos de TeamTailor",
        "http://localhost:8000/dashboard/",
    )

    print_item(
        "Dashboard Dual",
        "Dashboard con datos locales y TeamTailor",
        "http://localhost:8000/dashboard/dual",
    )

    print_item(
        "Página de Pruebas",
        "Herramienta de diagnóstico",
        "http://localhost:8000/dashboard/test",
    )

    print_section("4. Sistema de Tags")
    print_item(
        "Ver Tags Disponibles",
        "Menú interactivo del sistema de tags",
        "pipenv run python scripts/teamtailor/quick_start_tagging.py",
    )

    print_item(
        "Aplicar Tags",
        "Aplicar tags a un candidato específico",
        "pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags 'python,react'",
    )


def show_tag_system():
    """Mostrar información del sistema de tags"""
    print_header("SISTEMA DE TAGS")

    print_section("Scripts Principales")
    print_item(
        "quick_start_tagging.py",
        "Menú interactivo para comenzar con el sistema de tags",
        "pipenv run python scripts/teamtailor/quick_start_tagging.py",
    )

    print_item(
        "add_candidate_tags.py",
        "Aplicar tags a candidatos individuales o en lote",
        "pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags 'python,react'",
    )

    print_item(
        "fast_batch_migration.py",
        "Migración rápida y masiva de candidatos con tags",
        "pipenv run python scripts/teamtailor/fast_batch_migration.py --limit 100 --live",
    )

    print_section("Scripts de Utilidad")
    print_item(
        "example_tag_usage.py",
        "Ejemplos de uso del sistema de tags",
        "pipenv run python scripts/teamtailor/example_tag_usage.py",
    )

    print_item(
        "demo_tag_system.py",
        "Demo del sistema sin conexión real a TeamTailor",
        "pipenv run python scripts/teamtailor/demo_tag_system.py",
    )

    print_item(
        "verify_migration.py",
        "Verificar el éxito de la migración",
        "pipenv run python scripts/teamtailor/verify_migration.py",
    )

    print_section("Flujo de Trabajo Recomendado")
    steps = [
        "1. quick_start_tagging.py - Ver opciones disponibles",
        "2. demo_tag_system.py - Probar sin conexión real",
        "3. fast_batch_migration.py --dry-run - Simular migración",
        "4. verify_migration.py - Verificar resultados",
        "5. fast_batch_migration.py --live - Aplicar cambios reales",
    ]

    for step in steps:
        print(f"   {step}")

    print_section("Variables de Entorno Requeridas")
    env_vars = [
        "TT_TOKEN=your_teamtailor_token",
        "TT_BASE_URL=https://api.teamtailor.com",
        "TT_API_VERSION=v1",
        "TEAMTAILOR_TEST_MODE=true  # Para pruebas",
    ]

    for var in env_vars:
        print(f"   {var}")


def show_dashboards():
    """Mostrar información de dashboards"""
    print_header("SISTEMAS DE DASHBOARDS")

    print_section("Dashboards Disponibles")
    print_item(
        "Dashboard Principal",
        "Dashboard original con datos de TeamTailor",
        "http://localhost:8000/dashboard/",
    )

    print_item(
        "Dashboard Dual",
        "Dashboard con dos fuentes de datos (local + TeamTailor)",
        "http://localhost:8000/dashboard/dual",
    )

    print_item(
        "Página de Pruebas",
        "Herramienta de diagnóstico y testing",
        "http://localhost:8000/dashboard/test",
    )

    print_section("Scripts de Diagnóstico")
    print_item(
        "diagnose_dashboard.py",
        "Diagnóstico completo del sistema de dashboards",
        "pipenv run python scripts/dashboard/diagnose_dashboard.py",
    )

    print_item(
        "test_dashboard_browser.py",
        "Simular comportamiento del navegador",
        "pipenv run python scripts/testing/test_dashboard_browser.py",
    )

    print_item(
        "test_dual_dashboard.py",
        "Tests específicos del dashboard dual",
        "pipenv run python scripts/testing/test_dual_dashboard.py",
    )

    print_section("Endpoints de API")
    endpoints = [
        ("/api/teamtailor/local/stats", "Estadísticas de datos locales"),
        ("/api/teamtailor/local/candidates", "Lista de candidatos locales"),
        ("/api/teamtailor/stats", "Estadísticas de TeamTailor"),
        ("/api/teamtailor/candidates", "Lista de candidatos de TeamTailor"),
        ("/api/teamtailor/test", "Test de conectividad"),
        ("/candidate-tags/search", "Búsqueda por tags"),
    ]

    for endpoint, description in endpoints:
        print(f"   {endpoint}")
        print(f"     {description}")
        print()


def show_scripts():
    """Mostrar información de scripts"""
    print_header("SCRIPTS Y HERRAMIENTAS")

    print_section("Scripts de Configuración")
    print_item(
        "setup-dev.sh",
        "Script principal de configuración del proyecto",
        "./setup-dev.sh",
    )

    print_item(
        "start_server.sh",
        "Iniciar el servidor de desarrollo",
        "./scripts/start_server.sh",
    )

    print_section("Scripts de TeamTailor")
    print_item(
        "quick_start_tagging.py",
        "Menú interactivo para el sistema de tags",
        "pipenv run python scripts/teamtailor/quick_start_tagging.py",
    )

    print_item(
        "add_candidate_tags.py",
        "Aplicar tags a candidatos",
        "pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags 'python,react'",
    )

    print_item(
        "fast_batch_migration.py",
        "Migración masiva de candidatos",
        "pipenv run python scripts/teamtailor/fast_batch_migration.py --limit 100 --live",
    )

    print_section("Scripts de Dashboard")
    print_item(
        "diagnose_dashboard.py",
        "Diagnóstico completo del sistema de dashboards",
        "pipenv run python scripts/dashboard/diagnose_dashboard.py",
    )

    print_section("Scripts de Testing")
    print_item(
        "test_dashboard_browser.py",
        "Simular comportamiento del navegador",
        "pipenv run python scripts/testing/test_dashboard_browser.py",
    )

    print_item(
        "test_dual_dashboard.py",
        "Tests específicos del dashboard dual",
        "pipenv run python scripts/testing/test_dual_dashboard.py",
    )

    print_section("Scripts de Seguridad")
    print_item(
        "security_analysis.py",
        "Análisis de seguridad del código",
        "pipenv run python scripts/security/security_analysis.py",
    )

    print_section("Scripts de Limpieza")
    print_item(
        "aggressive_cleanup.py",
        "Limpieza agresiva del proyecto",
        "pipenv run python scripts/aggressive_cleanup.py",
    )


def show_documentation():
    """Mostrar enlaces a documentación"""
    print_header("DOCUMENTACIÓN COMPLETA")

    print_section("Documentación Principal")
    print_item(
        "README Principal", "Documentación general del proyecto", "docs/README.md"
    )

    print_item(
        "Sistema de Tags",
        "Documentación completa del sistema de tags",
        "docs/features/tag-system/README.md",
    )

    print_item(
        "Sistema de Dashboards",
        "Documentación de dashboards y interfaces",
        "docs/features/dashboard/README.md",
    )

    print_section("Guías y Tutoriales")
    print_item(
        "Guías de Migración",
        "Proceso de migración de datos",
        "docs/guides/migration/README.md",
    )

    print_item(
        "Guías de Desarrollo",
        "Setup y contribución al proyecto",
        "docs/development/README.md",
    )

    print_section("Scripts")
    print_item(
        "Scripts de TeamTailor",
        "Documentación de scripts de TeamTailor",
        "docs/scripts/teamtailor/README.md",
    )

    print_item(
        "Scripts de Dashboard",
        "Documentación de scripts de dashboard",
        "docs/scripts/dashboard/README.md",
    )

    print_section("APIs")
    print_item(
        "API de TeamTailor",
        "Endpoints y documentación de API",
        "docs/api/TEAMTAILOR_API_ENDPOINTS.md",
    )

    print_item(
        "API de Candidatos",
        "Gestión de candidatos y prospects",
        "docs/api/CANDIDATES_PROSPECTS_API.md",
    )


def show_troubleshooting():
    """Mostrar solución de problemas"""
    print_header("SOLUCIÓN DE PROBLEMAS")

    print_section("Problemas Comunes")

    print_item(
        "Dashboard no carga datos",
        "Verificar conectividad y endpoints",
        "http://localhost:8000/dashboard/test",
    )

    print_item(
        "Errores de API", "Verificar variables de entorno", "cat .env | grep TT_"
    )

    print_item("Scripts no ejecutan", "Verificar dependencias", "pipenv install")

    print_section("Herramientas de Diagnóstico")
    print_item(
        "Diagnóstico Rápido",
        "Test completo del sistema",
        "pipenv run python scripts/dashboard/diagnose_dashboard.py",
    )

    print_item(
        "Test de Navegador",
        "Simular comportamiento del navegador",
        "pipenv run python scripts/testing/test_dashboard_browser.py",
    )

    print_item(
        "Validación de Datos",
        "Verificar integridad de datos",
        "pipenv run python scripts/dashboard/data_validation.py",
    )

    print_section("Pasos de Diagnóstico")
    steps = [
        "1. Verificar que el servidor esté corriendo",
        "2. Probar conectividad básica: curl http://localhost:8000/",
        "3. Usar página de pruebas: http://localhost:8000/dashboard/test",
        "4. Revisar logs del servidor",
        "5. Verificar variables de entorno",
        "6. Ejecutar script de diagnóstico completo",
    ]

    for step in steps:
        print(f"   {step}")

    print_section("Logs Importantes")
    logs = [
        "logs/dashboard.log - Logs del dashboard",
        "logs/teamtailor.log - Logs de TeamTailor",
        "logs/error.log - Errores generales",
    ]

    for log in logs:
        print(f"   {log}")


def show_project_status():
    """Mostrar estado del proyecto"""
    print_header("ESTADO DEL PROYECTO")

    print_section("✅ Completado")
    completed = [
        "Sistema de tags estructurado",
        "Dashboard dual (local + TeamTailor)",
        "API endpoints completos",
        "Scripts de migración",
        "Documentación organizada",
        "Herramientas de diagnóstico",
        "Sistema de filtros avanzados",
        "Página de pruebas y diagnóstico",
    ]

    for item in completed:
        print(f"   ✅ {item}")

    print_section("🔄 En Progreso")
    in_progress = [
        "Optimización de performance",
        "Tests automatizados",
        "Monitoreo avanzado",
    ]

    for item in in_progress:
        print(f"   🔄 {item}")

    print_section("📋 Pendiente")
    pending = [
        "Exportación de datos",
        "Notificaciones en tiempo real",
        "Gráficos avanzados",
        "Modo offline",
        "Personalización de dashboards",
    ]

    for item in pending:
        print(f"   📋 {item}")

    print_section("📊 Métricas Actuales")
    metrics = [
        "Candidatos Locales: ~3,656 únicos",
        "Candidatos TeamTailor: ~25 (paginados)",
        "Tags Disponibles: 50+ categorizados",
        "Categorías: 7 tipos principales",
        "Scripts Disponibles: 20+ herramientas",
    ]

    for metric in metrics:
        print(f"   📊 {metric}")


def main():
    """Función principal del script de ayuda"""
    while True:
        choice = show_main_menu()

        if choice == "1":
            show_quick_start()
        elif choice == "2":
            show_tag_system()
        elif choice == "3":
            show_dashboards()
        elif choice == "4":
            show_scripts()
        elif choice == "5":
            show_documentation()
        elif choice == "6":
            show_troubleshooting()
        elif choice == "7":
            show_project_status()
        elif choice == "0":
            print("\n👋 ¡Gracias por usar el sistema de ayuda!")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")

        input("\n⏸️  Presiona Enter para continuar...")


if __name__ == "__main__":
    main()

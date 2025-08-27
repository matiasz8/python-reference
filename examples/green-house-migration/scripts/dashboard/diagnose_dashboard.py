#!/usr/bin/env python3
"""
Dashboard Diagnosis Script

Script to diagnose and test all dashboard endpoints.
"""

import json
import time
from typing import Any, Dict

import requests


def test_endpoint(url: str, name: str) -> Dict[str, Any]:
    """Test a specific endpoint."""
    try:
        print(f"🔍 Probando {name}...")
        start_time = time.time()

        response = requests.get(url, timeout=10)
        duration = time.time() - start_time

        if response.status_code == 200:
            try:
                data = response.json()
                return {
                    "status": "success",
                    "status_code": response.status_code,
                    "duration": round(duration, 2),
                    "data": data,
                }
            except json.JSONDecodeError:
                return {
                    "status": "success",
                    "status_code": response.status_code,
                    "duration": round(duration, 2),
                    "data": "HTML content (not JSON)",
                }
        else:
            return {
                "status": "error",
                "status_code": response.status_code,
                "duration": round(duration, 2),
                "error": response.text,
            }

    except requests.exceptions.Timeout:
        return {"status": "timeout", "duration": 10, "error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"status": "connection_error", "error": "Connection failed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    """Main diagnosis function."""
    base_url = "http://localhost:8000"

    print("🔧 DIAGNÓSTICO DEL DASHBOARD")
    print("=" * 50)

    # Test endpoints
    endpoints = [
        (f"{base_url}/dashboard/", "Dashboard Principal"),
        (f"{base_url}/dashboard/dual", "Dashboard Dual"),
        (f"{base_url}/dashboard/static/dual_dashboard.js", "JavaScript Dual Dashboard"),
        (f"{base_url}/api/teamtailor/local/stats", "API Stats Local (Dual)"),
        (f"{base_url}/api/teamtailor/local/candidates", "API Candidates Local (Dual)"),
        (f"{base_url}/api/teamtailor/test", "API TeamTailor Test"),
        (f"{base_url}/api/teamtailor/stats", "API TeamTailor Stats"),
        (f"{base_url}/api/teamtailor/candidates", "API TeamTailor Candidates"),
    ]

    results = {}

    for url, name in endpoints:
        result = test_endpoint(url, name)
        results[name] = result

        # Print result
        if result["status"] == "success":
            print(f"   ✅ {name}: {result['status_code']} ({result['duration']}s)")
        else:
            print(
                f"   ❌ {name}: {result['status']} - {result.get('error', 'Unknown error')}"
            )

    # Summary
    print("\n" + "=" * 50)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 50)

    successful = sum(1 for r in results.values() if r["status"] == "success")
    total = len(results)

    print(f"Total de endpoints probados: {total}")
    print(f"✅ Exitosos: {successful}")
    print(f"❌ Fallidos: {total - successful}")
    print(f"Tasa de éxito: {(successful/total)*100:.1f}%")

    # Detailed results
    print("\n📋 RESULTADOS DETALLADOS:")
    print("-" * 30)

    for name, result in results.items():
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{status_icon} {name}")
        print(f"   Estado: {result['status']}")
        if "status_code" in result:
            print(f"   Código: {result['status_code']}")
        if "duration" in result:
            print(f"   Tiempo: {result['duration']}s")
        if "error" in result:
            print(f"   Error: {result['error']}")
        print()

    # Recommendations
    print("💡 RECOMENDACIONES:")
    print("-" * 20)

    if results["Dashboard Principal"]["status"] != "success":
        print("• Verificar que el dashboard principal esté funcionando")

    if results["Dashboard Dual"]["status"] != "success":
        print("• Verificar que el dashboard dual esté funcionando")

    if results["JavaScript Dual Dashboard"]["status"] != "success":
        print("• Verificar que el archivo JavaScript esté accesible")

    if results["API TeamTailor Test"]["status"] != "success":
        print("• Verificar la conectividad con TeamTailor")

    if results["API TeamTailor Stats"]["status"] != "success":
        print("• Verificar el endpoint de estadísticas de TeamTailor")

    print("\n🎉 ¡Diagnóstico completado!")


if __name__ == "__main__":
    main()

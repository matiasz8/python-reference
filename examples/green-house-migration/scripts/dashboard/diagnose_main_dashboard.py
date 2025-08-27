#!/usr/bin/env python3
"""
Diagnóstico específico para el Dashboard Principal
"""

from pathlib import Path

import requests


def test_dashboard_endpoints():
    """Test all dashboard-related endpoints."""
    base_url = "http://localhost:8000"

    print("🔍 Diagnóstico del Dashboard Principal")
    print("=" * 50)

    # Test 1: Main dashboard HTML
    print("\n1. Testing Dashboard HTML...")
    try:
        response = requests.get(f"{base_url}/dashboard/")
        if response.status_code == 200:
            print("✅ Dashboard HTML: OK")
            if "TeamTailor Sourced Candidates Analytics Dashboard" in response.text:
                print("✅ Dashboard title found in HTML")
            else:
                print("⚠️ Dashboard title not found in HTML")
        else:
            print(f"❌ Dashboard HTML: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard HTML: Error - {e}")

    # Test 2: Dashboard JavaScript
    print("\n2. Testing Dashboard JavaScript...")
    try:
        response = requests.get(f"{base_url}/dashboard/static/dashboard.js")
        if response.status_code == 200:
            print("✅ Dashboard JavaScript: OK")
            if "ProspectsDashboard" in response.text:
                print("✅ ProspectsDashboard class found")
            else:
                print("⚠️ ProspectsDashboard class not found")
        else:
            print(f"❌ Dashboard JavaScript: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard JavaScript: Error - {e}")

    # Test 3: Analytics endpoint
    print("\n3. Testing Analytics Endpoint...")
    try:
        response = requests.get(f"{base_url}/candidates/sourced/analytics/overview")
        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics endpoint: OK")
            print(
                f"   Total sourced: {data.get('overview', {}).get('total_sourced', 'N/A')}"
            )
            print(
                f"   Unique tags: {data.get('overview', {}).get('unique_tags', 'N/A')}"
            )
            print(f"   Categories: {len(data.get('sourced_analytics', []))}")
        else:
            print(f"❌ Analytics endpoint: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Analytics endpoint: Error - {e}")

    # Test 4: Check if dashboard.js exists in filesystem
    print("\n4. Checking Dashboard Files...")
    dashboard_js = Path("dashboard/dashboard.js")
    if dashboard_js.exists():
        print("✅ dashboard.js file exists")
        print(f"   Size: {dashboard_js.stat().st_size} bytes")
    else:
        print("❌ dashboard.js file not found")

    dashboard_html = Path("dashboard/index.html")
    if dashboard_html.exists():
        print("✅ index.html file exists")
        print(f"   Size: {dashboard_html.stat().st_size} bytes")
    else:
        print("❌ index.html file not found")

    # Test 5: Check for common issues
    print("\n5. Checking for Common Issues...")

    # Check if dashboard.js is referenced correctly in HTML
    if dashboard_html.exists():
        html_content = dashboard_html.read_text()
        if 'src="/dashboard/static/dashboard.js"' in html_content:
            print("✅ JavaScript reference in HTML: Correct")
        else:
            print("❌ JavaScript reference in HTML: Incorrect")
            print('   Expected: src="/dashboard/static/dashboard.js"')

    # Check if Bootstrap is loaded
    if dashboard_html.exists():
        html_content = dashboard_html.read_text()
        if "bootstrap" in html_content.lower():
            print("✅ Bootstrap CSS/JS: Found")
        else:
            print("❌ Bootstrap CSS/JS: Not found")

    # Check if Chart.js is loaded
    if dashboard_html.exists():
        html_content = dashboard_html.read_text()
        if "chart.js" in html_content.lower():
            print("✅ Chart.js: Found")
        else:
            print("❌ Chart.js: Not found")

    print("\n" + "=" * 50)
    print("🎯 Recomendaciones:")
    print("1. Abre http://localhost:8000/dashboard/ en tu navegador")
    print("2. Presiona F12 para abrir las herramientas de desarrollador")
    print("3. Ve a la pestaña 'Console' para ver errores de JavaScript")
    print("4. Ve a la pestaña 'Network' para ver si los archivos se cargan")
    print("5. Si hay errores, compártelos para diagnóstico adicional")


def main():
    """Main function."""
    test_dashboard_endpoints()


if __name__ == "__main__":
    main()

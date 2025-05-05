# Selenium POM Python + Allure

Este proyecto demuestra una estructura básica con Selenium WebDriver usando el patrón Page Object Model (POM) en Python, pruebas con `pytest` y reportes con `Allure`.

## 🚀 Requisitos

- Python 3.8+
- Git Bash o PowerShell en Windows (o terminal en Linux/Mac)
- Java instalado para ejecutar Allure

## 🛠 Instalación

```bash
python -m venv venv
source venv/Scripts/activate    # en Git Bash
pip install -r requirements.txt
```

## ▶️ Ejecutar pruebas
Instalar Allure CLI
Descarga Allure para eso:

Ve a: https://github.com/allure-framework/allure2/releases

Descarga la última versión (allure-X.Y.Z.zip)

Extrae el .zip en una carpeta, por ejemplo: C:\Allure

Agrega la ruta C:\Allure\bin a tu variable de entorno PATH:

Entra a Configuración del sistema → Variables de entorno → PATH

Haz clic en Editar → Nuevo → y pega: C:\Allure\bin

Reinicia tu terminal o IDE para que tome los cambios.

```bash
 pytest --browser=chrome --alluredir=allure-results  
```
## 📊Generar reporte 
 allure generate allure-results --clean -o allure-report

## 📊 Ver reportes Allure

```bash
allure open allure-report
allure serve reports
```

## 📁 Estructura

```
.
├── conftest.py
├── requirements.txt
├── pages/
│   └── google_page.py
├── tests/
│   └── test_google_search.py
└── utils/
    └── browser_factory.py
```

## 🧱 Buenas prácticas

- POM para separar lógica de navegación
- Fixtures reutilizables
- Soporte para múltiples navegadores Nota: firefox no estable aún
- Reportes profesionales con Allure

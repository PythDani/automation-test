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

```bash
pytest tests/test_google_search.py --browser=chrome --alluredir=reports
```

## 📊 Ver reportes Allure

```bash
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
- Soporte para múltiples navegadores
- Reportes profesionales con Allure

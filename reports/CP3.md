# Отчет CP3: Конфигурация ИС и выбор техники + Git/роли

## 1. Конфигурация и требования

| Компонент | Требование | Обоснование |
| :--- | :--- | :--- |
| **ОС** | Linux (Termux) / Windows | Кросс-платформенность Python. |
| **Python** | 3.11+ | Поддержка современных подсказок типов (Type Hints). |
| **Зависимости** | Flask, requests | Легковесный сервер и простой HTTP-клиент. |
| **GUI** | Tkinter | Встроен в Python, не требует сложной установки. |

## 2. Политика ветвления

В проекте используется упрощенный **Git Flow**:
1.  **Ветка `main`**: Содержит только стабильный код.
2.  **Feature-ветки**: Разработка ведется локально, фиксация по этапам (КП).

## 3. Сценарий “первого запуска”

```bash
# 1. Клонирование
git clone [https://github.com/GalaxyTail/college-library-Bagdaev.git](https://github.com/GalaxyTail/college-library-Bagdaev.git)
cd college-library-Bagdaev

# 2. Настройка
pip install -r requirements.txt
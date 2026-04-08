# 🇺🇦 Ukrainian SCMDB Translation - Quick Start Guide

## 📋 Що це?

Цей набір скриптів автоматизує створення української локалізації для [SCMDB](https://scmdb.dev) — Star Citizen Mission & Data Browser.

## 🚀 Швидкий старт

### 1. Запустіть автоматичне оновлення

```bash
# Для LIVE версії
python auto_update_translation.py

# Для PTU версії
python auto_update_translation.py --ptu
```

**Результат:** Створиться файл `lang-global_ua_fixed-*.json` готовий для використання в SCMDB.

### 2. Опублікуйте файл

**Варіант A: GitHub (рекомендовано)**
```bash
# Створіть репозиторій на GitHub
git init
git add lang-global_ua_fixed-*.json
git commit -m "Initial Ukrainian translation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scmdb-ukrainian.git
git push -u origin main
```

**Варіант B: GitHub Gist**
1. Завантажте файл на https://gist.github.com
2. Скопіюйте Raw URL

### 3. Використовуйте в SCMDB

Відкрийте в браузері:
```
https://scmdb.dev?lang=https://raw.githubusercontent.com/YOUR_USERNAME/scmdb-ukrainian/main/lang-global_ua_fixed-4.7.0-ptu.11506930.json
```

Налаштування збережеться в браузері!

## 📁 Файли та скрипти

### 🎯 Основні скрипти

| Скрипт | Опис | Використання |
|--------|------|--------------|
| `auto_update_translation.py` | Головний скрипт автоматизації | `python auto_update_translation.py` |
| `fix_encoding.py` | Виправлення кодування | `python fix_encoding.py input.ini output.ini` |
| `build_lang_template.py` | Створення JSON з INI (від SCMDB) | `python build_lang_template.py --translate file.ini` |

### 📄 Робочі файли

| Файл | Опис |
|------|------|
| `global_ua_fixed.ini` | Виправлена версія вашого global.ini |
| `lang-global_ua_fixed-*.json` | Готовий файл локалізації для SCMDB |
| `lang-template-*.json` | Шаблон від SCMDB (оновлюється з репозиторію) |

## 🔧 Команди автоматизації

### Базове використання
```bash
# LIVE версія
python auto_update_translation.py

# PTU версія
python auto_update_translation.py --ptu
```

### Розширені опції
```bash
# Вказати шлях до global.ini
python auto_update_translation.py --global-ini "C:\path\to\global.ini"

# Вказати папку для виводу
python auto_update_translation.py --output-dir "C:\output"

# Не оновлювати репозиторій SCMDB_LANG
python auto_update_translation.py --no-update

# З комітом в git
python auto_update_translation.py --commit

# З комітом та пушем в git
python auto_update_translation.py --commit --push
```

## 📊 Розуміння результатів

Після запуску ви побачите звіт:

```
=== Result ===
  File:          lang-global_ua_fixed-4.7.0-ptu.11506930.json
  Total:         3359          # Всього записів
  Translated:    3024 (90%)    # Перекладено українською
  Missing:       189 (5.6%)    # Відсутні (використовується англійська)
  Substituted:   154           # Автозаміна токенів ([RANK], [LOCATION], etc.)
```

### Це нормально ✅

- **Missing**: Нові місії/предмети, яких ще немає в вашому global.ini
- **Substituted**: Автоматична заміна плейсхолдерів (наприклад, [RANK] → "Сержант")

## 🔄 Регулярне оновлення

Коли виходить новий патч Star Citizen:

1. **Оновіть гру** (отримаєте новий global.ini)
2. **Запустіть скрипт**:
   ```bash
   python auto_update_translation.py --commit --push
   ```
3. **Готово!** Файл автоматично опублікується

## 🛠️ Налаштування шляхів

Якщо ваші файли в іншому місці, відредагуйте `auto_update_translation.py`:

```python
# Знайдіть ці рядки в файлі:
DEFAULT_SC_INI_LIVE = Path("F:/Games/StarCitizen/LIVE/Data/Localization/korean_(south_korea)/global.ini")
DEFAULT_SC_INI_PTU = Path("F:/Games/StarCitizen/PTU/Data/Localization/korean_(south_korea)/global.ini")

# Змініть на ваші шляхи:
DEFAULT_SC_INI_LIVE = Path("C:/Games/StarCitizen/LIVE/Data/Localization/ukrainian/global.ini")
```

## 🐛 Виправлення проблем

### Проблема: Python не знайдено

**Рішення:**
```bash
# Встановіть Python 3.10+ з https://python.org
# Або використайте повний шлях:
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe auto_update_translation.py
```

### Проблема: global.ini не знайдено

**Рішення:**
```bash
# Знайдіть ваш файл global.ini:
python auto_update_translation.py --global-ini "C:\path\to\your\global.ini"
```

### Проблема: Git не працює

**Рішення:**
1. Встановіть Git з https://git-scm.com
2. Не використовуйте `--commit` та `--push` флаги
3. Завантажте файл вручну на GitHub/Gist

## 📈 Покриття локалізації

Орієнтовно 3,359 записів на версію:

| Категорія | Кількість | Приклади |
|-----------|-----------|----------|
| Місії | ~685 | Контракти, завдання |
| Описи | ~724 | Тексти місій |
| Локації | ~626 | Планети, станції |
| Кораблі | ~144 | Назви кораблів |
| Предмети | ~1,033 | Зброя, броня, обладнання |
| Фракції | ~35 | Організації |
| Репутація | ~55 | Звання та рівні |

## 🔢 Статистика української локалізації

**Поточний статус:**
- ✅ Перекладено: ~90% (3,024 записів)
- ⚠️ Відсутні: ~6% (189 записів)
- 🔄 Автотокени: 154 замін

## 🤝 Допомога та внесок

Щоб покращити переклад:

1. **Додайте відсутні ключі** в ваш global.ini
2. **Покращіть існуючі переклади**
3. **Перезапустіть скрипт**: `python auto_update_translation.py`
4. **Опублікуйте оновлення**

## 📞 Корисні посилання

- **SCMDB**: https://scmdb.dev
- **SCMDB_LANG Repository**: https://github.com/KrovaxCode/SCMDB_LANG
- **Star Citizen**: https://robertsspaceindustries.com

## 📝 Ліцензія

Інструменти локалізації надаються як є. Дані гри Star Citizen належать Cloud Imperium Games.

---

**Створено з ❤️ для української спільноти Star Citizen**

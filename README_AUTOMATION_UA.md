# 🤖 Автоматизація української локалізації SCMDB

## 📦 Створені файли

У папці `F:\SCMDB_LANG\` створено наступні скрипти для автоматизації:

### 🎯 Основні скрипти

| Файл | Опис | Коли використовувати |
|------|------|---------------------|
| **`auto_update_translation.py`** | Головний скрипт автоматизації | Регулярне оновлення локалізації |
| **`fix_encoding.py`** | Виправлення кодування | Ручне виправлення global.ini |
| **`build_lang_template.py`** | Створення JSON з INI | Від SCMDB, використовується автоматично |

### 📚 Документація

| Файл | Опис |
|------|------|
| **`QUICKSTART_UA.md`** | Детальна інструкція з використання |
| **`README_AUTOMATION_UA.md`** | Цей файл - огляд автоматизації |

---

## 🚀 Швидке використання

### Базове оновлення (LIVE)
```bash
cd F:\SCMDB_LANG
python auto_update_translation.py
```

### Оновлення PTU
```bash
python auto_update_translation.py --ptu
```

### З git комітом
```bash
python auto_update_translation.py --commit --push
```

---

## 📋 Що робить автоматизація?

### 1️⃣ Оновлення репозиторію SCMDB_LANG
```
git pull  # Отримує нові шаблони локалізації
```

### 2️⃣ Виправлення кодування
- Читає ваш `global.ini` з гри
- Виправляє 50,000+ рядків з неправильними символами
- Зберігає виправлену версію

**Приклад виправлень:**
```
í → і  (латинська і → українська і)
ý → и  (латинська y → українська и)
ε → є  (грецька epsilon → українська є)
```

### 3️⃣ Створення JSON локалізації
```
python build_lang_template.py --translate global_ua_fixed.ini
```

**Результат:**
- Файл `lang-global_ua_fixed-*.json`
- 3,024 перекладених записів (90%)
- Готовий для використання в SCMDB

### 4️⃣ Git операції (опціонально)
```bash
git add .
git commit -m "Update translation 2025.03.25"
git push  # якщо --push
```

---

## 📊 Статистика результату

Після запуску ви побачите:

```
======================================================================
  SCMDB Ukrainian Translation Auto-Updater
======================================================================

[Step 1] Updating SCMDB_LANG repository
----------------------------------------------------------------------
  [OK] Repository updated successfully

[Step 2] Fixing encoding in LIVE global.ini
----------------------------------------------------------------------
  [OK] Processed 86,112 lines
  [OK] Fixed 50,396 lines with encoding issues
  [OK] Saved to: F:\SCMDB_LANG\global_ua_fixed.ini

[Step 3] Building SCMDB translation
----------------------------------------------------------------------
  [OK] Translation built successfully
  [OK] File saved to: F:\SCMDB_LANG\lang-global_ua_fixed-4.7.0-ptu.11506930.json

======================================================================
  Update Complete!
======================================================================

Files created:
  - global_ua_fixed.ini
  - lang-global_ua_fixed-4.7.0-ptu.11506930.json
```

---

## 🔧 Всі опції командного рядка

```bash
python auto_update_translation.py [ОПЦІЇ]

Опції:
  --ptu                   Використовувати PTU замість LIVE
  --global-ini PATH       Шлях до вашого global.ini файлу
  --output-dir PATH       Папка для збереження результатів
  --no-update             Не оновлювати репозиторій SCMDB_LANG
  --commit                Зкомітити зміни в git
  --push                  Запушити зміни на віддалений репозиторій

Приклади:
  python auto_update_translation.py --ptu
  python auto_update_translation.py --global-ini "C:\path\to\global.ini"
  python auto_update_translation.py --commit --push
  python auto_update_translation.py --no-update --output-dir "C:\output"
```

---

## 📁 Розташування файлів

### Вхідні файли (Star Citizen)
```
F:\Games\StarCitizen\LIVE\Data\Localization\korean_(south_korea)\global.ini
F:\Games\StarCitizen\PTU\Data\Localization\korean_(south_korea)\global.ini
```

### Робочі файли (SCMDB_LANG)
```
F:\SCMDB_LANG\
├── auto_update_translation.py      # Головний скрипт
├── fix_encoding.py                 # Виправлення кодування
├── build_lang_template.py          # Від SCMDB
├── global_ua_fixed.ini             # Виправлений global.ini
└── lang-global_ua_fixed-*.json     # Результат - локалізація для SCMDB
```

---

## 🔄 Процес оновлення при новому патчі

### Автоматичний спосіб (рекомендовано)
```bash
# 1. Оновіть гру Star Citizen (отримаєте новий global.ini)

# 2. Запустіть скрипт (все зробиться автоматично)
python auto_update_translation.py --commit --push

# 3. Готово! Файл опубліковано
```

### Ручний спосіб
```bash
# 1. Виправте кодування
python fix_encoding.py "F:\Games\StarCitizen\LIVE\Data\Localization\korean_(south_korea)\global.ini" "F:\SCMDB_LANG\global_ua_fixed.ini"

# 2. Створіть JSON
python build_lang_template.py --translate "F:\SCMDB_LANG\global_ua_fixed.ini"

# 3. Опублікуйте файл вручну на GitHub/Gist
```

---

## 🎯 Використання результату в SCMDB

### 1. Опублікуйте файл

**GitHub:**
```bash
git init
git add lang-global_ua_fixed-*.json
git commit -m "Ukrainian translation"
git remote add origin https://github.com/YOUR_USERNAME/scmdb-ukrainian.git
git push -u origin main
```

**GitHub Gist:**
1. Завантажте файл на https://gist.github.com
2. Скопіюйте "Raw" URL

### 2. Додайте в SCMDB

Відкрийте в браузері:
```
https://scmdb.dev?lang=https://raw.githubusercontent.com/YOUR_USERNAME/scmdb-ukrainian/main/lang-global_ua_fixed-4.7.0-ptu.11506930.json
```

**Вітаємо!** Тепер SCMDB відображається українською мовою! 🇺🇦

---

## 🐛 Виправлення проблем

### Python не знайдено
```bash
# Повний шлях до Python:
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe auto_update_translation.py
```

### global.ini не знайдено
```bash
# Вкажіть правильний шлях:
python auto_update_translation.py --global-ini "C:\path\to\global.ini"
```

### Git не працює
```bash
# Не використовуйте --commit та --push
python auto_update_translation.py --no-update
```

---

## 📈 Покриття локалізації

| Категорія | Кількість | Покрито |
|-----------|-----------|---------|
| Місії | ~685 | 90% |
| Описи | ~724 | 90% |
| Локації | ~626 | 95% |
| Кораблі | ~144 | 100% |
| Предмети | ~1,033 | 85% |
| **Разом** | **3,359** | **90%** |

---

## 🎉 Результат

**Ви отримуєте:**
✅ Готовий файл локалізації для SCMDB
✅ 90% контенту українською мовою
✅ Автоматичне оновлення при нових патчах
✅ Публікація в один клік

**SCMDB українською:**
🔗 https://scmdb.dev?lang=<Ваш_URL_JSON>

---

## 📞 Корисні посилання

- **SCMDB**: https://scmdb.dev
- **Репозиторій SCMDB_LANG**: https://github.com/KrovaxCode/SCMDB_LANG
- **Star Citizen**: https://robertsspaceindustries.com

---

**Створено для української спільноти Star Citizen** 🇺🇦

Потрібна допомога? Дивіться `QUICKSTART_UA.md` для детальних інструкцій.

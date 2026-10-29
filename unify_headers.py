import os
import re
from pathlib import Path

# Единый шаблон шапки (как на главной)
HEADER_TEMPLATE = '''<header>
  <div class="container header-inner">
    <a href="/" class="logo">
      <img src="/logo-mark.svg" alt="РеабМаршрут" style="width:32px;height:32px;">
      РеабМаршрут
    </a>
    <nav class="nav-links">
      <a href="#route">Определить этап</a>
      <a href="/centers/">Центры</a>
      <a href="/medications/">Лекарства</a>
      <a href="#articles">Статьи</a>
    </nav>
  </div>
</header>'''

# Список страниц для обработки (все подпапки с index.html)
PAGES = [
    'centers/index.html',
    'oms-rehabilitation/index.html',
    'tsr/index.html',
    'care/index.html',
    'mse/index.html',
    'home-rehab/index.html',
    'recovery-stages/index.html',
    'medications/index.html',
    'privacy/index.html',
]

def unify_header(file_path):
    """Заменяет header в файле на унифицированный шаблон."""
    path = Path(file_path)
    
    if not path.exists():
        print(f"⚠️  Не найден файл: {file_path}")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Создаём бэкап
    backup_path = path.with_suffix('.html.bak')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Ищем и заменяем header (regex с флагом re.DOTALL для многострочного поиска)
    pattern = r'<header[^>]*>.*?</header>'
    new_content = re.sub(pattern, HEADER_TEMPLATE, content, flags=re.DOTALL)
    
    # Если header не найден — добавляем после <body>
    if new_content == content:
        print(f"⚠️  Header не найден в {file_path}, добавляю после <body>")
        new_content = content.replace('<body>', f'<body>\n{HEADER_TEMPLATE}', 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Обновлён header: {file_path}")
    return True


def main():
    base_dir = Path(__file__).parent
    print(f"🔧 База: {base_dir}\n")
    
    updated = 0
    skipped = 0
    errors = 0
    
    for page in PAGES:
        full_path = base_dir / page
        try:
            if unify_header(str(full_path)):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"❌ Ошибка в {page}: {e}")
            errors += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Итого: обновлено {updated}, пропущено {skipped}, ошибок {errors}")
    print(f"💾 Бэкапы сохранены как .html.bak")


if __name__ == '__main__':
    main()
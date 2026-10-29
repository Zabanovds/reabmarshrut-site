import os
import re
from pathlib import Path

# Единый шаблон шапки с inline-стилями (гарантированно работает везде)
HEADER_TEMPLATE = '''<header style="background:#fff;border-bottom:1px solid #e2e8f0;padding:16px 0;position:sticky;top:0;z-index:100;">
  <div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <a href="/" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#0E7C6B;font-size:1.5rem;font-weight:800;">
      <img src="/logo-mark.svg" alt="РеабМаршрут" style="width:32px;height:32px;">
      РеабМаршрут
    </a>
    <nav style="display:flex;gap:24px;flex-wrap:wrap;">
      <a href="/#route" style="color:#2d3748;text-decoration:none;font-weight:500;font-size:0.95rem;">Определить этап</a>
      <a href="/centers/" style="color:#2d3748;text-decoration:none;font-weight:500;font-size:0.95rem;">Центры</a>
      <a href="/medications/" style="color:#2d3748;text-decoration:none;font-weight:500;font-size:0.95rem;">Лекарства</a>
      <a href="/#articles" style="color:#2d3748;text-decoration:none;font-weight:500;font-size:0.95rem;">Статьи</a>
    </nav>
  </div>
</header>'''

# Список всех внутренних страниц (главную пропускаем — она уже правильная)
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

def fix_header(file_path):
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
    # Ищем от <header до </header>, включая атрибуты и содержимое
    pattern = r'<header[^>]*>.*?</header>'
    new_content = re.sub(pattern, HEADER_TEMPLATE, content, flags=re.DOTALL, count=1)
    
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
    print("=" * 60)
    print("🎯 Унификация шапок на всех страницах сайта")
    print("=" * 60)
    print()
    
    updated = 0
    skipped = 0
    errors = 0
    
    for page in PAGES:
        full_path = base_dir / page
        try:
            if fix_header(str(full_path)):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f" Ошибка в {page}: {e}")
            errors += 1
    
    print()
    print("=" * 60)
    print(f"📊 ИТОГО:")
    print(f"   ✅ Обновлено: {updated}")
    print(f"   ⚠️  Пропущено: {skipped}")
    print(f"   ❌ Ошибок: {errors}")
    print(f"   💾 Бэкапы сохранены как .html.bak")
    print("=" * 60)
    print()
    print("🚀 Теперь выполни:")
    print("   git add .")
    print('   git commit -m "fix: unify header layout across all pages"')
    print("   git push")


if __name__ == '__main__':
    main()
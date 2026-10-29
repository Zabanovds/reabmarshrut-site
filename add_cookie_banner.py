import os

CSS = """
/* Cookie banner */
.cookie-banner {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #1a202c;
  color: #fff;
  padding: 16px 24px;
  z-index: 9999;
  box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.cookie-banner .cookie-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.cookie-banner p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  color: #e2e8f0;
  flex: 1;
  min-width: 280px;
}
.cookie-banner a {
  color: #4fd1c5;
  text-decoration: underline;
}
.cookie-banner a:hover {
  color: #81e6d9;
}
.cookie-btn {
  background: #0E7C6B;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}
.cookie-btn:hover {
  background: #0A5C4F;
}
@media (max-width: 640px) {
  .cookie-banner .cookie-inner {
    flex-direction: column;
    align-items: stretch;
  }
  .cookie-btn {
    align-self: flex-end;
  }
}
"""

HTML_JS = """
<!-- Cookie banner -->
<div id="cookie-banner" class="cookie-banner">
  <div class="cookie-inner">
    <p>🍪 Мы используем файлы cookie и сервис Яндекс.Метрика для улучшения работы сайта. Продолжая использовать сайт, вы соглашаетесь с <a href="/privacy/">Политикой конфиденциальности</a>.</p>
    <button class="cookie-btn" onclick="acceptCookies()">Принять</button>
  </div>
</div>

<script>
// Cookie banner
function acceptCookies() {
  localStorage.setItem('cookiesAccepted', 'true');
  document.getElementById('cookie-banner').style.display = 'none';
}
if (!localStorage.getItem('cookiesAccepted')) {
  document.getElementById('cookie-banner').style.display = 'block';
}
</script>
"""

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

for page in PAGES:
    path = os.path.join(os.path.dirname(__file__), page)
    if not os.path.exists(path):
        print(f" Не найден: {page}")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, нет ли уже баннера
    if 'cookie-banner' in content:
        print(f" Уже есть баннер: {page}")
        continue
    
    # Вставляем CSS перед </head>
    content = content.replace('</head>', f'<style>{CSS}</style>\n</head>')
    
    # Вставляем HTML+JS перед </body>
    content = content.replace('</body>', f'{HTML_JS}\n</body>')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Добавлен баннер: {page}")

print("\nГотово!")
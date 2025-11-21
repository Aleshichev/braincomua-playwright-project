# Brain.com.ua Parser

Web scraper for collecting product information from brain.com.ua using Playwright and Django ORM.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
poetry install

# Install browser for Playwright
poetry run playwright install chromium
```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
POSTGRES_DB=your-db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
```

### 3. Start Database

```bash
docker-compose up -d
```

### 4. Django Migrations

```bash
cd braincomua_project
python manage.py migrate
```

### 5. Run Parser

```bash
# From project root
python modules/1_playwright_parser.py
```

## 🔧 Features

- ✅ Search products by name
- ✅ Collect full product information (title, price, photos, specifications)
- ✅ Save to PostgreSQL
- ✅ Export to CSV
- ✅ Playwright anti-detection settings
- ✅ Logging of all operations

## 📊 Collected Data

- Product title
- Price (regular/sale)
- Photos (all)
- Product code
- Review count
- Specifications (processor, memory, screen, etc.)
- Manufacturer, color, memory, screen diagonal

## ⚙️ Configuration

### Browser Mode

```python
# In 1_playwright_parser.py
playwright, browser, context, page = create_browser_and_context(
    headless=False  # True - background mode, False - visible browser
)
```

### Timeouts

```python
# In playwright_config.py
context.set_default_timeout(60000)  # 60 seconds
context.set_default_navigation_timeout(120000)  # 2 minutes
```

## 🐛 Troubleshooting

### Timeout on Loading

```bash
# Check browser installation
poetry run playwright install chromium --force

# Run test script
python modules/test_playwright.py
```

### Django Async Context Error

Close browser **before** saving to database:

```python
product_data = collect_product_data(page)
close_browser(playwright, browser)  # Close first
save_to_database(product_data)      # Then save
```

### \xa0 Character in Data

Add cleanup in `parse_specification_row`:

```python
text = text.replace('\xa0', ' ').strip()
```

## 📝 Dependencies

- Python 3.10+
- Django 5.2.8
- Playwright 1.48.0
- PostgreSQL 15
- pandas 2.3.3

## 👨‍💻 Author

Igor Aleshichev

## 📄 License

MIT

# Digital Menu Service

## Назначение

Сервис предназначен для создания, редактирования и просмотра электронного меню
заведений общественного питания (кафе, ресторанов, баров, кофеен). Приложение
позволяет заменить бумажные меню цифровыми, оперативно обновлять цены и состав
блюд.

## Основные сущности

- **Блюдо (Dish)** — позиция меню: название, категория, цена, наличие и описание.
- **Категория (Category)** — раздел меню.
- **Пользователь (User)** — посетитель или сотрудник заведения.
- **Заказ (Order)** — заказ пользователя, связанный с блюдом.

Один заказ относится к одному блюду и одному пользователю. Отменённый заказ
сохраняется в базе и получает признак `is_cancelled = 1`.

## Структура базы данных (ПР7)

Для хранения данных используется SQLite, файл базы: `data/digital_menu.sqlite`.

| Таблица | Поля | Ключи |
|---|---|---|
| `categories` | `id INTEGER`, `name TEXT` | `id` — PK, `name` — UNIQUE |
| `dishes` | `id INTEGER`, `name TEXT`, `category_id INTEGER`, `price REAL`, `in_stock INTEGER`, `description TEXT` | `id` — PK, `category_id` — FK → `categories.id` |
| `users` | `id INTEGER`, `name TEXT`, `email TEXT` | `id` — PK, `email` — UNIQUE |
| `orders` | `id INTEGER`, `dish_id INTEGER`, `user_id INTEGER`, `quantity INTEGER`, `discount_percent REAL`, `is_cancelled INTEGER` | `id` — PK, `dish_id` — FK → `dishes.id`, `user_id` — FK → `users.id` |

В исходном `categories.json` перечислены не все категории, используемые блюдами.
Скрипт импорта автоматически добавляет недостающие названия категорий в таблицу
`categories`, не изменяя исходные JSON-файлы.

## Организация файлов базы данных

- `sql/schema.sql` — создание таблиц, ограничений и индексов.
- `sql/queries.sql` — 12 примеров SQL-запросов: выборки, фильтрация `WHERE`,
  соединения `JOIN`, агрегирующие функции, группировка `GROUP BY` и `HAVING`.
- `db/database.py` — подключение к SQLite и функции получения данных.
- `db/import_json.py` — перенос данных из исходных JSON-файлов в SQLite.

Исходные JSON-файлы и классы из предыдущих практических сохранены. Они нужны
как исходный формат данных для импорта и как часть ранее выполненной консольной
реализации.

## Практическая работа 9 — Django ORM

Django создаёт таблицы `menu_category`, `menu_dish`, `orders_customer`
и `orders_order` в стандартной базе `db.sqlite3`. Миграции приложений
`menu` и `orders` управляют их схемой. Модель `Customer` хранит
покупателей проекта, а встроенная модель Django используется для входа
в админку. Связи реализованы через `ForeignKey` с `PROTECT`. Обратные
связи доступны через `category.dishes`, `dish.orders`, `customer.orders`.

Команда `import_pr7` читает базу ПР7 в режиме только чтения и переносит
записи в одной транзакции, сохраняя ID и внешние ключи. Команда рассчитана
на однократное заполнение пустых таблиц предметной области. Путь к другой
копии базы можно указать параметром `--source`.

### Запуск

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py import_pr7
python manage.py runserver
```

Выполняйте `import_pr7` только при первом заполнении базы. Если исходной
базы ПР7 нет, создайте её из JSON командой `python -m db.import_json`.

| Страница | Сценарий |
|---|---|
| `/` | Главная страница |
| `/menu/` | Поиск по названию и описанию, фильтры по категории, цене и наличию |
| `/menu/<id>/` | Блюдо и его категория |
| `/orders/` | Поиск по блюду и покупателю, фильтр по статусу, сортировка |
| `/orders/<id>/` | Заказ, связанные блюдо и покупатель, сумма со скидкой |
| `/statistics/` | Сводные показатели и количество блюд по категориям |
| `/admin/` | Создание, редактирование и удаление записей |

Для доступа к админке создайте учётную запись командой
`python manage.py createsuperuser`. Списки меню и заказов показывают по
пять записей на страницу. Ссылки «Назад» и «Вперёд» сохраняют параметры
поиска, фильтрации и сортировки.

### ORM-запросы для демонстрации

| Выражение | Где используется |
|---|---|
| `Order.objects.all()` | Исходный список заказов |
| `Category.objects.order_by("name")` | Категории в фильтре меню |
| `Dish.objects.select_related("category")` | Меню и карточка блюда |
| `get_object_or_404(queryset, pk=dish_id)` | Карточка блюда |
| `filter(category_id=category_id)` | Блюда выбранной категории |
| `filter(price__lte=max_price)` | Блюда до указанной цены |
| `filter(category_id=category_id, price__lte=max_price)` | Совместный фильтр категории и цены |
| `exclude(in_stock=False)` | Доступные блюда |
| `filter(Q(name__iregex=pattern) \| Q(description__iregex=pattern))` | Поиск по названию или описанию |
| `filter(dish__name__iregex=pattern)` | Заказы с указанным блюдом |
| `filter(user__name__iregex=pattern)` | Заказы покупателя |
| `Order.objects.active()` | Активные заказы |
| `order_by("price", "name", "pk")` | Сортировка меню по цене с устойчивым порядком страниц |
| `order_by("dish__name", "id")` | Сортировка заказов по связанному блюду |
| `annotate(dish_name=F("dish__name"), ...).values(...)` | Подготовка сокращённых строк списка заказов |
| `Order.objects.select_related("dish", "user")` | Связанные данные в карточке заказа |
| `Dish.objects.aggregate(...)` | Количество блюд и статистика цен |
| `Order.objects.aggregate(...)` | Сводка по заказам и активным заказам |
| `Category.objects.annotate(dishes_count=Count("dishes"), ...)` | Количество блюд, включая пустые категории |
| `Paginator(queryset, 5).get_page(...)` | Списки блюд и заказов |

Поиск использует экранированный шаблон `iregex`, чтобы в SQLite
сопоставлять кириллицу без учёта регистра и искать введённые символы
буквально. Админка Django предоставляет CRUD. В Django shell те же
операции можно показать на временной категории:

```python
from menu.models import Category
category = Category.objects.create(name="Категория для демонстрации")
category = Category.objects.get(pk=category.pk)
category.name = "Обновлённая категория"
category.save(update_fields=["name"])
assert Category.objects.get(pk=category.pk).name == "Обновлённая категория"
category.delete()
```

Для проверки прямой и обратной связи в shell можно выполнить
`order = Order.objects.select_related("dish", "user").first()`,
`order.dish.category`, `order.user` и `order.user.orders.all()`.

### Проверки

```powershell
python manage.py check
python manage.py showmigrations menu orders
python manage.py makemigrations --check --dry-run
python -m pytest -v
python -m flake8 .
```

Для запуска Flake8 с явным параметром исключения используйте
`--extend-exclude=venv,.venv,migrations,__pycache__,menu_project/settings.py`.
При передаче этого параметра Flake8 использует список из командной строки.

## ПР10 и ПР11

Для обновления существующей базы ПР9 выполните `python manage.py migrate`.
Миграция переносит флаг `is_cancelled` в статусы активного и отменённого
заказа. У записей ПР9 дата предзаказа остаётся пустой. При установке с нуля
после миграций по-прежнему можно выполнить `python manage.py import_pr7`.

- В админке доступны поиск, сортировка, фильтры по статусу и заказам на дату,
  а в карточке покупателя видны его заказы.
- В меню можно выбрать дату предзаказа. Блюда должны быть в наличии, а активный
  заказ уже занимает дату для блюда. Отмена освобождает дату и сохраняет запись.
- Сотрудник после входа в админку может создать, изменить или отменить
  предзаказ через `/orders/`. Список поддерживает фильтры по дате и статусу.
- Карточка блюда открывается по slug и по прежнему числовому URL. Фото можно
  добавить через карточку или админку. Изображения находятся в `media/dishes/`.

Интеграционные сценарии проверяются командой `python manage.py test`.
Для SQL-диагностики перед запуском локального сервера задайте в PowerShell
`$env:DMS_DEBUG_TOOLBAR = "1"` и откройте вкладку SQL на странице заказов.

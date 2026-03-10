# OLX Market - Marketplace Platformasi

OLX.UZ ga o'xshash sodda marketplace backend platformasi. Django REST Framework yordamida qurilgan.

## Texnologiyalar

- **Django 4.2** + **Django REST Framework**
- **PostgreSQL** — ma'lumotlar bazasi
- **Simple JWT** — autentifikatsiya
- **drf-spectacular** — Swagger API hujjatlari
- **django-filter** — filterlash
- **Pillow** — rasm ishlash

## Imkoniyatlar

- Telegram orqali ro'yxatdan o'tish va kirish (JWT)
- Rol tizimi: `customer` va `seller`
- Ierarxik kategoriyalar
- E'lon (mahsulot) yaratish, tahrirlash, nashr etish, arxivlash
- Qidiruv va filterlash (narx, viloyat, kategoriya, holat)
- Sevimlilar ro'yxati
- Buyurtma tizimi (status workflow bilan)
- Fikr va reyting tizimi
- Swagger UI orqali API hujjatlari

## O'rnatish

### 1. Repositoryni clone qilish

```bash
git clone https://github.com/yourusername/olx_market.git
cd olx_market
```

### 2. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlash

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=olx_market
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

TELEGRAM_BOT_TOKEN=your-bot-token
```

### 5. PostgreSQL ma'lumotlar bazasini yaratish

```bash
psql -U postgres
CREATE DATABASE olx_market;
\q
```

### 6. Migratsiyalar

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Superuser yaratish

```bash
python manage.py createsuperuser
```

### 8. Serverni ishga tushirish

```bash
python manage.py runserver
```

## API Hujjatlari

Swagger UI: http://localhost:8000/api/docs/  
ReDoc: http://localhost:8000/api/redoc/  
OpenAPI schema: http://localhost:8000/api/schema/

## API Endpointlar

### Autentifikatsiya
| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/api/v1/auth/telegram-login/` | Telegram orqali login/registratsiya |
| POST | `/api/v1/auth/refresh/` | Token yangilash |
| POST | `/api/v1/auth/logout/` | Chiqish |

### Foydalanuvchi
| Method | URL | Tavsif |
|--------|-----|--------|
| GET/PATCH | `/api/v1/users/me/` | Profil ko'rish/tahrirlash |
| POST | `/api/v1/users/me/upgrade-to-seller/` | Sotuvchiga o'tish |

### Sotuvchilar
| Method | URL | Tavsif |
|--------|-----|--------|
| POST | `/api/v1/sellers/` | Do'kon profili yaratish |
| GET/PATCH | `/api/v1/sellers/me/` | O'z do'konini ko'rish/tahrirlash |
| GET | `/api/v1/sellers/{id}/` | Sotuvchi profili (public) |
| GET | `/api/v1/sellers/{id}/products/` | Sotuvchi mahsulotlari |

### Kategoriyalar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/categories/` | Barcha kategoriyalar |
| GET | `/api/v1/categories/{slug}/` | Bitta kategoriya |
| GET | `/api/v1/categories/{slug}/products/` | Kategoriya mahsulotlari |

### Mahsulotlar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/products/` | Barcha aktiv mahsulotlar |
| POST | `/api/v1/products/` | Yangi e'lon |
| GET/PATCH/DELETE | `/api/v1/products/{id}/` | Bitta mahsulot |
| POST | `/api/v1/products/{id}/publish/` | Nashr etish |
| POST | `/api/v1/products/{id}/archive/` | Arxivlash |
| POST | `/api/v1/products/{id}/sold/` | Sotilgan deb belgilash |

### Sevimlilar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/favorites/` | Sevimlilar ro'yxati |
| POST | `/api/v1/favorites/` | Sevimlilarga qo'shish |
| DELETE | `/api/v1/favorites/{id}/` | O'chirish |

### Buyurtmalar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/orders/` | Buyurtmalar (?role=buyer\|seller) |
| POST | `/api/v1/orders/` | Yangi buyurtma |
| GET/PATCH | `/api/v1/orders/{id}/` | Bitta buyurtma |

### Fikrlar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/reviews/` | Barcha fikrlar (?seller_id=X) |
| POST | `/api/v1/reviews/` | Fikr qoldirish |

## Biznes mantiq

### Foydalanuvchi rollari
- **Customer** — mahsulotlarni ko'rish, sevimlilar, buyurtma, fikr
- **Seller** — customer imkoniyatlari + mahsulot boshqarish, buyurtmalarni boshqarish

### Order status workflow
```
kutilyapti → [sotuvchi] → kelishilgan → [xaridor] → sotib_olingan
kutilyapti → [sotuvchi] → bekor_qilingan
kelishilgan → [xaridor] → bekor_qilingan
```

### Mahsulot status workflow
```
moderatsiyada → [publish] → aktiv
aktiv → [tahrirlash] → moderatsiyada
aktiv → [archive] → arxivlangan
aktiv/arxivlangan → [sold] → sotilgan
```

## Deploy (Production)

```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

python manage.py collectstatic
gunicorn core.wsgi:application
```

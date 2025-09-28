# Alx_DjangoLearnLab
ALX Jango project

## API Endpoints

### Books
- `GET /api/books/` → List all books (public)
- `GET /api/books/<id>/` → Retrieve a single book (public)
- `POST /api/books/create/` → Create a book (authenticated users only)
- `PUT /api/books/<id>/update/` → Update a book (authenticated users only)
- `DELETE /api/books/<id>/delete/` → Delete a book (authenticated users only)

## Filtering, Searching, and Ordering

The `/api/books/` endpoint supports advanced querying:

- **Filter** by fields:
  - `/api/books/?title=1984`
  - `/api/books/?author=1`
  - `/api/books/?publication_year=1949`

- **Search** across title and author:
  - `/api/books/?search=Orwell`

- **Ordering** by title or publication year:
  - `/api/books/?ordering=title`
  - `/api/books/?ordering=-publication_year`

## Testing the API

Tests are located in `api/test_views.py`.

### Run tests
```bash
python manage.py test api
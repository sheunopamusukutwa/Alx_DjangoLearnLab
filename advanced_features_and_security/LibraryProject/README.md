# Permissions & Groups Setup

This app uses Django's groups and permissions to restrict access:

## Permissions
Defined in `Book` model:
- can_view → Allows viewing books
- can_create → Allows adding new books
- can_edit → Allows editing existing books
- can_delete → Allows deleting books

## Groups
Configured in Django Admin:
- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → all permissions

## Enforcement
Views use `@permission_required` decorators to check permissions.
Example: `@permission_required('bookshelf.can_edit')` protects the edit view.

SECURE_SSL_REDIRECT=True forces HTTPS.
HSTS (SECURE_HSTS_*) instructs browsers to always use HTTPS (and allows preloading).
SESSION_COOKIE_SECURE / CSRF_COOKIE_SECURE ensure cookies travel only over HTTPS.
X_FRAME_OPTIONS="DENY" and SECURE_CONTENT_TYPE_NOSNIFF=True harden against clickjacking and MIME sniffing.
Use SECURE_PROXY_SSL_HEADER when Django sits behind a TLS-terminating proxy.
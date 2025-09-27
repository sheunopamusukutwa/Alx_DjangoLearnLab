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
"""Insert data into categories and products

Revision ID: 8d1fdfb32770
Revises: 53b7bf77b655
Create Date: 2025-11-16 21:29:46.197772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d1fdfb32770'
down_revision = '53b7bf77b655'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Визначаємо структуру таблиці (для bulk_insert)
    categories_table = sa.table(
        'categories',
        sa.column('name', sa.String)
    )

    # Вставляємо дані в 'categories'
    op.bulk_insert(categories_table,
        [
            {'name': 'Smartphones'},
            {'name': 'Monitors'},
            {'name': 'Keyboards'}
        ]
    )

    # 2. Визначаємо 'products'
    products_table = sa.table(
        'products',
        sa.column('name', sa.String),
        sa.column('price', sa.Float),
        sa.column('active', sa.Boolean)
        # Ми не вказуємо category_id, created_at, 
        # оскільки ми хочемо, щоб спрацювали server_default
        # (і ми не знаємо ID категорій наперед)
    )
    
    # Вставляємо дані в 'products'
    op.bulk_insert(products_table,
        [
            {'name': 'Samsung Galaxy', 'price': 850.00, 'active': True},
            {'name': 'Dell Monitor', 'price': 300.00, 'active': True},
            {'name': 'Logitech MX Keys', 'price': 120.00, 'active': True},
        ]
    )


def downgrade():
    # Видаляємо дані у зворотному порядку
    
    # Складніше видалити конкретні дані, не зачепивши існуючі,
    # тому часто в data-migration downgrade залишають порожнім
    # або видаляють за назвою.
    op.execute("DELETE FROM products WHERE name IN ('Samsung Galaxy', 'Dell Monitor', 'Logitech MX Keys')")
    op.execute("DELETE FROM categories WHERE name IN ('Smartphones', 'Monitors', 'Keyboards')")


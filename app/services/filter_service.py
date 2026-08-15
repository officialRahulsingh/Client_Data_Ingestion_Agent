from datetime import date
from sqlalchemy import Select, and_, select
from sqlalchemy.orm import Session
from app.models.client import Client


FILTERABLE_TEXT_FIELDS = {
    "client_code": Client.client_code,
    "client_name": Client.client_name,
    "email": Client.email,
    "phone": Client.phone,
    "city": Client.city,
    "state": Client.state,
    "status": Client.status,
}


def build_client_filter_query(
    *,
    city: str | None = None,
    state: str | None = None,
    status: str | None = None,
    client_name: str | None = None,
    email: str | None = None,
    client_code: str | None = None,
    min_revenue: float | None = None,
    max_revenue: float | None = None,
    created_from: date | None = None,
    created_to: date | None = None,
) -> Select:
    conditions = []

    values = {
        "city": city,
        "state": state,
        "status": status,
        "client_name": client_name,
        "email": email,
        "client_code": client_code,
    }

    for field_name, value in values.items():
        if value:
            conditions.append(FILTERABLE_TEXT_FIELDS[field_name].ilike(f"%{value}%"))

    if min_revenue is not None:
        conditions.append(Client.revenue >= min_revenue)
    if max_revenue is not None:
        conditions.append(Client.revenue <= max_revenue)
    if created_from is not None:
        conditions.append(Client.created_date >= created_from)
    if created_to is not None:
        conditions.append(Client.created_date <= created_to)

    query = select(Client).order_by(Client.id)
    if conditions:
        query = query.where(and_(*conditions))

    return query


def fetch_filtered_clients(db: Session, **filters) -> tuple[list[Client], int]:
    query = build_client_filter_query(**filters)
    rows = list(db.scalars(query).all())
    return rows, len(rows)

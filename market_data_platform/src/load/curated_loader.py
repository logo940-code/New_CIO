from sqlalchemy.dialects.postgresql import insert


def upsert_rows(session, model, rows: list[dict], conflict_cols: list[str]) -> None:
    if not rows:
        return
    stmt = insert(model).values(rows)
    update_cols = {c.name: stmt.excluded[c.name] for c in model.__table__.columns if c.name not in {'id', *conflict_cols}}
    stmt = stmt.on_conflict_do_update(index_elements=conflict_cols, set_=update_cols)
    session.execute(stmt)
    session.commit()

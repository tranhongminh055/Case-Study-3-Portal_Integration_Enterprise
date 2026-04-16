from backend.models.position import Position


def list_positions(session):
    return session.query(Position).order_by(Position.id).all()


def get_position(session, position_id):
    return session.query(Position).filter(Position.id == position_id).first()


def create_position(session, payload):
    position = Position(**payload)
    session.add(position)
    session.flush()
    return position


def create_position_mysql(session, payload):
    position = Position(**payload)
    session.add(position)
    session.flush()
    return position


def update_position(session, position, payload):
    for field, value in payload.items():
        setattr(position, field, value)
    session.flush()
    return position


def update_position_mysql(session, position_id, payload):
    position = session.query(Position).filter(Position.id == position_id).first()
    if position is None:
        position = Position(id=position_id, **payload)
        session.add(position)
    else:
        for field, value in payload.items():
            setattr(position, field, value)
    session.flush()
    return position


def delete_position(session, position):
    session.delete(position)
    session.flush()


def delete_position_mysql(session, position_id):
    position = session.query(Position).filter(Position.id == position_id).first()
    if position:
        session.delete(position)
        session.flush()

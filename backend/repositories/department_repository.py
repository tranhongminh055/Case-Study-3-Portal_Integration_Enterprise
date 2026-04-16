from backend.models.department import Department


def list_departments(session):
    return session.query(Department).order_by(Department.id).all()


def get_department(session, department_id):
    return session.query(Department).filter(Department.id == department_id).first()


def create_department(session, payload):
    department = Department(**payload)
    session.add(department)
    session.flush()
    return department


def create_department_mysql(session, payload):
    department = Department(**payload)
    session.add(department)
    session.flush()
    return department


def update_department(session, department, payload):
    for field, value in payload.items():
        setattr(department, field, value)
    session.flush()
    return department


def update_department_mysql(session, department_id, payload):
    department = session.query(Department).filter(Department.id == department_id).first()
    if department is None:
        department = Department(id=department_id, **payload)
        session.add(department)
    else:
        for field, value in payload.items():
            setattr(department, field, value)
    session.flush()
    return department


def delete_department(session, department):
    session.delete(department)
    session.flush()


def delete_department_mysql(session, department_id):
    department = session.query(Department).filter(Department.id == department_id).first()
    if department:
        session.delete(department)
        session.flush()

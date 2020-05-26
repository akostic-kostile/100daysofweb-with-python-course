import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session

from db import db_folder

__engine = None
__factory = None


def global_init(db_name: str):
    global __engine, __factory

    if __factory is not None:
        return

    conn_str = "sqlite:///" + db_folder.get_full_path(db_name)
    __engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sqlalchemy.orm.sessionmaker(bind=__engine)


def create_tables():
    if __engine is None:
        raise Exception("You have not called global_init()")

    import data.__all_models  # noqa: F401
    from data.sqlalchemybase import SqlAlchemyBase

    SqlAlchemyBase.metadata.create_all(__engine)


def create_session() -> sqlalchemy.orm.Session:
    if __factory is None:
        raise Exception("You have not called global_init()")

    session: Session = __factory()
    session.expire_on_commit = False
    return session

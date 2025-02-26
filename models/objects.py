from sqlalchemy.orm import Mapped, mapped_column

from core.postgres.initialization import Base


class ObjectModel(Base):
    __tablename__ = "objects"

    name: Mapped[str] = mapped_column(primary_key=True)
    reports_count: Mapped[int] = mapped_column(default=0)

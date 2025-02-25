from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


class ObjectModel(Base):
    __tablename__ = "objects"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    reports = relationship(
        "ReportModel",
        back_populates="object"
    )

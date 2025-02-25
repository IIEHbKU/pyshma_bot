from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[str] = mapped_column(ForeignKey("objects.id"))
    width: Mapped[int]
    height: Mapped[int]

    predictions = relationship(
        "PredictionsModel",
        back_populates="report"
    )

    object = relationship(
        "ObjectModel",
        back_populates="reports"
    )

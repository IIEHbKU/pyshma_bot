from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.postgres.initialization import Base


class PredictionModel(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[str] = mapped_column(ForeignKey("reports.id"))
    x: Mapped[float]
    y: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]
    confidence: Mapped[float]
    class_id: Mapped[str]

    report = relationship(
        "ReportModel",
        back_populates="predictions"
    )

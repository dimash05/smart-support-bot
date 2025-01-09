from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.faq import FAQEntry  # noqa: E402,F401
from app.models.ticket import Ticket  # noqa: E402,F401
from app.models.user import User  # noqa: E402,F401
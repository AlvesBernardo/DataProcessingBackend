from sqlalchemy.orm import sessionmaker
from modelsv2.subtitle_model import Subtitle


def get_subtitle(language, subtitle):
    subtitle_obj = session.query(Subtitle).filter(
        Subtitle.dtLanguage == language,
        Subtitle.dtSubtitle == subtitle
    ).first()
    return subtitle_obj
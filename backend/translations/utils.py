import datetime
import typing as t
from contextvars import ContextVar

from babel import Locale, dates
from babel.support import LazyProxy, NullTranslations, Translations
from starlette_admin.utils.countries import countries_codes

from conf import settings

translations: t.Dict[str, NullTranslations] = {
    locale: Translations.load(dirname=settings().TRANSLATION_DIR, locales=[locale])
    for locale in settings().TRANSLATION_LOCALES
}

_current_locale: ContextVar[str] = ContextVar(
    "current_locale", default=settings().TRANSLATION_DEFAULT_LOCALE
)
_current_translation: ContextVar[NullTranslations] = ContextVar(
    "current_translation", default=translations[settings().TRANSLATION_DEFAULT_LOCALE]
)


def set_locale(locale: str) -> None:
    _current_locale.set(locale if locale in translations else settings().TRANSLATION_DEFAULT_LOCALE)
    _current_translation.set(translations[get_locale()])


def get_locale() -> str:
    return _current_locale.get()


def gettext(message: str) -> str:
    return _current_translation.get().ugettext(message)


def ngettext(msgid1: str, msgid2: str, n: int) -> str:
    return _current_translation.get().ngettext(msgid1, msgid2, n)


def lazy_gettext(message: str) -> str:
    return LazyProxy(gettext, message, enable_cache=False)  # type: ignore[return-value]


def format_datetime(
        dt: t.Union[datetime.date, datetime.time],
        fmt: t.Optional[str] = None,
        tzinfo: t.Any = None,
) -> str:
    return dates.format_datetime(dt, fmt or "medium", tzinfo, get_locale())


def format_date(date: datetime.date, fmt: t.Optional[str] = None) -> str:
    return dates.format_date(date, fmt or "medium", get_locale())


def format_time(
        time: datetime.time,
        fmt: t.Optional[str] = None,
        tzinfo: t.Any = None,
) -> str:
    return dates.format_time(time, fmt or "medium", tzinfo, get_locale())


def get_countries_list() -> t.List[t.Tuple[str, str]]:
    locale = Locale.parse(get_locale())
    return [(x, locale.territories[x]) for x in countries_codes]


def get_currencies_list() -> t.List[t.Tuple[str, str]]:
    locale = Locale.parse(get_locale())
    return [(str(x), f"{x} - {locale.currencies[x]}") for x in locale.currencies]


def get_locale_display_name(locale: str) -> str:
    return Locale(locale).display_name.capitalize()

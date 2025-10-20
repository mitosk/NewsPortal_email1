from django import template
import re

register = template.Library()

# Список нецензурных слов (для примера)
CENSORED_WORDS = [
    'редиска', 'плохой', 'ужасный', 'отвратительный'
]


@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError(f"Фильтр 'censor' применяется только к строкам, получен: {type(value)}")

    censored_text = value
    for word in CENSORED_WORDS:
        # Ищем слово в любом регистре
        pattern = re.compile(re.escape(word), re.IGNORECASE)

        # Заменяем все буквы кроме первой на *
        def replace_match(match):
            matched_word = match.group()
            if len(matched_word) > 1:
                return matched_word[0] + '*' * (len(matched_word) - 1)
            return matched_word

        censored_text = pattern.sub(replace_match, censored_text)

    return censored_text
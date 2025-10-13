import re

polish = {
    "warning": {
        "Straight rows of keys are easy to guess.": "Sekwencje klawiszy w jednym rzędzie są łatwe do odgadnięcia.",
        "Short keyboard patterns are easy to guess.": "Krótkie wzory klawiaturowe są łatwe do odgadnięcia.",
        "Repeats like \"aaa\" are easy to guess.": "Powtarzające się znaki, np. „aaa”, są łatwe do odgadnięcia.",
        "Repeats like \"abcabcabc\" are only slightly harder to guess than \"abc\".": "Powtarzające się wzorce, np. „abcabcabc”, są prawie tak samo łatwe do odgadnięcia jak „abc”.",
        "Sequences like \"abc\" or \"6543\" are easy to guess.": "Proste sekwencje znaków, np. „abc” lub „6543”, są łatwe do odgadnięcia.",
        "Recent years are easy to guess.": "Ostatnie lata są łatwe do odgadnięcia.",
        "Dates are often easy to guess.": "Daty są często łatwe do odgadnięcia.",
        "This is a top-10 common password.": "To jedno z 10 najczęściej używanych haseł.",
        "This is a top-100 common password.": "To jedno z 100 najczęściej używanych haseł.",
        "This is a very common password.": "To bardzo popularne hasło.",
        "This is similar to a commonly used password.": "To hasło jest podobne do często używanego.",
        "A word by itself is easy to guess.": "Pojedyncze słowa są łatwe do odgadnięcia.",
        "Names and surnames by themselves are easy to guess.": "Same imiona i nazwiska są łatwe do odgadnięcia.",
        "Common names and surnames are easy to guess.": "Popularne imiona i nazwiska są łatwe do odgadnięcia.",
        "This is a very similar password to one commonly used.": "To hasło jest bardzo podobne do często używanego.",
        "Repeats like '123123' are easy to guess.": "Powtarzające się liczby, np. „123123”, są łatwe do odgadnięcia.",
        "Names by themselves are easy to guess.": "Same imiona są łatwe do odgadnięcia.",
        "This is a common password!": "To popularne hasło!",
        "This is similar to a commonly used password!": "To hasło przypomina często używane hasło!"
    },
    "suggestions": {
        "Use a few words, avoid common phrases.": "Używaj kilku słów, unikaj popularnych fraz.",
        "No need for symbols, digits, or uppercase letters.": "Silne hasło nie zawsze wymaga symboli, cyfr ani wielkich liter.",
        "Add another word or two. Uncommon words are better.": "Dodaj jedno lub dwa rzadko spotykane słowa.",
        "Use a longer keyboard pattern with more turns.": "Używaj dłuższych wzorów klawiaturowych ze zmianami kierunku.",
        "Avoid repeated words and characters.": "Unikaj powtarzających się słów i znaków.",
        "Avoid sequences.": "Unikaj przewidywalnych sekwencji znaków.",
        "Avoid recent years.": "Unikaj niedawnych lat lub dat.",
        "Avoid years that are associated with you.": "Unikaj dat związanych z Tobą (np. rok urodzenia).",
        "Avoid dates and years that are associated with you.": "Unikaj dat i lat związanych z Tobą.",
        "Capitalization doesn't help very much.": "Wielkie litery nie zwiększają znacząco siły hasła.",
        "All-uppercase is almost as easy to guess as all-lowercase.": "Samo pisanie wielkimi literami nie zwiększa bezpieczeństwa.",
        "Reversed words aren't much harder to guess.": "Słowa pisane wspak są tylko nieco trudniejsze do odgadnięcia.",
        "Predictable substitutions like '@' instead of 'a' don't help very much.": "Przewidywalne zamiany liter, np. „@” zamiast „a”, niewiele pomagają.",
        "Avoid recent years or dates.": "Unikaj niedawnych dat lub lat.",
        "Avoid common names and surnames.": "Unikaj popularnych imion i nazwisk.",
        "Avoid keyboard patterns.": "Unikaj prostych układów klawiaturowych (np. qwerty).",
        "Use uncommon words.": "Używaj mniej popularnych słów.",
        "Combine random words to create a passphrase.": "Połącz kilka losowych słów, aby utworzyć bezpieczną frazę."
    }
}

time_translations = {
    "second": ["sekunda", "sekundy", "sekund"],
    "minute": ["minuta", "minuty", "minut"],
    "hour": ["godzina", "godziny", "godzin"],
    "day": ["dzień", "dni", "dni"],
    "month": ["miesiąc", "miesiące", "miesięcy"],
    "year": ["rok", "lata", "lat"],
    "century": ["wiek", "wieki", "wieków"]
}


def get_polish_plural(word, number):
    if word not in time_translations:
        return word

    forms = time_translations[word]
    if number == 1:
        return forms[0]
    elif 2 <= number % 10 <= 4 and not (12 <= number % 100 <= 14):
        return forms[1]
    else:
        return forms[2]


def translate_crack_time_string(english_string):
    english_string = english_string.lower().strip()

    if "less than" in english_string:
        return "mniej niż sekunda"

    if english_string == "centuries":
        return "wieki"

    match = re.match(r"(?P<number>\d+)\s(?P<unit>\w+)", english_string)
    if not match:
        return english_string 

    number = int(match.group("number"))
    unit = match.group("unit").rstrip("s")

    plural_form = get_polish_plural(unit, number)
    return f"{number} {plural_form}"

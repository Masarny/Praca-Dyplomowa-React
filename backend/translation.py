import re


polish = {
    "warning": {
        "Straight rows of keys are easy to guess.": "Występujące kolejno po sobie znaki na klawiaturze są łatwe do odgadnięcia.",
        "Short keyboard patterns are easy to guess.": "Krótkie wzory klawiaturowe są łatwe do odgadnięcia.",
        "Repeats like \"aaa\" are easy to guess.": "Powtarzające się znaki, takie jak „aaa”, są łatwe do odgadnięcia.",
        "Repeats like \"abcabcabc\" are only slightly harder to guess than \"abc\".": "Powtarzające się wzorce znaków, takie jak „abcabcabc”, są łatwe do odgadnięcia.",
        "Sequences like \"abc\" or \"6543\" are easy to guess.": "Typowe sekwencje znaków, takie jak „abc” lub „6543”, są łatwe do odgadnięcia.",
        "Recent years are easy to guess.": "Ostatnie lata są łatwe do odgadnięcia",
        "Dates are often easy to guess.": "Daty są łatwe do odgadnięcia.",
        "This is a top-10 common password.": "To jest przesadnie często używane hasło.",
        "This is a top-100 common password.": "To jest bardzo często używane hasło.",
        "This is a very common password.": "To jest często używane hasło.",
        "This is similar to a commonly used password.": "To jest podobne do często używanego hasła.",
        "A word by itself is easy to guess.": "Pojedyncze słowa są łatwe do odgadnięcia.",
        "Names and surnames by themselves are easy to guess.": "Pojedyncze imiona lub nazwiska są łatwe do odgadnięcia.",
        "Common names and surnames are easy to guess.": "Popularne imiona i nazwiska są łatwe do odgadnięcia."
    },
    "suggestions": {
        "Use a few words, avoid common phrases.": "Używaj wielu słów, ale unikaj popularnych fraz.",
        "No need for symbols, digits, or uppercase letters.": "Możesz tworzyć silne hasła bez używania symboli, cyfr lub wielkich liter.",
        "Add another word or two. Uncommon words are better.": "Dodaj więcej słów, które są mniej popularne.",
        "Use a longer keyboard pattern with more turns.": "Używaj dłuższych wzorów klawiaturowych i wielokrotnie zmieniaj kierunek pisania.",
        "Avoid repeated words and characters.": "Unikaj powtarzających się słów i znaków.",
        "Avoid sequences.": "Unikaj typowych sekwencji znaków.",
        "Avoid recent years.": "Unikaj ostatnich lat.",
        "Avoid years that are associated with you.": "Unikaj lat, które są z Tobą powiązane.",
        "Avoid dates and years that are associated with you.": "Unikaj dat i lat, które są z Tobą powiązane.",
        "Capitalization doesn't help very much.": "Wielkie litery nie są zbytnio pomocne.",
        "All-uppercase is almost as easy to guess as all-lowercase.": "Niektóre litery napisz wielkimi literami, lecz nie wszystkie.",
        "Reversed words aren't much harder to guess.": "Unikaj pisowni popularnych słów na wspak.",
        "Predictable substitutions like '@' instead of 'a' don't help very much.": "Unikaj przewidywalnych podstawień liter, takich jak „@” zamiast „a”."
    }
}

time_translations = {
    "second": ["sekunda", "sekundy", "sekund"],
    "minute": ["minuta", "minuty", "minut"],
    "hour":   ["godzina", "godziny", "godzin"],
    "day":    ["dzień", "dni", "dni"],
    "month":  ["miesiąc", "miesiące", "miesięcy"],
    "year":   ["rok", "lata", "lat"],
    "century": ["wiek", "wieki", "wieków"],
}


def get_polish_plural(word, number):
    forms = time_translations[word]
    if number == 1:
        return forms[0]
    elif 2 <= number % 10 <= 4 and not (12 <= number % 100 <= 14):
        return forms[1]
    else:
        return forms[2]


def translate_crack_time_string(english_string):
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

from flask import Blueprint, jsonify, request
from zxcvbn import zxcvbn
import re, math, traceback, random, html


tests_bp = Blueprint("tests_bp", __name__)


try:
    with open("dicts/wordlist_merged_en_pl.txt", "r", encoding="utf-8", errors="ignore") as f:
        COMMON_PATTERNS = set(line.strip().lower() for line in f if line.strip())
except FileNotFoundError:
    COMMON_PATTERNS = set()
    print("Nie znaleziono pliku dicts/wordlist_merged_en_pl.txt.")


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


def uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def translate_msg(m, map_dict):
    if not m:
        return None
    if m in map_dict:
        return map_dict[m]
    low = m.lower()
    for k, v in map_dict.items():
        if k.lower() in low:
            return v
    return m


@tests_bp.route("/test_password", methods=["POST"])
def test_password():
    try:
        data = request.get_json(silent=True) or {}
        password = str(data.get("password", "")).strip()

        if not password:
            return jsonify({"error": "Hasło jest wymagane."}), 400

        if len(password) > 512:
            return jsonify({"error": "Hasło jest zbyt długie (max 512 znaków)."}), 400

        password = "".join(ch for ch in password if ch.isprintable())

        try:
            res = zxcvbn(password)
            z_score = int(res.get("score", 0))
            z_feedback = res.get("feedback", {}) or {}
            z_crack = res.get("crack_times_display", {}).get("offline_slow_hashing_1e4_per_second", "Unknown")
        except Exception as e:
            print("Błąd zxcvbn:", e)
            traceback.print_exc()
            z_score = 0
            z_feedback = {}
            z_crack = "Unknown"

        words = re.findall(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", password)
        word_count = len(words)

        entropy = 0
        if word_count >= 3:
            entropy = math.log2(7776 ** word_count)
            if entropy < 40:
                score = 1
            elif entropy < 60:
                score = 2
            elif entropy < 80:
                score = 3
            else:
                score = 4
            crack_time = f"{round(entropy, 1)} bity entropii"
        else:
            score = z_score
            try:
                crack_time = translate_crack_time_string(z_crack)
            except Exception:
                crack_time = z_crack

        warnings = []
        suggestions = []

        z_warn = z_feedback.get("warning")
        z_sugs = z_feedback.get("suggestions", [])
        for w in (z_warn if isinstance(z_warn, list) else ([z_warn] if z_warn else [])):
            t = translate_msg(w, polish.get("warning", {}))
            if t:
                warnings.append(t)
        for s in z_sugs:
            t = translate_msg(s, polish.get("suggestions", {}))
            if t:
                suggestions.append(t)

        for pat in COMMON_PATTERNS:
            if re.search(rf"\b{re.escape(pat)}\b", password, re.IGNORECASE):
                warnings.append(f"Hasło zawiera popularny wzorzec: '{pat}'.")

        if word_count == 1 and password.lower() in COMMON_PATTERNS:
            warnings.append("Hasło jest pojedynczym, popularnym słowem — bardzo słabe i łatwe do odgadnięcia.")

        if len(set(password)) < len(password) / 2:
            warnings.append("Zbyt wiele powtarzających się znaków — zwiększ różnorodność.")
        if re.search(r"(.)\1{2,}", password):
            warnings.append("Hasło zawiera powtarzające się znaki (np. 'aaa').")
        if re.search(r"(0123|1234|2345|abcd|qwerty)", password.lower()):
            warnings.append("Hasło zawiera prostą sekwencję znaków.")

        if len(password) < 12:
            suggestions.append("Użyj co najmniej 12 znaków — dłuższe hasła są znacznie trudniejsze do złamania.")

        if not re.search(r"[A-ZĄĆĘŁŃÓŚŹŻ]", password):
            suggestions.append("Dodaj wielkie litery.")
        if not re.search(r"\d", password):
            suggestions.append("Dodaj co najmniej jedną cyfrę.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            suggestions.append("Dodaj znaki specjalne (np. @, #, $).")
        if word_count >= 3:
            suggestions.append("Passphrase z kilkoma losowymi słowami to dobry wybór — nie zmieniaj ich kolejności.")
        if word_count > 12:
            warnings.append("Bardzo długie passphrase może być trudne do zapamiętania.")

        if any(x in crack_time for x in ["sekund", "minut", "godzin", "mniej niż"]):
            warnings.append("Hasło można złamać w czasie poniżej doby metodą brute force.")

        if score <= 2:
            labels = ["Bardzo słabe", "Słabe", "Średnie"]
            warnings.append(f"{labels[score]} hasło — nie jest zalecane używanie go.")

        warnings = uniq(warnings) or ["Brak ostrzeżeń."]
        suggestions = uniq(suggestions) or ["Brak sugestii."]
        labels = ["Bardzo słabe", "Słabe", "Średnie", "Silne", "Bardzo silne"]
        score = max(0, min(4, int(score)))

        return jsonify({
            "strength": labels[score],
            "score": score,
            "warnings": warnings,
            "suggestions": suggestions,
            "crack_time": crack_time,
            "entropy_bits": round(entropy, 1) if word_count >= 3 else None,
            "zxcvbn_score": z_score,
            "length": len(password),
            "unique_chars": len(set(password))
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Wewnętrzny błąd serwera podczas analizy hasła."}), 500


@tests_bp.route("/improve_password", methods=["POST"])
def improve_password():
    try:
        data = request.get_json(silent=True) or {}
        password = str(data.get("password", "")).strip()

        if not password:
            return jsonify({"error": "Brak hasła do ulepszenia."}), 400
        if len(password) > 512:
            return jsonify({"error": "Hasło jest zbyt długie (max 512 znaków)."}), 400

        password = html.escape(password)
        specials = ["@", "#", "$", "%", "&", "^", "!", "*", "_", "-", "+", "=", "?"]
        digits = "0123456789"
        words = re.split(r"\s+", password)

        def stylize_word(word):
            if not word:
                return ""
            result = ""
            for i, ch in enumerate(word):
                if ch.isalpha():
                    if i == 0 or random.random() < 0.3:
                        result += ch.upper()
                    else:
                        result += ch.lower()
                else:
                    result += ch
            return result

        styled_words = [stylize_word(w) for w in words]
        separator = random.choice(["_", "-", "@", ""])
        improved_core = separator.join(styled_words)

        prefix = ""
        suffix = ""

        if random.random() < 0.7:
            prefix = random.choice(specials)

        suffix = str(random.randint(1000, 9999)) + random.choice(specials)
        improved_password = f"{prefix}{improved_core}{suffix}"

        if not any(c.isdigit() for c in improved_password):
            improved_password += str(random.randint(1, 99))
        if not re.search(r"[!@#$%^&*()_+\-?]", improved_password):
            improved_password += random.choice(specials)
        if not any(c.isupper() for c in improved_password):
            improved_password = improved_password[0].upper() + improved_password[1:]

        improved_password = re.sub(r"\s+", "_", improved_password)
        return jsonify({"improved_password": improved_password})
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Błąd podczas ulepszania hasła."}), 500

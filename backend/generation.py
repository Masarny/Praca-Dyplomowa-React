from flask import Blueprint, jsonify, request
import string, secrets, random, re, os


generation_bp = Blueprint("generation_bp", __name__)


_dice_cache = None


@generation_bp.route("/generate")
def generate_password():
    try:
        length = int(request.args.get("length", 24))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid length"}), 400
    if length < 4 or length > 256:
        return jsonify({"error": "Length range 4..256"}), 400

    alphabet = string.ascii_letters + string.digits + string.punctuation
    return jsonify({"password": "".join(secrets.choice(alphabet) for _ in range(length))})


@generation_bp.route("/generate_diceware")
def generate_diceware():
    global _dice_cache
    try:
        count = int(request.args.get("count", 5))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid count"}), 400
    if count < 1 or count > 32:
        return jsonify({"error": "Count between 1 and 32"}), 400

    sep_param = (request.args.get("sep") or "space").lower()
    sep_map = {"space":" ", "dash":"-", "underscore":"_", "slash":"/"}

    if sep_param == "random":
        separator = None
    else:
        separator = sep_map.get(sep_param)

    if sep_param != "random" and separator is None:
        return jsonify({"error": "Invalid separator"}), 400

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dice_path = os.path.join(base_dir, "dicts", "dice-directory.txt")

    if _dice_cache is None:
        try:
            with open(dice_path, encoding="utf-8") as f:
                D = {}
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        D[parts[0]] = parts[1]
            if not D:
                return jsonify({"error": "Dictionary file is empty or corrupted"}), 500
            _dice_cache = D
        except FileNotFoundError:
            return jsonify({"error": "Missing dice list file"}), 500
    else:
        D = _dice_cache

    words = []
    for ch in range(count):
        while True:
            key = "".join(str(random.randint(1,6)) for ch in range(5))
            if key in D:
                words.append(D[key])
                break

    if sep_param == "random":
        sep_values = list(sep_map.values())
        password = "".join(
            word + (random.choice(sep_values) if i < len(words) - 1 else "")
            for i, word in enumerate(words)
        )
    else:
        password = separator.join(words)

    return jsonify({"password": password})


@generation_bp.route("/generate_from_phrase", methods=["POST"])
def generate_from_phrase():
    data = request.get_json() or {}
    phrase = data.get("phrase", "").strip()

    if not phrase:
        return jsonify({"error": "Brak zdania wejściowego."}), 400

    phrase = re.sub(r"[<>\"']", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase)

    specials = ["!", "@", "#", "$", "%", "^", "&", "*", "_", "-", "=", "+"]
    separator = random.choice(["@", "#", "$", "%", "&", "_", "-", "=", " "])

    words = phrase.split(" ")

    def smart_case(word):
        result = ""
        for ch in word:
            if ch.isalpha():
                if random.random() < 0.25:
                    result += ch.upper()
                else:
                    result += ch.lower()
            else:
                result += ch
        return result

    password = separator.join(smart_case(w) for w in words)

    prefix = random.choice(specials) if random.random() < 0.7 else ""
    suffix = ""

    if random.random() < 0.9:
        suffix += str(random.randint(10, 9999))
    if random.random() < 0.8:
        suffix += random.choice(specials)

    strong_password = f"{prefix}{password}{suffix}"

    if not any(c.isdigit() for c in strong_password):
        strong_password += str(random.randint(1, 99))
    if not re.search(r"[!@#$%^&*()_+=\-]", strong_password):
        strong_password += random.choice(specials)
    if not any(c.isupper() for c in strong_password):
        chars = list(strong_password)
        for i in range(0, len(chars), max(1, len(chars)//6)):
            if chars[i].isalpha():
                chars[i] = chars[i].upper()
        strong_password = "".join(chars)

    return jsonify({"password": strong_password})

from flask import Blueprint, jsonify


guidelines_bp = Blueprint("guidelines_bp", __name__)


@guidelines_bp.route("/guidelines")
def get_guidelines():
    return jsonify({
        "Cyberbezpieczeństwo": [
            "Cyberbezpieczeństwo to dziedzina nauki zajmująca się bezpieczeństwem systemów komputerowych, sieci, aplikacji oraz danych użytkownika przed atakami, kradzieżą lub uszkodzeniem. "
            "Celem cyberbezpieczeństwa jest zapewnienie poufności, integralności oraz dostępności informacji, czyli tzw. triady CIA (Confidentiality, Integrity, Availability). "
            "W praktyce oznacza to dbanie o to, aby dane użytkownika były bezpieczne, niezmienione i dostępne tylko dla i wyłącznie dla niego. ",

            "Dlaczego cyberbezpieczeństwo jest dla nas ważne? Ponieważ w dzisiejszym świecie niemal wszystko, z czym wchodzimy interakcję - od bankowości, przez komunikację, po zakupy - odbywa się online. "
            "Każde urządzenie podłączone do Internetu może stać się celem ataku, a jego właściciel – ofiarą kradzieży danych, pieniędzy lub tożsamości. "
            "Cyberprzestępcy często wykorzystują nieuwagę, brak wiedzy oraz naiwność zwykłych ludzi, dlatego warto zachować ostrożność w sieci, jak i posiadać odpowiedniom wiedzę. ",

            "Podstawy cyberbezpieczeństwa to m.in.: ",
            "- Stosowanie silnych, unikalnych, ciężkich do odgadnięcia haseł; ",
            "- Weryfikacja dwuetapowa (MFA); ",
            "- Regularna aktualizacja systemu i oprogramowania; ",
            "- Ostrożność przy otwieraniu załączników i linków w e-mailach oraz na stronach internetowych; ",
            "- Korzystanie z bezpiecznych i szyfrowanych sieci Wi-Fi; ",
            "- Korzystanie z oprogramowania antywirusowego oraz antymalware. ",
            "Warto też pamiętać o regularnym tworzeniu kopii zapasowych najważniejszych dla nas danych. Pomoże to odzyskać je w przypadku awarii lub ataku na nie. ",

            "Warto uczyć się cyberbezpieczeństwa, ponieważ świadomość użytkownika jest najlepszą linią obrony przeciwko atakom cyberprzestępców. "
            "Nawet najlepszy antywirus nie ochroni nas, jeżeli użytkownik udostępni swoje dane przestępcy. "
            "I ty możesz zwiększyć swoje bezpieczeństwo w sieci, wystarczy, że będziesz czujny, zaktualizujesz swój system oraz oprogramowanie antywirusowe i nie będziesz ufać zbyt dobrym ofertom w Internecie. "
        ],
        "Bezpieczne Hasła": [
            "Silne hasło to takie, które jest trudne do odgadnięcia przez człowieka i trudne do złamania przez komputer. "
            "Każde silne hasło powinno zawierać: wielkie i małe litery, cyfry oraz znaki specjalne. "
            "Czego nie powinno nigdy podawać w swoim haśle to nasze dane osobiste, takie jak imię, nazwisko, data urodzenia, nazwa ukochanego zwierzaka itp. ",
            "Jedną z najlepszych metod tworzenia haseł jest stworzenie ciągu znaków, który nie ma żadnego sensu językowego i wygląda na oko losowo, np. 'Fr!8xTz#4qR'. ",
            "Inną świetną metodą jest stworzenie hasła z kilku wyrazów, nawet zdania, oddzielając słowa różnymi separatorami, stosując losowo wielkie litery oraz dodając kilka cyfr, np. 'alA-MA555!kOtA369#$'. ",

            "Jak tworzyć bezpieczne hasła? ",
            "- Używaj MINIMUM 12 znaków (im więcej, tym lepiej). ",
            "- Łącz różne typy znaków: litery, cyfry oraz symbole. ",
            "- Unikaj prostych, popularnych wzorców: '12345', 'qwerty', 'abcd'. ",
            "- Nie używaj tego samego hasła w wielu miejscach. ",
            "- Używaj menedżera haseł (takiego jak ta aplikacja), który pozwoli ci przechowywać unikalne i silne hasła bez konieczności ich zapamiętywania. ",
            "Dobrym rozwiązaniem jest też tzw. metoda 'passphrase', czyli hasła z kilku przypadkowych słów lub tworzenie hasła na bazie zdania, które możemy zapamiętać. ",

            "Najczęściej stosowane hasła (TOP 25 – UNIKAJ ZA WSZELKĄ CENĘ!): ",
            "1. 123456 ",
            "2. password ",
            "3. 123456789 ",
            "4. 12345 ",
            "5. 12345678 ",
            "6. qwerty ",
            "7. 111111 ",
            "8. 123123 ",
            "9. abc123 ",
            "10. password1 ",
            "11. 1234 ",
            "12. qwerty123 ",
            "13. 1q2w3e ",
            "14. admin ",
            "15. letmein ",
            "16. welcome ",
            "17. iloveyou" ,
            "18. monkey ",
            "19. football ",
            "20. 000000 ",
            "21. 123321 ",
            "22. 654321 ",
            "23. superman ",
            "24. 1234567 ",
            "25. qazwsx ",

            "Pełna lista najczęściej używanych haseł (aktualizowana corocznie): "
            "https://cybernews.com/best-password-managers/most-common-passwords/. ",
            "Jeśli używasz któregoś z tych haseł, to natychmiast je zmień! " 
            "Pamiętaj również, że zawsze warto odświeżyć hasłą do ważnych dla nas kont co kilka. "
        ],
        "Uwierzytelnianie": [
            "Uwierzytelnianie (z ang. authentication) to proces potwierdzania tożsamości użytkownika, czyli upewnienia się, że osoba próbująca uzyskać dostęp do systemu "
            "jest naprawdę tym, za kogo się podaje. Jest to podstawowy element każdego systemu bezpieczeństwa informatycznego. "
            "Bez uwierzytelniania każdy mógłby podszyć się pod dowolnego użytkownika i uzyskać dostęp do jego danych, kont oraz systemów. ",

            "Najczęściej spotykane formy uwierzytelniania to: ",
            "- Coś, co wiesz – np. hasło lub PIN. ",
            "- Coś, co masz – np. telefon, karta, token sprzętowy. ",
            "- Coś, kim jesteś – np. odcisk palca lub rozpoznawanie twarzy. ",
            "Nowoczesne aplikacje coraz częściej łączą te trzy elementy, zwiększając tym samym bezpieczeństwo logowania. ",

            "W praktyce, najlepszym rozwiązaniem jest uwierzytelnianie wieloskładnikowe (MFA), które łączy w sobie kilka metod uwierzytelniania jednocześnie. "
            "Na przykład: wpisujemy hasło (pierwszy składnik), a następnie potwierdzamy nasze logowanie kodem dostarczonym na nasz e-mail lub SMS-em (drugi składnik). "
            "Niektóre firmy oferują też logowanie z potwierdzeniem w aplikacji mobilnej bez konieczności wpisywania kodu (np. banki). ",

            "Dlaczego jest to ważne dla użytkownika? Jeżeli przestępca pozna twoje hasło, to bez drugiego składnika uwierzytelniania nie dua mu się uzyskać dostępu do twojego konta. "
            "MFA jest w ten sposób jednym z najskuteczniejszych sposobów ochrony konta oraz danych użytkownika przed włamaniem i kradzieżą. ",

            "Uważaj zawsze na fałszywe strony logowania oraz pamiętaj, aby nie podawać kodów (drugiego skłądnika) innym osobom. Są to najczęstsze sposoby na utratę naszego konta. "
            "Jeśli dostaniesz powiadomienie o próbie logowania, której nie rozpoznajesz, natychmiast zmień swoje hasło i zgłoś to do obsługi serwisu. "
        ],
        "Ataki na Użytkowników": [
            "Ataki na użytkowników w Internecie to bardzo duży problem w obecnym społeczeństwie. Wykorzystują one naszą nieuwagę, zaufanie lub brak wiedzy na tematy techniczne. "
            "Najlepszym mechanizmem na obronę przeciwko nim to zrozumienie, jak działają. "
            "Pamiętaj również, że cyberprzestępcy nie zawsze atakują, wykorzystując technologię, bardzo często korzystają z manipulacji, dobroci i strachu człowieka. ",

            "1. Phishing -> jest to oszustwo polegające na podszywaniu się przestępcy pod znane instytucje np. banki, pocztę, sklep internetowy. "
            "Ofiara ataku dostaje e-mail lub SMS z linkiem prowadzącym do fałszywej strony, gdzie podaje swoje dane logowania lub kartę płatniczą. ",
            "- Jak się bronić: nigdy nie klikaj w podejrzane linki, sprawdzaj adres strony, korzystaj z narzędzi dom sprawdzania linków oraz używaj tylko oficjalnych aplikacji. "
            "Zawsze zwracaj uwagę, czy adresy stron zaczyna się od 'https://' i czy domena (nazwa strony) jest poprawna (np. 'bank.com', a nie 'bank_secure_notscam.com'). ",

            "2. Malware –> jest to złośliwe oprogramowanie (np. wirusy, trojany, ransomware), które jest wykorzystywane przez przestępcę do kradzieży naszych danych lub blokowania komputera. ",
            "- Jak się bronić: regularnie aktualizuj swój system, używaj oprogramowania antywirusowego oraz antymalware, nie pobieraj żadnych plików z nieznanych źródeł. "
            "Jak najwięcej unikaj pirackiego oraz nieoficjalnego oprogramowania - często zawierają one złośliwy kod i są najczęstszą przyczyną zainfekowania malware. ",

            "3. Ataki socjotechniczne –> polegają na manipulacji człowiekiem, aby sam przekazał poufne informacje. Często przestępca podaje się za znane nam osoby lub pracowników korzystanych przez nas firm. ",
            "- Jak się bronić: nigdy nie udostępniaj nikomu swoich haseł, kodów oraz danych osobistych przez telefon lub e-mail. "
            "Przestępcy często podszywają się pod pracowników banku, policję lub firmę kurierską, staraj się zawsze jak najbardziej weryfikować takie rozmowy. ",

            "4. Keyloggery i kradzież danych logowania –> są to oprogramowanie rejestrujące każde naciśnięcie klawisza użytkownika. ",
            "- Jak się bronić: używaj menedżera haseł i uwierzytelniania dwustopniowego (MFA). "
            "Unikaj logowania się na niezaufanych komputerach oraz przy pomocy nie twojego sprzętu np. w kafejkach lub bibliotekach. ",

            "5. Ataki na Wi-Fi publiczne –> przestępcy mogą podsłuchiwać ruch w otwartych, niezabezpieczonych sieciach. ",
            "- Jak się bronić: unikaj korzystania z sieci publicznych oraz logowania się w nich. Dodatkowo zalecane jest używanie VPN-a. "
            "Jeśli musisz korzystać z publicznego Wi-Fi, nigdy nie loguj się do ważnych dla ciebie kont np. stron bankowych lub poczty. ",

            "Świadomość zagrożeń, wiedza o nich i czujność to twoje najważniejsze narzędzia obrony. "
            "Zawsze zastanów się dwa razy, zanim klikniesz link, pobierzesz plik lub udostępnisz komuś twoje dane online. "
            "Zasada ograniczonego zaufania w sieci to najprostszy, a zarazem najskuteczniejszy sposób ochrony siebie i swoich danych. ",

            "6. Łamanie haseł użytkowników –> cyberprzestępcy często próbują uzyskać dostęp do kont użytkowników, odgadując lub łamiąc ich hasła. "
            "Stosują w tym celu m.in. ataki słownikowe (sprawdzanie haseł z gotowej listy popularnych fraz), ataki brute-force (sprawdzanie wszystkich możliwych kombinacji znaków) "
            "oraz tzw. credential stuffing — wykorzystanie haseł wyciekłych z innych serwisów, ponieważ wielu użytkowników używa tego samego hasła w różnych serwisach. ",
            "- Jak się bronić: używaj długich, losowych i unikalnych haseł dla każdego ze swoich kont. "
            "Korzystaj z menedżera haseł oraz włącz uwierzytelnianie dwuskładnikowe (2FA). "
            "Pamiętaj, aby nigdy nie używać tego samego hasła w więcej niż jednym miejscu, w przeciwnym razie wyciek z jednego serwisu może doprowadzić do przejęcia wszystkich twoich kont. ",

            "Skutkiem złamania hasła może być utrata danych, pieniędzy, dostęp do prywatnych informacji, kradzież tożsamości, a nawet wykorzystanie twojego konta do kolejnych cyberataków. "
            "To właśnie dlatego ochrona haseł jest jednym z najważniejszych elementów bezpieczeństwa w sieci."
        ]
    })

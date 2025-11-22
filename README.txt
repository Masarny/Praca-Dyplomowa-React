Do uruchomienia aplikacji należy pobrać i zainstalować następujące oprogramowanie:
1. Python w wersji 3.10 lub nowszej, link do pobrania: https://www.python.org/downloads/
2. Node.js w wersji 18 lub nowszej, link do pobrania: https://nodejs.org/en/download/

Aby zainstalować backend, aplikacji przejdź do folderu „backendu”, następnie uruchom w nim narzędzie cmd (Windows) lub terminal (Linux/Mac), po czym utwórz tam środowisko wirtualne, wykorzystując np. następujące polecenia zależnie od systemu, który używasz:
Przykładowe komendy dla Windows: 
	a) python -m venv venv
	b) venv\Scripts\activate
Przykładowe komendy dla Linux/Mac:
	a) python3 -m venv venv
	b) source venv/bin/activate
W ostatnim kroku zainstaluj wymagane zależności backendu z pliku requirements.txt, np. narzędziem pip: pip install -r requirements.txt.

Aby zainstalować frontend, aplikacji przejdź do folderu „frontend”, uruchom w nim narzędzie cmd (Windows) lub terminal (Linux/Mac), po czym zainstaluj zależności frontend narzędziem npm, wykonując komendę: npm install. NPM zainstaluje zależności z pliku package.json.
Uruchomienie aplikacji webowej:
	a) Uruchomienie backendu: Będąc w aktywnym środowisku wirtualnym vent, uruchom plik app.py oprogramowaniem python, wykonaj komendę: python app.py.
	b) Uruchomienie frontend: Będąc w folderze „frontend”, uruchom w nim narzędzie cmd (Windows) lub terminal (Linux/Mac), po czym uruchom frontend narzędziem npm, komenda: npm run dev.

Otwórz przeglądarkę i przejdź do: http://localhost:5173. Aplikacja powinna być uruchomiona pod tym adresem.

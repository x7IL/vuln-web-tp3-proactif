# vulnerable-app

Petite app Flask volontairement trouée pour le TP3 DevSecOps. Sert
de cible à CodeQL et Dependabot via la CI GitHub Actions.

À lancer en local uniquement.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Failles présentes :

- `/search` — SQL injection
- `/greet` — XSS / SSTI
- `/ping` — command injection
- `/download` — path traversal
- `/hash` — MD5
- `/deserialize` — pickle.loads sur de l'input user
- `app.secret_key` hardcodé
- `app.run(debug=True)`

Pipeline :

- `.github/workflows/ci.yml` — quickstart
- `.github/workflows/codeql.yml` — SAST
- `.github/dependabot.yml` — SCA hebdo

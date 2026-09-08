# validkit

validkit ist eine kleine, eigenständige Python-Bibliothek mit neun unabhängigen
Prüf- und Normalisierungsfunktionen. Sie nutzt ausschließlich die
Standardbibliothek, hat keinerlei Laufzeit-Abhängigkeiten und keine
CLI/UI oder Netzwerkzugriffe. Jede Funktion ist typannotiert und meldet
ungültige Eingaben mit einem aussagekräftigen `ValueError`.

## Tech-Stack

- Sprache: Python (>= 3.10)
- Tests: pytest
- Paketierung: setuptools (pyproject.toml)
- Abhängigkeiten: keine (nur Standardbibliothek)

## Installation

Das Paket benötigt keine externen Abhängigkeiten und lässt sich direkt aus dem
Quellverzeichnis installieren:

```bash
pip install -e .
```

Nach der Installation sind alle neun Funktionen importierbar:

```python
from validkit import (
    is_valid_email,
    luhn_check,
    is_valid_iban,
    is_valid_isbn13,
    normalize_phone,
    strip_accents,
    mask_secret,
    slugify,
    clamp,
)
```

## Tests ausführen

```bash
pip install -e ".[dev]"
pytest
```

## Verwendung — Beispiele pro Funktion

### is_valid_email

```python
from validkit import is_valid_email

is_valid_email("test@example.com")  # True
is_valid_email("test@")  # False
```

### luhn_check

```python
from validkit import luhn_check

luhn_check("4532015112830366")  # True
luhn_check("4532015112830367")  # False
```

### is_valid_iban

```python
from validkit import is_valid_iban

is_valid_iban("DE89 3704 0044 0532 0130 00")  # True
is_valid_iban("DE89 3704 0044 0532 0130 01")  # False
```

### is_valid_isbn13

```python
from validkit import is_valid_isbn13

is_valid_isbn13("978-3-16-148410-0")  # True
is_valid_isbn13("978-3-16-148410-1")  # False
```

### normalize_phone

```python
from validkit import normalize_phone

normalize_phone("030 1234567", "DE")  # '+49301234567'
```

### strip_accents

```python
from validkit import strip_accents

strip_accents("Crème brûlée — déjà vu")  # 'Creme brulee — deja vu'
```

### mask_secret

```python
from validkit import mask_secret

mask_secret("geheim12345", 4)  # '*******2345'
mask_secret("abc", 4)  # 'abc'
```

### slugify

```python
from validkit import slugify

slugify("  Héllo, Wörld!  ")  # 'hello-world'
```

### clamp

```python
from validkit import clamp

clamp(5, 0, 10)  # 5
clamp(-5, 0, 10)  # 0
clamp(15, 0, 10)  # 10
```

## Funktionen

| Funktion | Beschreibung |
| --- | --- |
| `is_valid_email(text)` | Prüft eine E-Mail-Adresse |
| `luhn_check(digits)` | Prüft eine Ziffernfolge mit dem Luhn-Algorithmus |
| `is_valid_iban(text)` | Prüft eine IBAN |
| `is_valid_isbn13(text)` | Prüft eine ISBN-13 |
| `normalize_phone(text, country_code)` | Normalisiert eine Telefonnummer nach E.164 |
| `strip_accents(text)` | Entfernt Akzentzeichen |
| `mask_secret(text, keep=4)` | Maskiert alle Zeichen bis auf die letzten `keep` |
| `slugify(text)` | Erzeugt einen URL-freundlichen Slug |
| `clamp(value, low, high)` | Begrenzt einen Wert auf ein Intervall |

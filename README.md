# Zavrsni-demo

Ovaj projekt je web aplikacija izgrađena koristeći Django za testiranje performansi procesa enkripcije i dekripcije na višejezgrenom CPU-u. Aplikacija generira graf koji prikazuje opterećenje CPU-a prije i poslije izvršenja te pruža detaljne statistike vremena izvršavanja.

## Značajke
- Generiranje slučajnih stringova i njihova enkripcija/dekripcija koristeći AES.
- Mjerenje opterećenja CPU-a na svim dostupnim jezgrama.
- Prikaz detalja o vremenu izvršavanja i graf opterećenja CPU-a.

## Preduvjeti
- Python 3.x
- Django 5.1
- Potrebne Python knjižnice navedene u `requirements.txt`

## Instalacija

### Kloniranje Repozitorija
```bash
git clone https://github.com/dujebuljat/zavrsni-demo.git
cd zavrsni-demo
```

## Postavljanje virtualnog okruženja

### Linux/MacOS
```
python3 -m venv venv
source venv/bin/activate
```

### Windows
```
python -m ven venv
venv\Scripts\activate
```

### Instalacija ovisnosti
```
pip install -r requirements.txt
```

## Pokretanje aplikacije

### Primjena migracija
```
python manage.py migrate
```

### Pokretanje servera

#### Linux/MacOS
```
python3 manage.py runserver
```

#### Windows
```
python manage.py runserver
```

Aplikacija će biti dostupna na `http://localhost:8000/test/`.

## Korištenje aplikacije

* Otvorite `http://localhost:8000/test/` u vašem web pregledniku
* Stranica će prikazati graf opterećenja CPU-a prije i poslije izvršenja zajedno s detaljima o vremenu izvršavanja

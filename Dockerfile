# ETAP 1: Budowanie (Builder)
FROM python:3.10-slim AS builder

WORKDIR /app

# Instalujemy zależności do folderu lokalnego
RUN pip install --user flask

# ETAP 2: Produkcja (Final)
# Możesz tu użyć jeszcze mniejszego obrazu, np. python:3.10-alpine lub distroless
FROM python:3.10-slim

WORKDIR /app

# Kopiujemy TYLKO zainstalowane paczki z etapu builder
COPY --from=builder /root/.local /home/myuser/.local
COPY app.py .

# Ustawiamy PATH, żeby Python widział paczki
ENV PATH=/home/myuser/.local/bin:$PATH

# Bezpieczeństwo: tworzymy użytkownika
RUN useradd -m myuser
USER myuser

# Ostatni szlif: Sonar i Trivy będą zachwycone tym obrazem
CMD ["python", "app.py"]
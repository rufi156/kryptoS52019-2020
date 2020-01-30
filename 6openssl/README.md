OpenSSl

OpenSSL jest programem służącym do obsługi certyfikatów w formacie X.509.

Program OpenSSL jest zasadniczo używany z poziomu terminala. Polecenia nas interesujące to:

    openssl genrsa -des3 1024 > key.pem

    openssl req -x509 -new -key key.pem > key-cert.pem

Pierwsze polecenie generuje parę kluczy RSA i umożliwia dalsze generowanie certyfikatów w oparciu o przygotowany zestaw. Klucz prywatny zostanie zaszyfrowany, można opuścić to żądanie. Drugie polecenie generuje nowy certyfikat w formacie X.509. Certyfikat zostaje zapisany w pliku tekstowym i może być importowany do programu pocztowego, np. Thunderbird.

Zadanie:
========

1.  Wygeneruj dla siebie certyfikat, powinien on zawierać imię, nazwisko, email oraz instytucję "laboratorium z kryptografii", powinien być ważny co najmniej do końca semestru (i raczej niewiele dłużej). Certyfikat w formacie X.509 (\*.pem) umieść jako rozwiązanie zadania.

2.  Przygotuj plik dane.txt zawierający imię, nazwisko i bieżącą datę. Umieść jako rozwiązanie zadania podpisaną przez siebie powyższą wiadomość.


by Andrzej M. Borzyszkowski

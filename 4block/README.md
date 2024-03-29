Tryby szyfrów blokowych

Na [wykładzie 3](../krypto/blok.pdf), slajdy 6-12, przedstawiono kilka trybów szyfrów blokowych, z czego nas będzie interesować w tej chwili tryb EBC, książki kodowej, oraz tryb CBC, dodawania zaszyfrowanego bloku do szyfrowania kolejnego bloku. Pierwszy tryb jest zbyt prosty, by być odporny na wielokrotne szyfrowanie, czy na atak z tekstem jawnym. Celem tego ćwiczenia będzie unaocznienie tej prostoty w sposób wizualny.

W zadaniu, należy zaprojektować "szyfrowanie" obrazu graficznego. Obraz powinien być czarno-biały i mieć rozmiar rzędu kilkuset pikseli w pionie i w poziomie. Obraz taki należy podzielić na małe bloki, np. 3x4 piksele, w ten sposób każdy blok grafiki zostaje potraktowany jako blok szyfru blokowego. Np. 12-bitowy, jak w programie miniDES. Cały obraz należy potraktować jako ciąg małych bloków, np. przeglądanych kolejnymi wierszami. A jeśli nie jest dostępna implementacja szyfru blokowego, można przyjąć dowolne przekształcenie. Nie jest konieczne odszyfrowywanie kryptogramu, jest istotne, by te same bloki były identycznie szyfrowane. Np. można zastosować jakąkolwiek funkcję skrótu, np md5sum czy sha1sum, odpowiednio dostosowaną do przekształcania małych bloków.

**Uwaga:** celem zadania jest zrozumienia działania trybów blokowych, a nie tylko ich nazw. W związku z tym w rozwiązaniu **nie można** stosować gotowych bibliotek wywołujących szyfrowanie w jakimś trybie szyfru blokowego.

Program powinien wczytać plik graficzny i wyprodukować dwa pliki graficzne: kryptogram zaszyfrowany w trybie ECB oraz kryptogram zaszyfrowany w trybie CBC. Należy pamiętać, że obrazek powinien być maksymalnie nieskomplikowany, np. jakiś znak firmowy albo powiększona do dużych rozmiarów czcionka. Przykłady: [obrazek](blok/plain24bit.bmp) jest przekształcany w trybie [ECB](blok/ECB24bit.bmp) oraz [CBC](blok/CBC24bit.bmp) i drugi [obrazek](blok/plain.bmp), [ECB](blok/ecb_crypto.bmp) i [CBC](blok/cbc_crypto.bmp).

Zadanie:
========

Program block powinien czytać pliki: graficzny plain.bmp i opcjonalnie tekstowy key.txt z kluczem i powinien zapisywać dwa pliki graficzne "zaszyfrowanego" obrazu ecb\_crypto.bmp oraz cbc\_crypto.bmp. W rozwiązaniu należy przesłać program w wersji źródłowej i skompilowanej jak również testowy plik graficzny i ew. plik z kluczem.
 **Uwaga:** w programie nie wolno stosować wbudowanych bibliotek kryptograficznych z wywołaniem funkcji szyfrowania w wybranym trybie blokowym, należy te tryby zaimplementować własnoręcznie.


by Andrzej M. Borzyszkowski

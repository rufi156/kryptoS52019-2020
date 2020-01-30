Steganografia i znaki wodne

Na [wykładzie](../krypto/stegano.pdf) przedstawiono problematykę ukrywania wiadomości w różnych nośnikach.

Zadanie:
========

Dane są pliki **mess.txt** z ciągiem bitów zapisanym w układzie szesnastkowym (podobnie jak wyniki funkcji skrótu, jeden z znak z zakresu [0-9,a-e] oznacza 4 bity) oraz **cover.html** dużo większy jako zawartość jakiejś strony internetowej.

Program **stegano**będzie wywoływany z dwiema opcjami. Opcja **-e** oznacza zanurzanie wiadomości, opcja **-d** jej wyodrębnianie. Wiadomość odczytana z pliku **mess.txt**. Program wywołany jako zanurzanie zapisze zmieniony odpowiednio nośnik do pliku o nazwie **watermark.html**. Program w opcji wyodrębniania będzie odczytywać plik **watermark.html** i zapisywać wyodrębnioną wiadomość do pliku **detect.txt**. Program wywołany z opcją **-e** powinien zwracać błąd, gdy nośnik jest za mały do przekazania całej wiadomości.

Opcje o numerach -1, -2, -3 i -4 będą oznaczać przyjęty algorytm zanurzania wiadomości.

1.  każdy bit ukrywanej wiadomości będzie przekazywany jako dodatkowa spacja na końcu każdego wiersza, ukrywana wiadomość może mieć najwyżej tyle bitów ile wierszy w nośniku.
2.  każdy bit ukrywanej wiadomości będzie ukrywany jako pojedyncza lub podwójna spacja. Znaki tabulacji można pozostawić bez zmian. Ukrywana wiadomość może być co najwyżej długości równej liczbie spacji bez powtórzeń w nośniku.
3.  bity ukrywanej wiadomości będą przekazywane jako fałszywe literówki w nazwach atrybutów. Np. można w każdym znaczniku akapitu bez podanej wysokości czy marginesu dodać te atrybuty: **\<p style="margin-bottom: 0cm; line-height: 100%"\>** i wprowadzać błędną nazwę, np. margin-botom lub lineheight. Wówczas wiadomość jest ukrywana w wystąpieniach tych dwóch atrybutów, zero jako błąd w jednym a 1 jako błąd w drugim.
4.  bity ukrywanej wiadomości będą kodowane jako niepotrzebne sekwencje otwierające i zamykające znaczniki, np. zmiany fontu. W tej opcji program będzie poszukiwał wystąpień znacznika FONT i bit 1 wiadomości spowoduje, że otwarcie znacznika zostanie zastąpione sekwencją otwarcie-zamknięcie-otwarcie tego znacznika a bit 0 przeciwnie, po zamknięciu będzie doklejona jeszcze jedna pusta para . Wiadomość ukrywana nie może w tej wersji mieć więcej bitów niż wystąpień tego znacznika w nośniku.

We wszystkich przypadkach trzeba pamiętać o usunięciu wszystkich przypadkowych wystąpień sekwencji, które mają kodować wiadomość: spacji na końcach wierszy, podwójnych spacji, nieprawidłowych nazw atrybutów, które właśnie chcemy wprowadzić czy niepotrzebnych par otwarcie-zamknięcie znacznika, który używamy do ukrywania wiadomości.


by Andrzej M. Borzyszkowski

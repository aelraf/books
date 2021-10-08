Zadanie - lista książek

W wykorzystaniem dowolnego frameworka dostępnego dla języka Python (np. Django lub
Flask) stwórz aplikację do zarządzania zbiorem książek. Aplikacja powinna pozwalać na
ręczne dodawanie/edycję/usuwanie książek oraz ich importowanie korzystając z publicznie
dostępnego API Google (https://www.googleapis.com/books/v1/volumes?q=Hobbit) . 
Do warstwy wizualnej można wykorzystać bibliotekę Bootstrap.

Część 1:
1. Zamodeluj obiekty bazodanowe tak, by zawierały pola: tytuł, autor, data publikacji,
numer ISBN, liczba stron, link do okładki i język publikacji .

2. Stwórz 2 widoki: 
 a. Widok listy wszystkich znajdujących się w bazie książek z możliwością
wyszukiwania po tytule, autorze i języku oraz zakresie dat publikacji (od - do).
Lista ma zawierać wszystkie informacje z modelu wyświetlone w czytelny
sposób (np. w tabelce).
 b. Widok z formularzem pozwalającym na ręczne dodawanie/edycję książek
wraz z wyświetlaniem błędów walidacji.

Część 2:
1. Stwórz widok, który pozwoli na import książek według słów kluczowych z API:
https://developers.google.com/books/docs/v1/using#WorkingVolumes. Wpisy tych
książek muszą znaleźć się w bazie danych, która została stworzona w pierwszej części
tego zadania.

Część 3:
1. Utwórz widoki REST API, które będzie posiadało listę książek z wyszukiwaniem i
filtrowaniem przy użyciu query strings, jak w punkcie 2.a. z części pierwszej.

Część 4:
1. Postaw aplikację na publicznie dostępnym serwerze - darmowe Heroku jest jedną z
opcji.

Część 5:
1. Napisz testy jednostkowe oraz sprawdź kod pod względem standardów PEP8 .

Kod musi być napisany zgodnie ze standardami PEP8 oraz posiadać testy jednostkowe. Przy
odsyłaniu zadania, prosimy o udostępnienie adresu www, na którym jest dostępna aplikacja
oraz o adres do publicznego repozytorium, tak aby nasi rekruterzy techniczni byli w stanie
zajrzeć w kod.
Powodzenia!


W drugim podejściu zrobimy aplikację za pomocą frameworku Django, który znacząco ułatwia całość.


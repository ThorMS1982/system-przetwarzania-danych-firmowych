Firma dostaje dane (pliki)
  - dane są brudne / niespójne

Program musi:
  - je sprawdzić
  - przefiltrować
  - wygenerować raport
  - zapisać wynik

W katalogu razem z plikiem .py musi byc plik .csv. Na dole kodu przy wywolaniu podmien nazwe input_file.
Plik .csv powinien miec trzy kolumny : email, amount, country. Tylko poprawny email(@,domena) jest akceptowalny, jak i kwota dodatnia oraz skrot kraju skladajacy sie z dwoch duzych liter.

UPDATE_1 :
Dodalem automatyczny raport statystyczny, który odpowiada na pytania managementu:
  - ile rekordów było poprawnych
  - ile było błędnych
    
Jaka jest:
  - suma sprzedaży
  - średnia kwota sprzedaży

UPDATE_2 :
Z clean_records stworzylem DataFrame pandas
Zrobilem agregacje per kraj:
  - suma sprzedaży
  - średnia sprzedaży
  - liczba poprawnych rekordów

Zapisalem wynik do Excel .xlsx
Zrobilem wykres słupkowy sprzedaży per kraj i zapis do pliku PNG


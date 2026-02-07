import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"




def validate_record(record):
    errors = []

    email = record.get("email", "").strip()
    amount_raw = record.get("amount", "").strip()
    country = record.get("country", "").strip()

    # walidacja email
    # walidacja email
    if not email:
         errors.append("email jest pusty")
    elif not re.match(EMAIL_REGEX, email):
         errors.append("email ma niepoprawny format")


    # walidacja amount
    try:
        amount = float(amount_raw)
        if amount <= 0:
            errors.append("amount musi byc > 0")
    except ValueError:
        errors.append("amount nie jest liczba")

    # walidacja country
    if len(country) != 2 or not country.isupper():
        errors.append("country musi miec 2 wielkie litery")

    if errors:
        return False, errors

    cleaned_record = {
        "email": email,
        "amount": amount,
        "country": country
    }

    return True, cleaned_record




def process_sales_data(filename):
    clean_records = []
    error_records = []

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for line_num, row in enumerate(reader, start=2):  # start=2 bo nagłówek to linia 1
            is_valid, result = validate_record(row)

            if is_valid:
                clean_records.append(result)
            else:
                error_records.append({
                    "line": line_num,
                    "errors": result
                })

    return clean_records, error_records


def save_clean_data(records, filename):
    if not records:
        print("Brak poprawnych rekordów do zapisania.")
        return

    # Pobieramy nagłówki z kluczy pierwszego rekordu
    headers = records[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    print(f"Poprawne rekordy zapisane do {filename}")


def log_errors(errors, filename):
    if not errors:
        print("Brak błędów do zapisania.")
        return

    with open(filename, 'w', encoding='utf-8') as f:
        for err in errors:
            line = err["line"]
            for e in err["errors"]:
                f.write(f"Linia {line}: {e}\n")

    print(f"Błędy zapisane do {filename}")


def generate_report(clean_records, error_records, filename):
    total_records = len(clean_records) + len(error_records)
    valid_count = len(clean_records)
    error_count = len(error_records)

    total_amount = sum(record["amount"] for record in clean_records)
    average_amount = total_amount / valid_count if valid_count > 0 else 0

    with open(filename, "w", encoding="utf-8") as f:
        f.write("metric,value\n")
        f.write(f"total_records,{total_records}\n")
        f.write(f"valid_records,{valid_count}\n")
        f.write(f"error_records,{error_count}\n")
        f.write(f"total_sales_amount,{total_amount}\n")
        f.write(f"average_sales_amount,{average_amount}\n")




def generate_excel_report(clean_records, excel_filename, chart_filename):
    if not clean_records:
        print("Brak poprawnych danych do raportu Excel.")
        return

    # Tworzymy DataFrame z listy słowników
    df = pd.DataFrame(clean_records)

    # Grupowanie danych per kraj
    country_summary = df.groupby('country').agg(
        total_sales=('amount', 'sum'),
        average_sales=('amount', 'mean'),
        record_count=('amount', 'count')
    ).reset_index()

    # Zapis do Excel
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        country_summary.to_excel(writer, sheet_name='Summary', index=False)
        df.to_excel(writer, sheet_name='All_Records', index=False)

    print(f"Raport Excel zapisany jako {excel_filename}")

    # Tworzymy wykres słupkowy sprzedaży per kraj
    plt.figure(figsize=(8,6))
    plt.bar(country_summary['country'], country_summary['total_sales'], color='skyblue')
    plt.ylim(0, country_summary['total_sales'].max() * 1.1)  # 10% więcej niż max
    plt.title('Suma sprzedaży per kraj')
    plt.xlabel('Kraj')
    plt.ylabel('Suma sprzedaży')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(chart_filename)
    plt.close()
    print(f"Wykres zapisany jako {chart_filename}")




if __name__ == "__main__":
    input_file = "sales.csv"
    clean_file = "clean_sales.csv"
    error_file = "errors.log"
    report_file = "report.csv"
    excel_file = "report.xlsx"
    chart_file = "sales_per_country.png"

    clean_records, error_records = process_sales_data(input_file)
    save_clean_data(clean_records, clean_file)
    log_errors(error_records, error_file)
    generate_report(clean_records, error_records, report_file)
    generate_excel_report(clean_records, excel_file, chart_file)

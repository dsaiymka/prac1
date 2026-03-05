# receipt_parser.py
import re
import json

# читаем текст чека
with open("raw.txt", "r", encoding="utf-8") as f:
    data = f.read()

# цены (учитываем пробелы в больших суммах, например "1 200,00")
price_strings = re.findall(r"\d[\d\s]*,\d{2}", data)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in price_strings]

# товары: всё перед ценой
products = re.findall(r"(\d+\.\s+)?(.+?)\s+\d[\d\s]*,\d{2}", data)
products = [p[1].strip() for p in products]  # берём вторую группу (название товара)

# дата и время
dates = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", data)
times = re.findall(r"\b\d{2}:\d{2}:\d{2}\b", data)

# способ оплаты
payment = re.findall(r"Банковская карта|Cash|Card", data, re.IGNORECASE)

# общая сумма (ИТОГО)
total_match = re.search(r"ИТОГО:\s*([\d\s]+,\d{2})", data)
total = 0
if total_match:
    total = float(total_match.group(1).replace(" ", "").replace(",", "."))

# формируем результат
receipt = {
    "products": products,
    "prices": prices,
    "total": total,
    "dates": dates,
    "times": times,
    "payment": payment
}

# выводим в JSON
print(json.dumps(receipt, indent=2, ensure_ascii=False))
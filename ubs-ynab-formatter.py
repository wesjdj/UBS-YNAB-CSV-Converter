import csv
import re
import datetime

class aTransaction:
  def __init__(self, date, payee, memo, amount):
    self.date = date
    self.payee = payee
    self.memo = memo
    self.amount = amount

transactions = []

# optional user setting prompts

print('Remove Twint prefix from payee field? (Y/n):')
remove_twint = input()

print('Remove PayPal prefix from payee field? (Y/n):')
remove_paypal = input()

print('Remove country suffix from payee field? (Y/n):')
remove_country_code = input()

print('Remove multiple spaces from payee field? (Y/n):')
remove_multiple_spaces = input()

print('Add Cardholder name to memo field? (Y/n):')
add_cardholder_to_memo = input()

with open('transactions.csv', newline='', errors='replace') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=';')
  for row in spamreader:
    if len(row) != 0:
      account_number_match = re.search("^\d{4}\s{1}\d{4}\s{1}\d{4}$", row[0])
      if account_number_match:

        transaction_payee = row[4]
        transaction_memo = row[5]

        transaction_amount = 0

        # format transaction amount
        if row[10] != '' and row[11] == '':
          transaction_amount = "-" + row[10]
        elif row[10] == '' and row[11] != '':
          transaction_amount = row[11]
        else:
          print("Invalid transaction amount: row 10: ", str(row[10]), "row 11: ", str(row[11]))
        
        # remove Twint prefix if requested
        if remove_twint == 'Y':
          transaction_payee = transaction_payee.replace('TWINT  *','')

        # remove PayPal prefix if requested
        if remove_paypal == 'Y':
          transaction_payee = transaction_payee.replace('PAYPAL *','')

        # remove country code suffix if requested
        if remove_country_code == 'Y':
          transaction_payee = re.sub("\s[A-Z]{3}$", "", transaction_payee)

        # remove multiple spaces if requested
        if remove_country_code == 'Y':
          transaction_payee = re.sub("\s{2,}", " ", transaction_payee)

        # add cardholder name to memo field if requested
        if add_cardholder_to_memo == 'Y':
          transaction_memo = transaction_memo + " " + row[2]

        # remove trailing spaces from payee
        transaction_payee = re.sub("\s$", "", transaction_payee)

        # format date
        x = datetime.datetime.strptime(row[3], '%d.%m.%Y')
        transaction_date = x.strftime('%Y-%m-%d')

        transaction = aTransaction(transaction_date, transaction_payee, transaction_memo, transaction_amount)
        transactions.append(transaction)

# write to output csv file
with open('output.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
  spamwriter.writerow(["Date","Payee","Memo","Amount"])
  for transaction in transactions:
    print(transaction.date, transaction.payee, transaction.memo, transaction.amount)
    spamwriter.writerow([transaction.date, transaction.payee, transaction.memo, transaction.amount])


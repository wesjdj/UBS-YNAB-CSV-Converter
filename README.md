# UBS Credit Card CSV to YNAB conversion

This Python script reformats credit card statements exported by the UBS Online Banking portal to a format which can be imported into [YNAB](youneedabudget.com).

Some common UBS credit card statement booking text noise can be removed, such as PayPal or Twint prefixes before the Payee name and multiple successive whitespaces.

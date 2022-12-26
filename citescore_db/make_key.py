def make_key(journal,year):

    journal_key=''.join(c.lower() for c in journal if c.isalpha())
    return f'{year}{journal_key}'


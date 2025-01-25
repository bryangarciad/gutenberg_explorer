from re import sub, compile

def snake_case(text: str):
    '''
    Cast string to snake case key
    '''

    pattern = compile(r'[^a-zA-Z0-9\s]')
    clean_text = pattern.sub('', text)
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        clean_text.replace('-', ' '))).split()).lower()

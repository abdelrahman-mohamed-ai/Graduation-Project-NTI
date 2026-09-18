"""Presentation-only localization. Model and storage objects never enter this layer."""
import json
import re
from functools import lru_cache
from html import escape
from html.parser import HTMLParser
from flask import g, request
from config import BASE_DIR

CATALOG = json.loads((BASE_DIR / 'translations/ar.json').read_text(encoding='utf-8'))
LOOKUP = {k.casefold(): v for k, v in CATALOG.items()}
PHRASES = re.compile(r'(?<![\w])(?:' + '|'.join(re.escape(k) for k in sorted(CATALOG, key=len, reverse=True)) + r')(?![\w])', re.I)

@lru_cache(maxsize=8192)
def translate(text, language='ar'):
    if language != 'ar' or not text.strip(): return text
    stripped = text.strip()
    value = LOOKUP.get(stripped.casefold())
    if value is None:
        value = PHRASES.sub(lambda match: LOOKUP[match.group().casefold()], stripped)
    return text[:len(text)-len(text.lstrip())] + value + text[len(text.rstrip()):]

class LocalizedHTML(HTMLParser):
    def __init__(self, language):
        super().__init__(convert_charrefs=True)
        self.language, self.output, self.stack = language, [], []
    def handle_starttag(self, tag, attrs):
        skip = any(self.stack) or tag in ('script', 'style') or any(k == 'data-i18n-skip' for k,v in attrs)
        if tag not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'): self.stack.append(skip)
        originals = {}
        result = []
        for key, value in attrs:
            if not skip and key in ('title','placeholder','aria-label','alt') and value:
                originals[key] = value
                value = translate(value, self.language)
            result.append((key, value))
        if originals: result.append(('data-i18n-attrs', json.dumps(originals, ensure_ascii=False)))
        self.output.append('<'+tag+''.join(' '+k+(('="'+escape(v, quote=True)+'"') if v is not None else '') for k,v in result)+'>')
    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        if self.stack: self.stack.pop()
        self.output.append('</'+tag+'>')
    def handle_data(self, data):
        if not any(self.stack) and data.strip():
            translated = translate(data, self.language)
            if translated != data:
                # Original source survives instant language changes without wrapping text.
                import base64
                self.output.append('<!--i18n:'+base64.b64encode(data.encode()).decode()+'-->')
            self.output.append(escape(translated, quote=False))
        else: self.output.append(data)
    def handle_entityref(self, name): self.output.append('&'+name+';')
    def handle_charref(self, name): self.output.append('&#'+name+';')
    def handle_comment(self, data): self.output.append('<!--'+data+'-->')
    def handle_decl(self, decl): self.output.append('<!'+decl+'>')

def init_i18n(app):
    @app.before_request
    def language():
        choice = request.args.get('lang', request.cookies.get('eduguard_language', 'en'))
        g.language = choice if choice in ('en','ar') else 'en'
    @app.context_processor
    def language_context(): return dict(language=g.language, translations=CATALOG)
    @app.after_request
    def localize(response):
        if response.mimetype == 'text/html':
            parser = LocalizedHTML(g.language)
            parser.feed(response.get_data(as_text=True))
            response.set_data(''.join(parser.output))
            response.headers['Content-Language'] = g.language
            response.headers['Vary'] = 'Cookie'
        if request.args.get('lang') in ('en','ar'):
            response.set_cookie('eduguard_language', g.language, max_age=31536000, samesite='Lax', secure=request.is_secure)
        return response

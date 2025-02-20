"""
Python simple SOAP Client helpers.
"""

from datetime import datetime
from urllib import request
from urllib.parse import urlsplit
import os
import logging
import hashlib

log = logging.getLogger(__name__)

def fetch(url:str, http:str=None, cache:bool=False, force_download:bool=False, wsdl_base_dir:str='', headers:dict=None):
    '''Download a document from a URL, save it locally if cahce enabled'''

    # check / append a valid sceham if not given
    url_scheme, netloc, path, query, fragment = urlsplit(url)
    schemas = ['http', 'https','file']
    if not url_scheme in schemas:
        for scheme in schemas:
            try:
                path = os.path.normpath(os.path.join(wsdl_base_dir, url))
                if not url.startswith("/") and scheme in ('http','https'):
                    tmp_url = f'{scheme}://{path}'
                else:
                    tmp_url = f"{scheme}:{path}"
                log.debug(f'Scheme not found, trying {scheme}')
                return fetch(tmp_url, http, cache, force_download, wsdl_base_dir, headers)
            except Exception as e:
                log.error(e)
        raise RuntimeError(f'No scheme given for url: {url}')
    
    # make md5 hash of the url for caching
    filename = f'{hashlib.md5(url.encode('utf8')).hexdigest()}.xml'
    if isinstance(cache, str):
        filename= os.path.join(cache, filename)
    if cache and os.path.exists(filename) and not force_download:
        log.info(f'Reading file: {filename}')

    return url_scheme, netloc, path, query, fragment


if __name__ == '__main__':
    gus_wsdl = "https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl-ver11-test.wsdl"
    gus_endpoint = "https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc"
    print(fetch(gus_wsdl))
    print(fetch(gus_endpoint))

# coding=UTF-8

import time
import httplib2
from urllib.parse import quote
from xml.etree.ElementTree import fromstring
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Taxon

class Command( BaseCommand ):
    help = 'Check for every species in the database if there are any photos on the EoL Flickr group.'
    usage_str = 'Usage: ./manage.py check_flickr app'

    def handle( self, *args, **options ):
        conn = httplib2.Http(timeout=600)
        for taxon in Taxon.objects.all().order_by('genus', 'species'):
            print('Processing', taxon.genus,taxon.species)
            url_query = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+settings.FLICKR_API_KEY+'&group_id=806927%40N20&machine_tags=taxonomy%3Abinomial%3D%22'+quote(taxon.genus.encode('utf-8'))+'%20'+quote(taxon.species.encode('utf-8'))+'%22'
            resp, content = conn.request( url_query )
            if resp.status == 200:
                xml = content
                tree = fromstring( xml )
                photos = tree.find( 'photos' )
                if photos is not None:
                    total = photos.get( 'total' )
                    if total not in [None, '']:
                        total = int(total)
                        print(str(total), 'photos')
                        if total > 0:
                            if not taxon.has_pictures:
                                taxon.has_pictures = True
                                taxon.save()
                        else:
                            if taxon.has_pictures:
                                taxon.has_pictures = False
                                taxon.save()
                    else:
                        print('No @total attribute!')
                else:
                    print('No <photos> element!')
            else:
                print('Failed! HTTP status code', str(resp.status))
            time.sleep(1)

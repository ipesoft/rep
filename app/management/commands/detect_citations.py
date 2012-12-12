# coding=UTF-8

import os, sys, string
from optparse import make_option
from django.core.management.base import BaseCommand
from rep.app.models import Interview, TaxonName
from app.interview_paginator import InterviewPaginator

class Command( BaseCommand ):
    option_list = BaseCommand.option_list + (
        make_option('-i', '--interview', dest='interview_id', type='int',
            help='Interview identifier'),
    )
    help = 'Detect species citations in interviews.'
    usage_str = 'Usage: ./manage.py detect_citations app [-i --interview interview id]'

    def handle( self, app=None, interview_id=None, **options ):

        if interview_id is None:
            interviews = Interview.objects.all().order_by('title')
        else:
            interviews = Interview.objects.filter(pk=interview_id)

        popular_names = TaxonName.objects.filter(ntype='P')

        for interview in interviews:
            paginator = None
            output = 'Interview: ' + interview.title
            print output
            print '-' * len(output)
            has_names = False
            for pop_name in popular_names:
                cnt = interview.content.count(pop_name.name)
                if cnt > 0:
                    has_names = True
                    if paginator is None:
                        paginator = InterviewPaginator(interview.content, 1, 0, True, 40)
                    num_found = 0
                    pages = []
                    for page_num in range(1, paginator.num_pages+1):
                        page_obj = paginator.page(page_num)
                        content = page_obj.object_list[0] # There must always one object
                        page_cnt = content.count(pop_name.name)
                        if page_cnt > 0:
                            pages.append(page_num)
                            num_found += page_cnt
                        if num_found == cnt:
                            break
                    print 'Found', pop_name.name, 'in pages', str(pages)
            if not has_names:
                print 'nothing found'



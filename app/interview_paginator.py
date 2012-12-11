import textwrap
from django.core.paginator import Paginator

class InterviewPaginator(Paginator):
    """
    A paginator that takes a long text and splits it into pages according to
    a lines per page configuration
    """
    def __init__(self, text, per_page, orphans=0, allow_empty_first_page=True, lines_per_page=40):
        """
        Instead of an object_list this object takes a long string
        """
        self.object_list = []
        num_lines_in_page = 0
        page_content = ''
        paragraphs = text.split("\n")
        for paragraph in paragraphs:
            lines = textwrap.wrap(paragraph)
            page_content += paragraph + "\n"
            num_lines_in_page += len(lines)
            if num_lines_in_page >= lines_per_page:
                self.object_list.append(page_content)
                page_content = ''
                num_lines_in_page = 0
        self.per_page = per_page
        self.orphans = orphans
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None



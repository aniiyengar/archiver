
from bs4 import BeautifulSoup
import io
from pathlib import Path
import re

from utils.basefile import BaseFile

class KindleFile(BaseFile):

    def compile(self, file: io.FileIO) -> object:
        if not str(self.file_name).startswith('.'):
            soup = BeautifulSoup(file.read(), features='html.parser')

            sections = soup.select('h2.sectionHeading, h3.noteHeading, div.noteText')
            curr_section = None
            results = []

            for sec in sections:
                if 'sectionHeading' in sec['class']:
                    curr_section = list(sec.children)[0].string
                elif 'noteHeading' in sec['class']:
                    highlight, heading = list(sec.children)[1:3]
                    _, note_title, page_num = re.match(r'^((.*) > )?Page (\d+)', heading[len(') - '):]).groups()
                    note_text = sec.find_next('div', {'class': 'noteText'}).string
                    note_text = note_text.replace(' .', '.').replace(' ?', '?').replace(' ;', ';').replace(' !', '!')
                    note_text = note_text.replace(' ,', ',')
                    results.append({
                        'section': curr_section,
                        'chapter': note_title,
                        'contents': note_text,
                        'metadata': {
                            'color': highlight.string,
                            'page_num': int(page_num),
                        },
                    })

            return {
                'title': soup.select('div.bookTitle')[0].string,
                'segments': results,
            }

        return None

import os
from IPython.nbformat import current as nbformat
import itertools


def notebooks_in_directory(directory):
    for fname in os.listdir(directory):
        if fname.endswith('.ipynb'):
            yield os.path.join(directory, fname)


def read_notebook(fname):
    with open(fname) as fh:
        notebook = nbformat.reads(''.join(fh.readlines()), format='ipynb')
        return notebook


def notebooks_by_keyword(notebook_fnames):
    result = {}
    for notebook_fname in notebook_fnames:
        notebook = read_notebook(notebook_fname)
        for keyword in notebook['metadata'].get('keywords', []):
            result.setdefault(keyword, []).append(notebook_fname)
    return result


def notebook_rst(notebook_fname):
    notebook = read_notebook(notebook_fname)
    return 'todo'


def build_gallery(examples_directory, target_directory):
    notebook_fnames = list(notebooks_in_directory(examples_directory))
    print 'Fnames:', notebook_fnames

    template = """ * {} <thumbnail>\n"""
    
    gallery_content = []

    examples_directory = os.path.join(target_directory, 'gallery')
    if not os.path.isdir(examples_directory):
        os.makedirs(examples_directory)

    gallery_page_fname = os.path.join(target_directory, 'gallery.rst')

    for keyword, fnames in notebooks_by_keyword(notebook_fnames).items():
        gallery_content.append('\n\nSection: {}\n{}\n\n'.format(keyword, '-' * len(keyword)))
        for fname in fnames:
            gallery_content.append(template.format(os.path.basename(fname)))
            name = os.path.splitext(os.path.basename(fname))[0]
            page_content_fname = os.path.join(examples_directory,  name + '.rst')
            with open(page_content_fname, 'w') as fh:
                fh.writelines(notebook_rst(fname))

    with open(gallery_page_fname, 'w') as gallery_page:
        gallery_page.writelines(gallery_content)


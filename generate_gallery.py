import os
from IPython.nbformat import current as nbformat
import itertools
from IPython.nbconvert import RSTExporter
import io


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


def convert_to_rst(notebook, resources, target_directory):
    """Return a list of strings representing the rst of the given notebook."""
    exporter = RSTExporter()

    rst, resources = exporter.from_notebook_node(notebook, resources)
    rst = rst.split('\n')

    # Convert linked resources (such as images) into actual files in the
    # source directory.
    for name, data in resources.get('outputs', {}).items():
        if name.startswith('/'):
            name = target_directory + name
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))

        with io.open(name, 'wb') as f:
            f.write(data)

    return rst


def notebook_rst(notebook_fname, refname, target_directory):
    notebook = read_notebook(notebook_fname)
    template = u"""\n.. _{ref}:\n\n\n{content}\n\n"""

    output = os.path.join(target_directory, 'notebook_outputs')
    if not os.path.isdir(output):
        os.makedirs(output)
    resources = dict(unique_key=refname,
                     output_files_dir='/' + output)

    content = convert_to_rst(notebook, resources, output)
    return template.format(content=u'\n'.join(content), ref=refname)


def build_gallery(examples_directory, target_directory):
    notebook_fnames = list(notebooks_in_directory(examples_directory))

    template = """ * :ref:`{refname}` <thumbnail>\n"""
    
    gallery_content = []

#     target_directory = os.path.abspath(target_directory)
    examples_directory = os.path.join(target_directory, 'gallery')
    if not os.path.isdir(examples_directory):
        os.makedirs(examples_directory)

    gallery_page_fname = os.path.join(target_directory, 'gallery.rst')

    for fname in notebook_fnames:
        name = os.path.splitext(os.path.basename(fname))[0]
        page_content_fname = os.path.join(examples_directory,  name + '.rst')
        refname = 'gallery-{}'.format(name.replace('_', '-'))
        with open(page_content_fname, 'w') as fh:
            fh.write(notebook_rst(fname, refname, examples_directory).encode('utf-8'))

    for keyword, fnames in notebooks_by_keyword(notebook_fnames).items():
        gallery_content.append('\n\nSection: {}\n{}\n\n'.format(keyword, '-' * (len(keyword) + 10)))
        for fname in fnames:
            name = os.path.splitext(os.path.basename(fname))[0]
            page_content_fname = os.path.join(examples_directory,  name + '.rst')
            refname = 'gallery-{}'.format(name.replace('_', '-'))
            
            gallery_content.append(template.format(refname=refname, content=os.path.basename(fname)))

    with open(gallery_page_fname, 'w') as gallery_page:
        gallery_page.writelines(gallery_content)


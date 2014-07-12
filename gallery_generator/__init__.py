import os
from IPython.nbformat import current as nbformat
import itertools
from IPython.nbconvert import HTMLExporter
import io


def notebooks_in_directory(directory):
    for fname in os.listdir(directory):
        if fname.endswith('.ipynb'):
            yield os.path.join(directory, fname)


def read_notebook(fname):
    with open(fname) as fh:
        notebook = nbformat.reads(''.join(fh.readlines()), format='ipynb')
        return notebook


def convert_to_html(notebook, resources, target_directory):
    """Return a list of strings representing the rst of the given notebook."""
    exporter = HTMLExporter(template_file='gallery_page', template_path=[os.path.dirname(__file__)])
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


def notebook_html(notebook_fname, refname, target_directory):
    notebook = read_notebook(notebook_fname)

    output = os.path.join(target_directory, 'notebook_outputs')
    if not os.path.isdir(output):
        os.makedirs(output)
    resources = dict(unique_key=refname,
                     output_files_dir='/' + output)

    content = convert_to_html(notebook, resources, output)
    return u'\n'.join(content)


def build_gallery(examples_directory, target_directory):
    notebook_fnames = list(notebooks_in_directory(examples_directory))
    
    examples_directory = os.path.join(target_directory, 'gallery')
    if not os.path.isdir(examples_directory):
        os.makedirs(examples_directory)

    gallery_page_fname = os.path.join(target_directory, 'gallery.html')

    exporter = HTMLExporter(template_file='gallery', template_path=[os.path.dirname(__file__)])
    exporter._load_template()
    exporter = exporter.template

    sections = []

    notebook_keywords = {}
    for notebook_fname in notebook_fnames:
        notebook = read_notebook(notebook_fname)
        notebook_keywords[notebook_fname] = notebook['metadata'].get('keywords', [])

    notebooks_by_keyword = {}
    for notebook_fname, keywords in notebook_keywords.items():
        for keyword in keywords:
            notebooks_by_keyword.setdefault(keyword, []).append(notebook_fname)

    import collections
    Section = collections.namedtuple('Section', ['name', 'examples'])
    Example = collections.namedtuple('Example', ['name', 'url', 'keywords'])


    for fname in notebook_fnames:
        name = os.path.splitext(os.path.basename(fname))[0]
        page_content_fname = os.path.join(examples_directory, name + '.html')
        refname = 'gallery-{}'.format(name.replace('_', '-'))
        with open(page_content_fname, 'w') as fh:
            fh.write(notebook_html(fname, refname, examples_directory).encode('utf-8'))


    for keyword, fnames in notebooks_by_keyword.items():
        section = Section(keyword, [])
        sections.append(section)
        for fname in fnames:
            name = os.path.splitext(os.path.basename(fname))[0]
            example = Example(name, 'gallery/{}.html'.format(name), notebook_keywords[fname])
            section.examples.append(example)

    with open(gallery_page_fname, 'w') as gallery_page:
        gallery_page.write(exporter.render(title='foobar', sections=sections))


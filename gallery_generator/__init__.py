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
    exporter = HTMLExporter(template_file='gallery_page', template_path=[os.path.dirname(__file__)],
                            config={'ExtractOutputPreprocessor':{'enabled':True}})
    resources.update({'output_files_dir': 'notebook_output'})
    html, resources = exporter.from_notebook_node(notebook, resources)

    # Convert linked resources (such as images) into actual files in the
    # source directory.
    for name, data in resources.get('outputs', {}).items():
        name = os.path.join(target_directory, name)
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))

        with io.open(name, 'wb') as f:
            f.write(data)

    return html, resources.get('outputs', {}).keys()


def notebook_html(notebook_fname, refname, target_directory):
    notebook = read_notebook(notebook_fname)

    resources = dict(unique_key=refname)

    content, output_files = convert_to_html(notebook, resources, target_directory)
    return content, output_files


def build_gallery(examples_directory, target_directory):
    notebook_fnames = list(notebooks_in_directory(examples_directory))
    
    examples_dir_name = 'examples'
    examples_directory = os.path.join(target_directory, examples_dir_name)
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
    Example = collections.namedtuple('Example', ['name', 'url', 'keywords', 'outputs'])

    examples_by_fname = {}

    for fname in notebook_fnames:
        name = os.path.splitext(os.path.basename(fname))[0]
        page_content_fname = os.path.join(examples_directory, name + '.html')
        refname = 'gallery-{}'.format(name.replace('_', '-'))
        with open(page_content_fname, 'w') as fh:
            html, outputs = notebook_html(fname, refname, examples_directory)
            fh.write(html.encode('utf-8'))

        images = []
        for output in outputs:
            thumb_path = examples_dir_name + '/' + 'notebook_output_thumbs' + '/' + os.path.basename(output)
            thumb_fname = os.path.join(target_directory, thumb_path)
            orig_fname = os.path.join(examples_directory, output)
            if not os.path.exists(os.path.dirname(thumb_fname)):
                os.makedirs(os.path.dirname(thumb_fname))
            import shutil
            # TODO - resize these.
            shutil.copy(orig_fname, thumb_fname)
            images.append(thumb_path)

#         outputs = [examples_dir_name + '/' + image for image in images]

        example = Example(name, '{}/{}.html'.format(examples_dir_name, name),
                          notebook_keywords[fname],
                          images)
        examples_by_fname[fname] = example
        break

    for keyword, fnames in notebooks_by_keyword.items():
        section = Section(keyword, [])
        sections.append(section)
        for fname in fnames:
            name = os.path.splitext(os.path.basename(fname))[0]
            if fname in examples_by_fname:
                section.examples.append(examples_by_fname[fname])

    with open(gallery_page_fname, 'w') as gallery_page:
        gallery_page.write(exporter.render(title='Gallery', sections=sections))


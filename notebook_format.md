#Format for Example Notebooks
##General
Place the title of the example (not including the section) at the top of the notebook in a Heading 1 cell. 
For example, if the full title of the example is `images_contours_and_fields example code: image_demo.py`, then write the title as `Image Demo` and also title the notebook the same but with underscores, which would be `Image_Demo` in this case.

##Code
Place the code from the original example into code cells in notebook, separate the cells where it is needed and/or make sense in the context of the example.

##Metadata
The metadata of the notebook can be edited by clicking ‘Edit Notebook Metadata’ in the Edit Menu. By default, the metadata will look something like this:
```json
{
  "name": "",
  "signature": "sha256:52b3805edbda44d709560e8f109b2ec3c4db13121a76531da79e7a0f4e3701ff"
}
```
Add the original title and keywords from the original example in the format shown below. Make sure to add a comma at the end of the signature line, which will likely be cut off due to its length.
**For many of the examples in the gallery, the keywords are not very specific, so feel free to add more specific keywords, such as `image`, or `scatter`.
```json
{
  "name": "",
  "signature": "sha256:52b3805edbda44d709560e8f109b2ec3c4db13121a76531da79e7a0f4e3701ff",
  "title": "images_contours_and_fields example code: image_demo.py",
  "keywords": [
    "python",
    "matplotlib",
    "pylab",
    "example",
    "codex"
  ]
}
```

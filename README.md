# barc - make sheets of barcode labels.

For various kinds of inventory management, it is convenient to
be able to create neatly formatted pages with labelled barcodes.
For example, using a domestic inventory management system such as
[Grocy](https://github.com/grocy/grocy), we can:
 - make pages of barcode labels to stick on goods when we put them in the freezer
 - make a laminated sheet of common goods, such as fruit, for onvenient scanning

For use cases like the first, we want to make a sheet of labels with
the same barcode repeated, or perhaps half a sheet of one barcode, and
half a sheet of another. For the second case, we simply want to have a
sheet with many different labels, once each.

*Barc* is a tool for doing exatly these tasks. It works by reading
a [YAML](https://yaml.org/) specification for the page of labels,
and producing an HTML file using [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
to arrange the barcodes and text so they can be printed to suit sticky
label sheets such as those from [Avery](https://www.averyproducts.com.au/). 
To render the HTML+CSS accurately, we like [Prince](https://www.princexml.com/)
(Especially as it is made by a local company!), and use it in the docker
container for Barc.

The YAML for specifying a page of labels has the following form:

```yaml
version: '1'
options:
  barcode-type: <<barcode-type>>
  style: <<CSS styling to use>>
barcodes:
- - code: 123456789             # first row, first column
    label: 'Apple, green'
  - code: 234567890             # first row, second column
    label: 'Apple, red'
  ...
- - code: 567890123             # second row, first column
    label: 'Orange, Seville'
  ...
```

If no barcode type is given, `code128` is assumed.

If a style is given, it is added to the HTML with a link element.

It is assumed you know the number of rows and columns for your sheet of
labels, the dimensions of which will be described in the CSS.

Both the code and label in the specification are optional - the following rules are applied:
  - If the code is not specified but the label is, the label is used as the code. 
  - If the label is not specified, but the code is, the code is added as a label.
  - If the code is the empty string, or neither the code or label are given then
    a random code is generated.

## YAML Anchors and References

If you are making a sheet of labels which are all the same, the YAML
can become quite verbose, and awkward to modify. However, YAML contains
a nifty mechanism to allow you mark a part of the document tree, and
refer to it subsequently. For example, suppose we want to make a page
of barcodes for packages of chicken breasts for the freezer, we might
have a specification like the following:

```yaml
version: '1'
options:
  barcode-type: code128
  style: /style/L7160
barcodes:
- - code: CHICKBRST
    label: Chicken Breast
  - code: CHICKBRST
    label: Chicken Breast
  - code: CHICKBRST
    label: Chicken Breast
- - code: CHICKBRST
    label: Chicken Breast
  - code: CHICKBRST
    label: Chicken Breast
  - code: CHICKBRST
    label: Chicken Breast
...
```

YAML allows us to attach a label to the `{code: ..., label: ...}` map
node, and then refer to it after:

```yaml
version: '1'
options:
  barcode-type: code128
  style: /style/L7160
barcodes:
- - &CB code: CHICKBRST
    label: Chicken Breast
  - *CB
  - *CB
- - *CB
  - *CB
  - *CB
...
```

But we can go further, and attach a label to the row, and then replicate
the row:

```yaml
version: '1'
options:
  barcode-type: code128
  style: /style/L7160
barcodes:
- &ROW [&CB code: CHICKBRST, *CB, *CB]
- *ROW
- *ROW
- *ROW
- *ROW
- *ROW
- *ROW
```

With this brief form, the above YAML yields a full sheet of 21 (3x7)
L7160 labels.  (Note we switched between the _layout_ form and the
_inline_ form of the YAML for the row.)


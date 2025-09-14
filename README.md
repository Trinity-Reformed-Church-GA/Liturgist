# Liturgist
A liturgical document generator

## Installation

### Install from Source
```sh
git clone git@github.com:Trinity-Reformed-Church-GA/Liturgist.git
cd Liturgist
pip install .
```

### Development Installation
For development, install with development dependencies:
```sh
git clone git@github.com:Trinity-Reformed-Church-GA/Liturgist.git
cd Liturgist
pip install -e ".[dev]"
```

## System Requirements

* Python 3.9 or higher
* For PDF generation: `brew install pango` (macOS) or equivalent system dependency

## Usage

### Command Line Options

```
liturgist [OPTIONS] SCHEDULE

Arguments:
  SCHEDULE  Path to schedule file (CSV, ODS, XLSX, or XLS)

Options:
  --date TEXT           Date in YYYY-mm-dd format (defaults to next Sunday)
  --print-json          Print data as JSON instead of rendering template
  --bible-json-path     Path to Bible JSON file for scripture text lookup
  --template TEXT       Path to Handlebars template file
  -o, --output TEXT     Output file path (default: output/out.pdf)
  --help               Show this message and exit
```

### Print JSON Data
The simplest use of the tool is to print data as JSON from a spreadsheet.

```sh
liturgist --print-json liturgy.ods
```

Example output:
```json
{
  "DATE": "2024-02-18", 
  "FORMATTED_DATE": "Sunday, February 18, 2024", 
  "HYMNS": [
    "Hymn 290 - Hallelujah, Praise Jehovah", 
    "Hymn 620 - Stricken, Smitten, and Afflicted", 
    "Hymn 301 - Praise to the Lord, the Almighty", 
    "Hymn 403 - Our God, Our Help in Ages Past", 
    "Hymn 337 - Immortal, Invisible, God Only Wise", 
    "Hymn 537 - Rejoice, the Lord is King"
  ], 
  "SCRIPTURE": "Acts 2:34-35", 
  "PRAYER_VERSE": "Acts 2:36-37", 
  "ASSURANCE_VERSE": "Acts 5:30-31", 
  "OT_READING": "Genesis 22:1-18", 
  "NT_READING": "James 1:12-21", 
  "CATECHISM_QUESTION": "Q51. What is forbidden in the second commandment?", 
  "CATECHISM_ANSWER": "A. The second commandment forbiddeth the worshipping of God by images, or any other way not appointed in his Word.", 
  "BENEDICTION": "Ephesians 3:20-21"
}
```

You can pipe the output into [jq](https://jqlang.github.io/jq/) for formatting:
```sh
liturgist --print-json liturgy.ods | jq
{
  "DATE": "2024-02-11",
  "FORMATTED_DATE": "Sunday, February 11, 2024",
  "HYMNS": [
    "Hymn 387 - Guide Me, O Thou Great Jehovah",
    "Hymn 412 - Oh, the Deep, Deep Love of Jesus",
    "Hymn 347 - I sing the Mighty Power of God",
    "Hymn 335 - All Hail the Power of Jesus’ Name",
    "Hymn 337 - Immortal, Invisible, God Only Wise",
    "Hymn 537 - Rejoice, the Lord is King"
  ],
  "SCRIPTURE": "Hosea 2:23",
  "PRAYER_VERSE": "Hosea 5:15",
  "ASSURANCE_VERSE": "Hosea 6:1-2",
  "OT_READING": "Deuteronomy 10:12-22",
  "NT_READING": "Philippians 2:12-18",
  "CATECHISM_QUESTION": "Q50. What is required in the second commandment?",
  "CATECHISM_ANSWER": "A. The second commandment requireth the receiving, observing, and keeping pure and entire, all such religious worship and ordinances as God hath appointed in his Word.",
  "BENEDICTION": "2 Thessalonians 2:16-17",
  "BAPTISMS": "Ginger Rogers"
}
```

Or to query the data:
```sh
liturgist --print-json liturgy.ods | jq '.HYMNS[]'
```

Output:
```
"Hymn 290 - Hallelujah, Praise Jehovah"
"Hymn 620 - Stricken, Smitten, and Afflicted"
"Hymn 301 - Praise to the Lord, the Almighty"
"Hymn 403 - Our God, Our Help in Ages Past"
"Hymn 337 - Immortal, Invisible, God Only Wise"
"Hymn 537 - Rejoice, the Lord is King"
```

### Rendering a Handlebars Template
Handlebars is a templating language that enables parameterizing documents to be filled in with data at a later point.

An introduction: https://handlebarsjs.com/guide/

Essentially this is very fancy text replacement.

Say we wanted to create a markdown document with a bulleted list of the hymns:

1. Save a markdown template document that loops over all the values in the hymns array to `./hymn-list-template.md`:
```handlebars
# The Officiant Hymn List

{{#each HYMNS}}
* {{this}}
{{/each}}
```

2. Run liturgist:
```sh
liturgist liturgy.ods --template ./hymn-list-template.md -o hymn-list.md
```

3. `hymn-list.md` has been rendered as
```markdown
# The Officiant Hymn List

* Hymn 290 - Hallelujah, Praise Jehovah
* Hymn 620 - Stricken, Smitten, and Afflicted
* Hymn 301 - Praise to the Lord, the Almighty
* Hymn 403 - Our God, Our Help in Ages Past
* Hymn 337 - Immortal, Invisible, God Only Wise
* Hymn 537 - Rejoice, the Lord is King
```

#### PDF Rendering
HTML documents will be rendered to PDFs if the file extension of the output argument is `.pdf`.

#### DOCX and ODT Rendering
Markdown documents can be rendered to ODT (Open Document Text) or DOCX (Microsoft Word) formats:

```bash
liturgist ./liturgy.ods --template ./officiant-order-of-worship.md -o ./output/officiant-order-of-worship.odt --date 2024-03-03
```

## Supported File Formats

### Input Formats
- **Schedule files**: CSV, ODS, XLSX, XLS
- **Template files**: Any text-based format (HTML, Markdown, etc.)
- **Bible data**: JSON (schema should match [samples/kjv.json](samples/kjv.json)

### Output Formats
- **PDF**: Automatic when output file ends with `.pdf`
- **DOCX**: Microsoft Word format
- **ODT**: OpenDocument Text format  
- **Text**: Any other extension (HTML, Markdown, plain text, etc.)

## Template Variables

The following variables are available in templates:

- `DATE`: ISO format date (YYYY-MM-DD)
- `FORMATTED_DATE`: Human-readable date (e.g., "Sunday, February 18, 2024")
- `HYMNS`: Array of hymn titles
- `SCRIPTURE`: Main scripture reading
- `PRAYER_VERSE`: Prayer verse reference
- `ASSURANCE_VERSE`: Assurance verse reference
- `OT_READING`: Old Testament reading
- `NT_READING`: New Testament reading
- `CATECHISM_QUESTION`: Catechism question
- `CATECHISM_ANSWER`: Catechism answer
- `BAPTISMS`: Baptism information
- `COLLECT`: Collect prayer
- `CHURCH_OF_THE_MONTH`: Featured church
- `BENEDICTION_SCRIPTURE`: Benediction scripture reference

When using `--bible-json-path`, scripture text variables are also available with `_TEXT` suffix (e.g., `SCRIPTURE_TEXT`).

## Examples

### Basic JSON Export
```bash
liturgist --print-json schedule.xlsx
```

### Generate PDF from HTML Template
```bash
liturgist --template bulletin.html schedule.xlsx -o bulletin.pdf
```

### Generate Word Document for Specific Date
```bash
liturgist schedule.xlsx --template service.md -o "service-2024-03-03.docx" --date 2024-03-03
```

### Include Scripture Text
```bash
liturgist schedule.xlsx --template service.html --bible-json-path bible.json -o service.pdf
```




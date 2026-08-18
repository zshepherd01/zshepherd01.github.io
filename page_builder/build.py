from pathlib import Path
import sys
import pypandoc
import argparse
from datetime import datetime

DEFAULT_AUTHOR = "Zoey :3"
DEFAULT_URL = "https://zshepherd01.github.io/page_builder"
TEMPLATE_PATH = Path("template.html")

default_date = datetime.now().strftime("%B %Y")

parser = argparse.ArgumentParser(description="Builds a static HTML page from an RTF file.")

parser.add_argument("rtf_file", help="Path to the source .rtf file")
parser.add_argument("description", help="Short description of the work")

parser.add_argument("-t", "--title", help="Title of the work (defaults to name of the output file)")
parser.add_argument("-a", "--author", default=DEFAULT_AUTHOR, help="Author name (defaults to one hard-coded in the script)")
parser.add_argument("-u", "--url", help="Constant URL (defaults to one hard-coded in the script)")
parser.add_argument("-d", "--date", default=default_date, help="Display date (defaults to this month)")
parser.add_argument("-o", "--output", help="Output HTML file path (defaults to matching the input)")
parser.add_argument("-p", "--preview", help="Relative path to the preview image (defaults to matching the output file, required if url is given)")

args = parser.parse_args()

rtf_file = Path(args.rtf_file)
if not rtf_file.exists():
    print(f"Error: can't find {rtf_file}")
    sys.exit(1)

out_file = Path(args.output) if args.output else rtf_file.with_suffix(".html")

title = args.title or out_file.stem

url = args.url or f"{DEFAULT_URL}/{out_file}"

if args.url and not args.preview:
    print("Error: if you provide an explicit url, you must provide an explicit preview url too.")
previewrl = args.preview or f"{DEFAULT_URL}/{out_file.with_suffix('.png')}"

try:
    html_content = pypandoc.convert_file(rtf_file, 'html')
except Exception as e:
    print(f"Error converting file: {e}")
    sys.exit(1)

if not TEMPLATE_PATH.exists():
    print(f"Error: can't find template.")
    sys.exit(1)

template = TEMPLATE_PATH.read_text(encoding="utf-8")

final_html = template.replace('{{TITLE}}', title)
final_html = final_html.replace('{{URL}}', url)
final_html = final_html.replace('{{PREVIEWRL}}', previewrl)
final_html = final_html.replace('{{DESCRIPTION}}', args.description)
final_html = final_html.replace('{{AUTHOR}}', args.author)
final_html = final_html.replace('{{DATE}}', args.date)
final_html = final_html.replace('{{CONTENT}}', html_content)

out_file.write_text(final_html, encoding="utf-8")

print(f"Saved at {out_file}")

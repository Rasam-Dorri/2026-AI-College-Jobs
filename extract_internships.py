#!/usr/bin/env python3
"""
Extract internships from markdown files and create an Excel file.
"""

import re
import pandas as pd
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    """Strip HTML tags from text."""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text)

def strip_html(text):
    """Remove HTML tags from text."""
    s = HTMLStripper()
    s.feed(text)
    return s.get_data().strip()

def extract_url_from_html(text):
    """Extract URL from HTML anchor tag."""
    match = re.search(r'href="([^"]+)"', text)
    return match.group(1) if match else ''

def parse_markdown_table(lines, has_salary=False):
    """Parse markdown table and extract internship data."""
    internships = []

    # Find table start and end markers
    in_table = False

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Check if this is a table row (starts with |)
        if line.strip().startswith('|') and '---' not in line:
            # Skip header row
            if 'Company' in line and 'Position' in line:
                continue

            # Parse data row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove first and last empty elements

            if len(cells) >= 5:  # Valid data row
                company_html = cells[0]
                position = strip_html(cells[1])
                location = strip_html(cells[2])

                # Extract company name and URL
                company_name = strip_html(company_html)
                company_url = extract_url_from_html(company_html)

                if has_salary:
                    # USA format: Company | Position | Location | Salary | Posting | Age
                    salary = strip_html(cells[3])
                    posting_html = cells[4]
                    age = strip_html(cells[5]) if len(cells) > 5 else ''
                else:
                    # International format: Company | Position | Location | Posting | Age
                    salary = ''
                    posting_html = cells[3]
                    age = strip_html(cells[4]) if len(cells) > 4 else ''

                # Extract application URL
                apply_url = extract_url_from_html(posting_html)

                # Only add if we have valid data
                if company_name and position:
                    internships.append({
                        'Company': company_name,
                        'Position': position,
                        'Location': location,
                        'Salary': salary,
                        'Application URL': apply_url,
                        'Company URL': company_url,
                        'Age (days)': age.replace('d', '').strip()
                    })

    return internships

def main():
    print("Extracting internships from markdown files...")

    # Read USA internships (with salary)
    print("Reading USA internships...")
    with open('/home/user/2026-AI-College-Jobs/README.md', 'r', encoding='utf-8') as f:
        usa_lines = f.readlines()

    # Read International internships (without salary)
    print("Reading International internships...")
    with open('/home/user/2026-AI-College-Jobs/INTERN_INTL.md', 'r', encoding='utf-8') as f:
        intl_lines = f.readlines()

    # Parse USA internships
    usa_internships = parse_markdown_table(usa_lines, has_salary=True)
    for internship in usa_internships:
        internship['Region'] = 'USA'

    # Parse International internships
    intl_internships = parse_markdown_table(intl_lines, has_salary=False)
    for internship in intl_internships:
        internship['Region'] = 'International'

    # Combine all internships
    all_internships = usa_internships + intl_internships

    print(f"Found {len(usa_internships)} USA internships")
    print(f"Found {len(intl_internships)} International internships")
    print(f"Total: {len(all_internships)} internships")

    # Create DataFrame
    df = pd.DataFrame(all_internships)

    # Reorder columns
    column_order = ['Region', 'Company', 'Position', 'Location', 'Salary', 'Application URL', 'Company URL', 'Age (days)']
    df = df[column_order]

    # Save to Excel
    output_file = '/home/user/2026-AI-College-Jobs/AI_Internships_2026.xlsx'
    df.to_excel(output_file, index=False, sheet_name='AI Internships 2026')

    print(f"\n✓ Successfully created: {output_file}")
    print(f"  Total internships: {len(all_internships)}")
    print(f"  - USA: {len(usa_internships)}")
    print(f"  - International: {len(intl_internships)}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Validate independently installable Agent Skills without extra dependencies."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
skills = sorted((root / 'skills').glob('*/SKILL.md'))
assert skills, 'No skills found'
for skill in skills:
    content = skill.read_text(encoding='utf-8')
    assert content.startswith('---\n'), f'{skill}: missing YAML frontmatter'
    header = content.split('---', 2)[1]
    name = re.search(r'^name:\s*(.+)$', header, re.MULTILINE)
    description = re.search(r'^description:\s*(.+)$', header, re.MULTILINE)
    assert name and name.group(1).strip() == skill.parent.name, f'{skill}: invalid name'
    assert description and description.group(1).strip(), f'{skill}: missing description'
    assert content.split('---', 2)[2].strip(), f'{skill}: empty instructions'
print(f'Validated {len(skills)} skills')

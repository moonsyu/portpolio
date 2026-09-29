"""Check actual generated board text bounds, collisions, and retained facts."""
from collections import defaultdict
import re
from design_board import Board, width, AWARDS, TIMELINE, UART
from build_design_ac import make_a, make_c
from build_design_b import build

original = Board.text
layouts = defaultdict(list)

def record(self, x, y, value, size=24, weight=600, color='#211C37', anchor='start'):
    assert '\n' not in value, f'Use para() for multiline text: {value}'
    tw = width(value, size, weight)
    left = x - (tw if anchor == 'end' else tw / 2 if anchor == 'middle' else 0)
    layouts[self.filename].append((left, y, left + tw, y + size, value))
    assert left >= 0 and left + tw <= self.width, f'{self.filename}: horizontal overflow: {value}'
    assert y >= 0 and y + size <= self.height, f'{self.filename}: vertical overflow: {value}'
    return original(self, x, y, value, size, weight, color, anchor)

Board.text = record
make_a()
build()
make_c()
for filename, boxes in layouts.items():
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if min(a[2], b[2]) > max(a[0], b[0]) + 1 and min(a[3], b[3]) > max(a[1], b[1]) + 1:
                raise AssertionError(f'{filename}: text overlap: {a[4]} / {b[4]}')
    text = re.sub(r'\s+', '', ''.join(box[4] for box in boxes))
    expected = ['Jang MoonSu', '2024.10.02', '2026.09.14', 'Intermediate Low', 'STM-Simulator']
    expected += [fact for award in AWARDS for fact in award]
    expected += [fact for event in TIMELINE for fact in event]
    expected += [body for _, body in UART]
    for fact in expected:
        assert re.sub(r'\s+', '', fact) in text, f'{filename}: omitted fact: {fact}'
    print(f'{filename}: bounds, text collisions, retained facts OK ({len(boxes)} text lines)')

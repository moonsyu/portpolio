"""Build the explicitly unimplemented Arabica reflection diagram."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="650" viewBox="0 0 1280 650" role="img" aria-labelledby="title desc">
<title id="title">Arabica 추가 보완 설계 — 미구현 제안</title>
<desc id="desc">작업 ID와 상태를 저장하고, 실행량을 제한한 실행기에서 전용 계정으로 원격 백업 수행. 인증된 완료 알림을 받아 결과를 검증한 뒤 완료를 확정. 알림 누락 시 주기 재확인, 중복 결과는 작업 ID로 구분하여 한 번만 반영하는 제안.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 10 5 0 10Z" fill="#2355de"/></marker></defs>
<style>text{font-family:'Segoe UI','Malgun Gothic',sans-serif;fill:#172538}.title{font-size:32px;font-weight:750}.heading{font-size:27px;font-weight:750}.body{font-size:23px;font-weight:600}.small{font-size:21px;font-weight:600}.blue{fill:#2355de}.muted{fill:#5b687a}</style>
<rect width="1280" height="650" rx="12" fill="#fff"/>
<text x="44" y="58" class="title">실행 요청부터 완료 판정까지, 작업 단위로 추적</text>
<rect x="44" y="82" width="246" height="43" rx="7" fill="#eef3ff"/>
<text x="62" y="111" class="small blue">추가 보완안 · 미구현</text>
''']

def icon(name, x, y):
    source = (ROOT / 'assets/architecture/icons' / f'{name}.svg').read_text(encoding='utf-8')
    body = re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', source, flags=re.S).replace('currentColor', '#2355de')
    return f'<svg x="{x}" y="{y}" width="58" height="58" viewBox="0 0 24 24" fill="none" stroke="#2355de" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

nodes = [
    (44, 'database', '작업 접수', ['작업 ID·상태 저장', '예약 작업을 실행 대기']),
    (346, 'workflow', '전용 실행기', ['동시 실행·대기량 제한', '초과 요청은 재시도 관리']),
    (648, 'database-backup', '원격 백업', ['전용 계정·허용 명령', '백업 결과와 작업 ID 연결']),
    (950, 'shield-check', '결과 검증·이력', ['인증된 완료 알림 수신', '검증 후 완료 상태 확정']),
]
for x, name, heading, lines in nodes:
    parts.append(f'<rect x="{x}" y="167" width="286" height="254" rx="13" fill="#f8fafc" stroke="#dce3ed" stroke-width="2"/>')
    parts.append(icon(name, x+114, 192))
    parts.append(f'<text x="{x+143}" y="294" text-anchor="middle" class="heading">{escape(heading)}</text>')
    for i,line in enumerate(lines):
        parts.append(f'<text x="{x+143}" y="{337+i*36}" text-anchor="middle" class="small">{escape(line)}</text>')
for x in [330,632,934]:
    parts.append(f'<path d="M{x-3} 270H{x+14}" stroke="#2355de" stroke-width="2.4" marker-end="url(#arrow)"/>')
parts.append('''<path d="M1093 423V451H791V423" fill="none" stroke="#2355de" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#arrow)"/>
<rect x="826" y="437" width="241" height="30" fill="#fff"/>
<text x="946" y="459" text-anchor="middle" class="small blue">알림 누락 시 주기 재확인</text>
<rect x="44" y="499" width="1192" height="108" rx="10" fill="#eef3ff"/>
<text x="640" y="541" text-anchor="middle" class="heading blue">대기 → 실행 → 검증 → 완료 / 실패</text>
<text x="640" y="579" text-anchor="middle" class="body">타임아웃으로 미완료 작업 식별 · 동일 작업 ID의 결과는 한 번만 반영</text>
</svg>''')
target = ROOT / 'assets/flows/arabica-reflection.svg'
target.write_text('\n'.join(parts), encoding='utf-8')
print(target)

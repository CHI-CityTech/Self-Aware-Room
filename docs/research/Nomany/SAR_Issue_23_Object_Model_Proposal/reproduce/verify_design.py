from pathlib import Path
import ast
import csv
import inspect
import json
import re
import sys
import types
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit

ROOT = Path('/workspace/scratch/b65e59c0fbe4/projects/SAR-Issue-23-Object-Model')
ANALYSIS = Path('/workspace/scratch/b65e59c0fbe4/analysis/issue23_object_model_2026-10-28')
DOC = ROOT / 'docs/computational/proposals/issue-23/SAR_Object_Abstraction_and_Interface_Proposal_V1_2026-10-28.md'
sys.path.insert(0, str(ROOT / 'src'))
from sar_core.contracts import models as baseline
from sar_core.contracts.stages import StageComponent
from sar_core.stages.o1_observability import O1ObservabilityComponent

source = (ROOT / 'src/sar_core/contracts/models.py').read_text()
tree = ast.parse(source)
tree.body.insert(2, ast.ImportFrom(module='abc', names=[ast.alias(name='ABC'), ast.alias(name='abstractmethod')], level=0))
for node in tree.body:
    if isinstance(node, ast.ClassDef) and node.name == 'DataObject':
        node.bases.append(ast.Name(id='ABC', ctx=ast.Load()))
        for member in node.body:
            if isinstance(member, ast.FunctionDef) and member.name == '__post_init__':
                member.decorator_list.append(ast.Name(id='abstractmethod', ctx=ast.Load()))
ast.fix_missing_locations(tree)
candidate = types.ModuleType('sar_core.contracts.issue23_review_only')
candidate.__package__ = 'sar_core.contracts'
sys.modules[candidate.__name__] = candidate
exec(compile(tree, '<in-memory issue23 candidate, not applied>', 'exec'), candidate.__dict__)

def cannot_construct(cls):
    try:
        cls()
    except TypeError:
        return True
    return False

assert inspect.isabstract(candidate.DataObject) and cannot_construct(candidate.DataObject)
class Incomplete(candidate.DataObject):
    pass
assert inspect.isabstract(Incomplete) and cannot_construct(Incomplete)
class BaselineIncomplete(baseline.DataObject):
    pass
assert isinstance(BaselineIncomplete(), baseline.DataObject)

inventory = json.loads((ANALYSIS / 'source_inventory.json').read_text())
subtypes = [name for name, info in inventory.items() if 'DataObject' in info['bases']]
assert len(subtypes) == 10
constructed = []
for name in subtypes:
    cls = getattr(candidate, name)
    assert not inspect.isabstract(cls), name
    value = cls()
    expected = getattr(baseline, name)().object_type.value
    assert value.object_type.value == expected, name
    constructed.append(name)

a, b = candidate.Observation(), candidate.Observation()
assert a.object_id != b.object_id
assert a.payload is not b.payload
assert a.provenance is not b.provenance
assert a.provenance.parent_object_ids is not b.provenance.parent_object_ids
assert a.time_context is not b.time_context
event = candidate.Event(observation_ids=['obs-1'])
event.add_observation_ids(['obs-1', 'obs-2', 'obs-2'])
assert event.observation_ids == ['obs-1', 'obs-2']
assert event.provenance.parent_object_ids == ['obs-1', 'obs-2']
assert not issubclass(StageComponent, baseline.DataObject)
assert not issubclass(O1ObservabilityComponent, baseline.EvaluationRecord)

snippet = re.search(r'```python\n(.*?)\n```', DOC.read_text(), re.S).group(1)
sketch = types.ModuleType('issue23_document_sketch')
sys.modules[sketch.__name__] = sketch
exec(compile(snippet, '<proposal snippet>', 'exec'), sketch.__dict__)
assert cannot_construct(sketch.DataObject)
assert sketch.Observation(source_id='example').source_id == 'example'

with (ROOT / 'docs/assets/issue23/field_inventory.csv').open() as f:
    rows = list(csv.DictReader(f))
for row in rows:
    line = (ROOT / row['source_path']).read_text().splitlines()[int(row['source_line']) - 1]
    assert row['field'] + ':' in line, row
assert len([r for r in rows if r['owner'] == 'DataObject']) == 8
assert {r['owner'] for r in rows if r['classification'] == 'subtype-specific contract'} == set(subtypes)

links = []
for f in [DOC]:
    content = re.sub(r'```.*?```', '', f.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^)]+)\)', content):
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith('#'):
            continue
        exists = (f.parent / unquote(parsed.path)).resolve().exists()
        links.append({'target': target, 'exists': exists})
assert all(v['exists'] for v in links), links

diagram_labels = []
for f in sorted((ROOT / 'docs/assets/issue23').glob('*.svg')):
    svg = ET.parse(f)
    diagram_labels.extend(n.text for n in svg.iter() if n.tag.endswith('text') and n.text)
assert all(name in diagram_labels for name in subtypes)
assert all(any(field in text for text in diagram_labels) for field, _, _ in inventory['DataObject']['fields'])
cases = re.findall(r'^\| (OBJ-\d+) \|', DOC.read_text(), flags=re.M)
assert cases == [f'OBJ-{i:02}' for i in range(1, 19)]

report = {
    'status': 'passed',
    'baseline_commit': '8c99abecd723a39370455ba9e27adca2cea872b1',
    'inspection': {'data_object_fields': 8, 'concrete_subtypes': constructed,
                   'field_inventory_rows': len(rows), 'source_line_checks': len(rows),
                   'local_proposal_targets': len(links), 'class_diagrams_rendered': 5},
    'isolated_design_checks': [
        'OBJ-01: proposed abstract base cannot be constructed',
        'OBJ-02: incomplete direct child cannot be constructed',
        'OBJ-03: all ten concrete categories construct with correct tags',
        'OBJ-04: independent default metadata and payload instances',
        'OBJ-05: Event observation and parent lists deduplicate consistently',
        'OBJ-06: stages/observer are separate from data artifacts',
        'Published Python sketch executes and constructs its concrete Observation',
        'Baseline manual guard permits an incomplete subclass, confirming the formal-ABC gap',
    ],
    'design_cases_not_executed': [f'OBJ-{i:02}' for i in range(7, 19)],
    'limits': [
        'Candidate ABC changes executed only in an isolated in-memory module. No production code changed.',
        'No full pipeline, mypy/interface conformance, schema migration, hardware, or profile-validator tests were run.',
        'Remaining acceptance cases require reviewed implementation and integration evidence.',
    ],
}
(ANALYSIS / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

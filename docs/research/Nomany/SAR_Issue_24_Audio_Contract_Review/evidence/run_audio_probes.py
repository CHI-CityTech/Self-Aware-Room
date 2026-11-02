from pathlib import Path
from dataclasses import asdict, fields
from datetime import datetime, timezone
from hashlib import sha256
import json
import sys

ROOT = Path('/workspace/scratch/b65e59c0fbe4/projects/SAR-Issue-24-Audio-Contract')
OUT = Path('/workspace/scratch/b65e59c0fbe4/analysis/issue24_audio_review_2026-10-28')
STORAGE = OUT / 'synthetic_storage'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'src'))
from sar_core.contracts.edge_ingress import EdgeObservationFrame, observation_from_edge_frame
from sar_core.contracts.models import DataObject, Observation
from sar_core.stages.l1_acquisition import L1AcquisitionStage
from sar_core.stages.l2_normalization import L2NormalizationStage
from sar_core.stages.o1_observability import O1ObservabilityComponent
from sar_core.storage.raw_store import LocalFileRawStore

results = []

def record(identifier, name, observed, interpretation, context=None):
    results.append({'probe_id': identifier, 'name': name, 'observed': observed,
                    'interpretation': interpretation, 'context': context or {}})

def frame(payload=None, **overrides):
    args = dict(source_node_id='synthetic-node', source_id='synthetic-mic-a', modality='audio',
                encoding='pcm16', sample_rate_hz=48000, channel_count=2, frame_index=0,
                source_frame_id='native-frame-0', source_capture_time=datetime(2026, 10, 28, 18, tzinfo=timezone.utc),
                payload={'sample_format':'pcm_s16le','bit_depth':16,'raw_audio_chunk':[0,200,-200,0]})
    if payload is not None: args['payload'] = payload
    args.update(overrides)
    return EdgeObservationFrame(**args)

def ingest(value, store=None, telemetry=None):
    seed = observation_from_edge_frame(value)
    response = L1AcquisitionStage(raw_store=store, telemetry=telemetry).process([seed])
    assert len(response.output_objects) == 1
    return seed, response, response.output_objects[0]

seed, response, obj = ingest(frame())
assert response.status.value == 'ok'
assert obj.object_id != seed.object_id and seed.object_id in obj.provenance.parent_object_ids
assert obj.time_context.receipt_time and obj.time_context.processing_time
assert obj.payload['sample_format'] == 'pcm_s16le' and obj.payload['bit_depth'] == 16
record('P01','Complete inline audio follows structural acquisition path',
       {'stage_status':response.status.value,'all_common_fields_present':all(hasattr(obj,f.name) for f in fields(DataObject)),
        'precision_metadata_preserved':True,'new_object_id':True,'parent_link_preserved':True,
        'receipt_and_processing_stamped':True},
       'Positive structural evidence only. Does not establish full audio conformance.')

_, response, obj = ingest(frame(payload={'raw_audio_chunk':[0,200,-200,0]}))
assert response.status.value == 'ok' and 'sample_format' not in obj.payload and 'bit_depth' not in obj.payload
record('P02','Missing required audio precision information accepted',
       {'stage_status':response.status.value,'sample_format_present':False,'bit_depth_present':False},
       'L1 does not enforce the explicit sample_format-or-bit_depth requirement in D01.02.01 section 4.')

try:
    EdgeObservationFrame(source_node_id='synthetic-node',source_id='synthetic-temperature',
                         modality='environmental',frame_index=0,payload={'temperature':22})
except TypeError as error:
    record('P03','Five-field non-audio envelope cannot be constructed',{'constructed':False,'error':str(error)},
           'The current transport constructor forces audio-related fields onto the generalized envelope. This is not a full environmental-profile test.')
else:
    raise AssertionError('Expected baseline constructor mismatch')

gates={'gate_state':'open','threshold_on_dbfs':-40.0,'threshold_off_dbfs':-44.0,
       'pre_roll_ms':500,'post_roll_ms':800,'dropped_by_policy':False,'capture_policy':'hybrid'}
payload={'sample_format':'pcm_s16le','bit_depth':16,'raw_audio_chunk':[0,200,-200,0],**gates}
store=LocalFileRawStore(base_dir=str(STORAGE))
_, response, obj = ingest(frame(payload=payload),store=store)
stored_path=Path(obj.payload['raw_ref_uri'])
stored_bytes=stored_path.read_bytes()
stored=json.loads(stored_bytes)
missing=sorted(set(['sample_format','bit_depth',*gates])-obj.payload.keys())
assert missing and all(key in stored for key in missing)
assert sha256(stored_bytes).hexdigest()==obj.payload['checksum_sha256']
assert len(stored_bytes)==obj.payload['byte_size']
record('P04','Reference-storage path removes direct precision and gating metadata',
       {'stage_status':response.status.value,'metadata_absent_from_emitted_payload':missing,
        'metadata_still_in_stored_artifact':True,'checksum_verified':True,'byte_size_verified':True,
        'stored_fixture':str(stored_path.relative_to(OUT)),'checksum_sha256':obj.payload['checksum_sha256'],
        'emitted_payload_keys':sorted(obj.payload)},
       'Metadata is not destroyed, but downstream consumers must resolve storage to recover it. The contract needs an explicit direct-metadata/reference-resolution rule.',
       {'gating_policy_assumption':'enabled for this fixture; no runtime gating configuration is implemented by this probe'})

_, response, obj=ingest(frame(payload={'sample_format':'pcm_s16le','bit_depth':16,
                                     'raw_audio_chunk':[0,200,-200,0],'gate_state':'open','capture_policy':'selective'}))
required=set(gates)
absent=sorted(required-obj.payload.keys())
assert response.status.value=='ok' and absent
record('P05','Incomplete gating metadata accepted under enabled-gating interpretation',
       {'stage_status':response.status.value,'missing_conditional_fields':absent},
       'No conditional profile validation is performed. The driver assumes enabled gating. It does not claim to have enabled an implemented runtime gating feature.',
       {'gating_enabled_in_review_context':True})

seeds=[observation_from_edge_frame(frame(frame_index=n,source_frame_id=f'native-{n}')) for n in [2,1]]
response=L1AcquisitionStage().process(seeds)
indexes=[o.payload['frame_index'] for o in response.output_objects]
assert indexes==[2,1] and response.status.value=='ok'
record('P06','Descending frame indices accepted for one source in one fixture sequence',
       {'stage_status':response.status.value,'emitted_indices':indexes},
       'This acquisition path does not enforce monotonic ordering. Stream/session/reset semantics still need an agreed validator boundary.',
       {'same_source_session_assumed':True})

_, response, obj=ingest(frame(payload={'sample_format':'pcm_s16le','bit_depth':16,'raw_audio_chunk':[0,200,-200,0],
                                     'encoding':'opus','modality':'video','source_node_id':'payload-shadow'}))
assert obj.payload['encoding']=='opus' and obj.payload['modality']=='video'
record('P07','Payload entries override conflicting outer frame metadata',
       {'outer_encoding':'pcm16','emitted_encoding':obj.payload['encoding'],'outer_modality':'audio',
        'emitted_modality':obj.payload['modality'],'emitted_source_node_id':obj.payload['source_node_id'],
        'stage_status':response.status.value},
       'The adapter merge has precedence behavior that the written contract does not specify. Recommend rejecting conflicting declarations.')

seed,response,obj=ingest(frame(source_frame_id='native-explicit-42'))
assert obj.provenance.source_native_id=='native-explicit-42'
assert obj.object_id!=seed.object_id
record('P08','Native identity and canonical object identity remain separate',
       {'native_id_preserved':True,'new_derived_object_id':True,'parent_link_preserved':seed.object_id in obj.provenance.parent_object_ids},
       'Positive identity/lineage evidence on this path.')

objects=[observation_from_edge_frame(frame(source_id=s,source_frame_id=None)) for s in ['synthetic-mic-a','synthetic-mic-b']]
native=[o.provenance.source_native_id for o in objects]
assert native[0]==native[1] and objects[0].object_id!=objects[1].object_id
record('P09','Generated fallback frame labels collide across two streams',
       {'generated_native_values':native,'canonical_object_ids_distinct':True},
       'The fallback ignores source_id. Canonical SAR object IDs did not collide.')

_,response,obj=ingest(frame(source_capture_time=None,source_frame_id=None))
prov_fields=[f.name for f in fields(obj.provenance)]
assert obj.time_context.source_capture_time is not None
record('P10','Estimated capture time has no explicit field-origin marker',
       {'capture_time_filled':True,'provenance_fields':prov_fields},
       'The scaffold fills missing values but its current provenance type lacks explicit generated/estimated-field markers required by the shared adapter policy.')

telemetry=O1ObservabilityComponent()
_,response,obj=ingest(frame(),telemetry=telemetry)
data={'object':asdict(obj),'telemetry':[asdict(r) for r in telemetry.records]}
def contains_key(value,key):
    if isinstance(value,dict):return key in value or any(contains_key(v,key) for v in value.values())
    if isinstance(value,list):return any(contains_key(v,key) for v in value)
    return False
assert not contains_key(data,'run_id') and not contains_key(data,'session_id')
record('P11','Run/session identifiers absent from these emitted records',
       {'telemetry_records':len(telemetry.records),'run_id_present':False,'session_id_present':False},
       'These scaffold outputs do not demonstrate D01.04 run/session propagation. No proposed ExecutionContext has been implemented.')

_,_,l1=ingest(frame())
l2=L2NormalizationStage().process([l1]).output_objects[0]
assert l2.time_context is l1.time_context
record('P12','L2 reuses the incoming mutable TimeContext instance',
       {'time_context_is_same_instance':True,'parent_link_preserved':l1.object_id in l2.provenance.parent_object_ids},
       'Relevant to issue 23 proposed metadata-isolation policy. This is not by itself a violation of a currently agreed immutability requirement.')

_,response,obj=ingest(frame(sample_rate_hz=0,channel_count=0,frame_index=-1))
assert response.status.value=='ok'
record('P13','Numerically implausible audio dimensions accepted',
       {'stage_status':response.status.value,'sample_rate_hz':obj.payload['sample_rate_hz'],
        'channel_count':obj.payload['channel_count'],'frame_index':obj.payload['frame_index']},
       'Presence-only wording needs explicit type/range rules and implementation checks. Proposed range validation is not an already executed approved schema test.')

result={'assessment_date_local':'2026-10-28','executed_at_utc':datetime.now(timezone.utc).isoformat(),
        'baseline_commit':'8c99abecd723a39370455ba9e27adca2cea872b1','probe_count':len(results),'probes':results,
        'limits':['Synthetic sample values only. No microphone, gating signal processor, clock calibration, deletion engine, or deployed system was exercised.',
                  'StageStatus.OK describes scaffold behavior, not contract certification.',
                  'Gating/order context is explicitly a review assumption where noted.',
                  'Reference metadata remains in stored synthetic artifacts even when absent from the emitted payload.',
                  'Issue 23 diagrams and context/validator interfaces remain proposals.']}
(OUT/'probe_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'probe_count':len(results),'witness_checks':'all completed','results_file':str(OUT/'probe_results.json'),
                  'probes':[{'id':p['probe_id'],'name':p['name'],'observed':p['observed']} for p in results]},indent=2))

-- 008 — hierarchical taxonomy for the prompt corpus (A4)
-- main_cat: what the user is fundamentally doing
--   generate  = create new content from description/refs
--   edit      = transform EXISTING media in place (vfx)
--   transfer  = move identity/performance onto existing footage
--   dialogue  = spoken/sung performance clips
-- sub_cat: dominant specific type (priority pick)
-- ops[]:   ALL matched edit operations (a prompt can do several)
-- subject_type (007) kept for backward compatibility.

-- column set/order changes → recreate, not replace
drop view if exists metrics.prompt_corpus_good;
drop view if exists metrics.prompt_corpus;

create view metrics.prompt_corpus as
with base as (
  select
    r.env, r.id, r.kind, r.provider, r.provider_model, r.created_at,
    r.prompt, length(r.prompt) as prompt_len,
    case when r.prompt ~ '[ก-๙]' then
      case when r.prompt ~* '[a-z]{4,}' then 'mixed' else 'th' end
    else 'en' end as lang,
    o.outcome,
    (o.signals->>'target_runs')::int as target_runs,
    -- edit operations (independent flags)
    array_remove(array[
      case when r.prompt ~* 'background|ฉากหลัง|พื้นหลัง|\ybg\y' then 'background' end,
      case when r.prompt ~* '\y(remove|erase)\y|ลบ' then 'object-remove' end,
      case when r.prompt ~* 'anime|cel.?shad|\ystyle\y|material|texture|วัสดุ|สไตล์' then 'style-material' end,
      case when r.prompt ~* 'sky|cloud|storm|rain|fog|ท้องฟ้า|เมฆ|ฝน|หมอก' then 'sky-atmosphere' end,
      case when r.prompt ~* 'light(ing)?|relight|color (grade|match)|แสง|เงา|โทนสี|darken|brighten|contrast' then 'lighting-color' end,
      case when r.prompt ~* 'zoom (in|out)|ซูม(เข้า|ออก)|reframe|เปลี่ยนมุมกล้อง|change (the )?(camera|angle)' then 'reframe-camera' end
    ], null) as ops,
    -- class triggers
    (r.prompt ~* 'character swap|performance transfer|face swap|lip.?sync|replace (both|the) (men|man|woman|people|face)|replace acting|แทนที่?(ผู้ชาย|ผู้หญิง|คน|ตัวละคร)|แทนคน') as is_transfer,
    (r.kind='video' and r.prompt ~* 'text performance lock|dialogue|บทพูด|พูดว่า|พูดกับ|อุทาน|(^|\n)\s*(V\.O\.|VO:)|spoken|lyric|ร้องเพลง') as is_dialogue,
    (r.prompt ~* 'absolute .*lock|keep the original|replace the existing|transform this exact|preserve (the|every|its|exact)|unchanged|ลบ.*ออก|ห้ามเปลี่ยนกล้อง|เปลี่ยน(ฉาก|พื้น)หลัง|remove the (background|object)') as is_edit,
    (r.kind='image' and r.prompt ~* 'storyboard|(\y[0-9]+ panels)|panel [0-9]|2x2 grid|ช่อง(ที่)? ?[0-9]') as is_sheet,
    (r.kind='image' and r.prompt ~* 'character (sheet|design|turnaround|portrait|reference)|turnaround|char ?sheet|ตัวละครหลัก|CHAR_REF|full.?body.*(view|reference)|(หน้าตรง.*ด้านข้าง)') as is_character,
    (r.prompt ~* '\y(prop|product (photo|photography|shot)|item design)\y|อุปกรณ์ประกอบฉาก|#d3d3d3'
       or (r.kind='image' and r.prompt ~* 'jewelry|necklace|\yring\y|brooch|object (on|against)|บนพื้นหลัง(ขาว|เรียบ)')) as is_prop,
    (r.prompt ~* 'concept art|isometric|bird.?s.?eye|aerial view|architectural layout|drone shot|world.?building|แผนที่|มุมสูงเห็นทั้ง') as is_world,
    (r.prompt ~* 'establishing shot|location (reference|ref|design)|environment (design|reference)|interior of|exterior of|เป็นสถานที่|อ้างอิงสถานที่|wide (view|shot) of (a|an|the) (room|city|street|landscape|cathedral|temple)') as is_location,
    (r.prompt ~* '@\[|\(node:|(\y(image|video|output image|output video|LOH|KEYVIS)\s*=)|อ้างอิง|reference|เรฟ|\[image [0-9]\]|start frame') as has_refs
  from raw.ai_runs r
  left join tags.run_outcomes o using (env, id)
  where r.prompt is not null and length(r.prompt) > 30
    and r.kind in ('image','video')
)
select
  env, id, kind, provider, provider_model, created_at,
  prompt, prompt_len, lang, outcome, target_runs, ops,
  -- main category
  case
    when is_transfer then 'transfer'
    when is_dialogue then 'dialogue'
    when is_edit then 'edit'
    else 'generate'
  end as main_cat,
  -- sub category (priority pick within main)
  case
    when is_transfer then case
      when prompt ~* 'lip.?sync|audio driver|keep the original audio' then 'audio-driven-swap'
      when prompt ~* 'face swap|replace (both|the) (men|man|woman|people|face)|แทนที่?(ผู้ชาย|ผู้หญิง|คน)' then 'face-swap'
      else 'full-performance' end
    when is_dialogue then case
      when prompt ~* 'lyric|ร้องเพลง|sing(ing|er)?' then 'singing'
      when prompt ~* '(^|\n)\s*(V\.O\.|VO:)|narrat|บรรยาย' then 'vo-narration'
      else 'spoken-dialogue' end
    when is_edit then case
      when 'background'    = any(ops) then 'background'
      when 'object-remove' = any(ops) then 'object-remove'
      when 'style-material'= any(ops) then 'style-material'
      when 'sky-atmosphere'= any(ops) then 'sky-atmosphere'
      when 'reframe-camera'= any(ops) then 'reframe-camera'
      when 'lighting-color'= any(ops) then 'relight-only'
      else 'other-edit' end
    else case  -- generate
      when is_sheet then 'storyboard-sheet'
      when is_character then 'character'
      when is_prop then 'prop-object'
      when is_world then 'world-concept'
      when is_location then 'scene-location'
      when has_refs then 'shot-with-refs'
      else 'freeform' end
  end as sub_cat,
  -- 007-compatible flat label
  case
    when is_transfer then 'performance-swap'
    when is_dialogue then 'dialogue-performance'
    when is_edit then 'vfx-edit'
    when is_sheet then 'storyboard-sheet'
    when is_character then 'character'
    when is_prop then 'prop-object'
    when is_world then 'world-concept'
    when is_location then 'scene-location'
    when has_refs then 'shot-with-refs'
    else 'freeform'
  end as subject_type
from base;

create or replace view metrics.prompt_corpus_good as
select * from metrics.prompt_corpus
where outcome in ('kept', 'single_success', 'final');

do $$
begin
  if exists (select from pg_roles where rolname = 'analyst') then
    grant select on all tables in schema metrics to analyst;
  end if;
end $$;

-- 007 — prompt corpus classifier (A1–A3 of best-practice mining)
-- Heuristic subject-type classification of every image/video prompt, spot-checked
-- against 60+ samples (2026-08-01). Types are corpus-navigation labels (~90%),
-- not ground truth. jewelry words limited to image kind: the SIAM NARUKAL story
-- features a cursed ring, so video scenes mentioning it are NOT prop shots.

create or replace view metrics.prompt_corpus as
select
  r.env, r.id, r.kind, r.provider, r.provider_model, r.created_at,
  r.prompt, length(r.prompt) as prompt_len,
  case when r.prompt ~ '[ก-๙]' then
    case when r.prompt ~* '[a-z]{4,}' then 'mixed' else 'th' end
  else 'en' end as lang,
  o.outcome,
  (o.signals->>'target_runs')::int as target_runs,
  case
    when r.prompt ~* 'character swap|performance transfer|face swap|lip.?sync|replace (both|the) (men|man|woman|people|face)|replace acting|แทนที่?(ผู้ชาย|ผู้หญิง|คน|ตัวละคร)|แทนคน' then 'performance-swap'
    when r.kind='video' and r.prompt ~* 'text performance lock|dialogue|บทพูด|พูดว่า|พูดกับ|อุทาน|(^|\n)\s*(V\.O\.|VO:)|spoken|lyric|ร้องเพลง' then 'dialogue-performance'
    when r.prompt ~* 'absolute .*lock|keep the original|replace the existing|transform this exact|preserve (the|every|its|exact)|unchanged|ลบ.*ออก|ห้ามเปลี่ยนกล้อง|เปลี่ยน(ฉาก|พื้น)หลัง|remove the (background|object)' then 'vfx-edit'
    when r.kind='image' and r.prompt ~* 'storyboard|(\y[0-9]+ panels)|panel [0-9]|2x2 grid|ช่อง(ที่)? ?[0-9]' then 'storyboard-sheet'
    when r.kind='image' and r.prompt ~* 'character (sheet|design|turnaround|portrait|reference)|turnaround|char ?sheet|ตัวละครหลัก|CHAR_REF|full.?body.*(view|reference)|(หน้าตรง.*ด้านข้าง)' then 'character'
    when r.prompt ~* '\y(prop|product (photo|photography|shot)|item design)\y|อุปกรณ์ประกอบฉาก|#d3d3d3'
         or (r.kind='image' and r.prompt ~* 'jewelry|necklace|\yring\y|brooch|object (on|against)|บนพื้นหลัง(ขาว|เรียบ)') then 'prop-object'
    when r.prompt ~* 'concept art|isometric|bird.?s.?eye|aerial view|architectural layout|drone shot|world.?building|แผนที่|มุมสูงเห็นทั้ง' then 'world-concept'
    when r.prompt ~* 'establishing shot|location (reference|ref|design)|environment (design|reference)|interior of|exterior of|เป็นสถานที่|อ้างอิงสถานที่|wide (view|shot) of (a|an|the) (room|city|street|landscape|cathedral|temple)' then 'scene-location'
    when r.prompt ~* '@\[|\(node:|(\y(image|video|output image|output video|LOH|KEYVIS)\s*=)|อ้างอิง|reference|เรฟ|\[image [0-9]\]|start frame' then 'shot-with-refs'
    else 'freeform'
  end as subject_type
from raw.ai_runs r
left join tags.run_outcomes o using (env, id)
where r.prompt is not null and length(r.prompt) > 30
  and r.kind in ('image','video');

-- A3: quality cohorts. "good" = evidence the output was accepted:
-- explicitly kept, accepted first try, or survived iteration as the final take.
create or replace view metrics.prompt_corpus_good as
select * from metrics.prompt_corpus
where outcome in ('kept', 'single_success', 'final');

do $$
begin
  if exists (select from pg_roles where rolname = 'analyst') then
    grant select on all tables in schema metrics to analyst;
  end if;
end $$;

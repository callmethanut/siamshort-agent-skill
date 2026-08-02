---
name: siamshort-module-style-profiles
description: >-
  Named visual-style profiles (photoreal-cinematic, pixar-3d-cartoon, anime-2d-cel, neon-noir, documentary-real, thai-period-drama, product-premium — extensible). Each carries the committed style sentence, lighting grammar, camera tendencies, materials, anti-slop, model routing, and video motion feel. Load when the user names a style or the production commits to one; reuse the chosen profile's style sentence VERBATIM in every prompt of the production.
---

# Style Profiles (visual look layer — compose with any subject template and genre)

Companion to [[D-genre-profiles]] (genre = the video's PURPOSE; style = the picture's LOOK). One profile = everything a prompt needs to commit to that look: style sentence, lighting grammar, camera tendencies, materials, anti-slop, model routing, motion feel. Evidence tags: **RECIPE** = read from accepted corpus prompts · **DRAFT** = curated, pending corpus validation.

Profiles compose with any subject template (B-notes) and any genre (D): pick ONE profile per production, reuse its style sentence VERBATIM in every prompt (series-constants law).

---

## photoreal-cinematic (RECIPE)
- **Style sentence:** "Photorealistic live-action cinematic frame, natural non-plastic skin, subtle film grain, no cartoon no anime."
- **Lighting:** one named practical source per scene (window light, lamplight, neon); dramatic contrast for portraits only.
- **Camera:** shot-size + angle words; locked camera for identity shots; NO lens numbers.
- **Materials:** wear-state realism — pores, flyaway hairs, fabric creases, scuffed surfaces.
- **Anti-slop:** the anti-plastic METHOD (concrete physical evidence in description), never bolt-on "natural skin" tokens. Real faces drift across panels/shots — plan iteration.
- **Models:** gpt-image-2 (images) · seedance-2 (video). **Video motion:** true-to-physics; write reflex beats; slow-mo on hero moments.

## pixar-3d-cartoon (RECIPE)
- **Style sentence:** "3D Pixar/DreamWorks-style cartoon, soft rounded shapes, warm saturated palette, gentle subsurface glow, expressive oversized eyes."
- **Lighting:** warm golden key + soft bounce; "bright cheerful daylight" exteriors; light reads soft, never harsh.
- **Camera:** wide friendly framings, low child-height angles for wonder; gentle push-ins.
- **Materials:** stylized-but-tactile ("squishy", "glossy", "felt-like"); exaggerated proportions stated per subject.
- **Anti-slop:** ban photoreal drift ("no photorealistic skin, no live-action") when characters must stay toony; keep ONE consistent stylization level across all assets.
- **Models:** gpt-image-2 solid; character consistency easier than photoreal. **Video motion:** bouncy squash-and-stretch feel; slightly exaggerated reactions welcome.

## anime-2d-cel (RECIPE)
- **Style sentence:** "Classic 2D anime, cel-shaded, clean bold line art, flat color planes with hard shadow shapes." (Action variant: "Anime cel-shading meets hyper-realistic CGI, bold ink-line accents.")
- **Lighting:** graphic hard-edged shadow shapes; rim light as drawn line; palettes per emotional beat (warm home / cold conflict).
- **Camera:** manga grammar welcome — dramatic low/high angles, speed-line-ready compositions, held close-ups on eyes.
- **Materials:** hair/cloth as shape language, not texture; auras and energy read as drawn FX ("bright electric blue aura with white core").
- **Anti-slop:** "no 3D render, no photorealistic" when drifting; consistency clause carries harder (drawn characters survive sheets best — 4-panel anime sheets 38% vs photoreal 10%).
- **Models:** gpt-image-2 for sheets/stills. **Video motion:** stylized timing OK; montage-friendly; DBZ-style beats proven in kept sheets.

## neon-noir (RECIPE — verbatim from kept b2c series)
- **Style sentence:** "Cinematic neon-noir, teal-amber, high contrast, wet reflective asphalt, subtle film grain."
- **Lighting:** neon signage as the named source; practicals reflected in wet surfaces; pools of light in darkness.
- **Camera:** low angles, hero poses, silhouettes against glow; slow push-ins.
- **Materials:** wet/reflective everything — asphalt, jackets, chrome.
- **Anti-slop:** keep darkness via lighting design, not "dark scene" adjectives (horror lesson: darkness prompts balloon — build night in stills/edit passes).
- **Models:** gpt-image-2 + seedance-2. **Video motion:** rain/steam drift, reflections shimmer; slow-mo hero beats.

## documentary-real (RECIPE — verbatim from accepted industrial series)
- **Style sentence:** "Ultra-realistic industrial documentary, natural workshop light, honest unglamorous surfaces."
- **Lighting:** the room's own light named ("late-afternoon light through the workshop door", "fluorescent tube above the bench").
- **Camera:** "Documentary handheld. Macro <detail>. Medium <context>." — the ONE style where handheld lifts.
- **Materials:** tactile process words — freshly cut, deburred, abrasive, grit-dusted.
- **Anti-slop:** faceless framing ("only hands and forearms visible") = drift-proof; no beauty-render gloss.
- **Models:** seedance-2 / -fast. **Video motion:** real speed, no slow-mo except one payoff shot.

## thai-period-drama (DRAFT — partial corpus evidence: Suvarnabhumi/ละคร productions)
- **Style sentence:** "Thai period drama film still, warm tropical light, aged teak and gold-leaf textures, humid atmospheric depth."
- **Lighting:** candle/oil-lamp practicals indoors; hazy golden exteriors; incense-smoke volume ONLY with a named source.
- **Camera:** formal composed frames; slow reverent moves; "ตัดจบแบบละครไทย" ending grammar appears in accepted prompts.
- **Materials:** teak grain, woven textiles, tarnished gold, weathered stone.
- **Anti-slop:** period accuracy stated per item (costume era, architecture); ban modern objects explicitly when they intrude.
- **Models:** gpt-image-2 + seedance-2 21:9. **Video motion:** measured pacing; wai/gesture beats described concretely.

## product-premium (RECIPE — from accepted commercial b-roll)
- **Style sentence:** "High-end commercial photography, crisp details, clean modern surfaces, premium studio polish."
- **Lighting:** soft even studio for heroes; one accent sweep for drama; sunlit-clean for lifestyle.
- **Camera:** macro close-ups; slow-motion pours/splashes/eruptions as the signature move.
- **Materials:** finish words — brushed, matte, gloss, condensation beads, crema layer.
- **Anti-slop:** NO hands unless the beat needs them; brand text NEVER generated (post only).
- **Models:** gpt-image-2 · seedance-2/-fast for b-roll. **Video motion:** one eruption beat per clip, slow-mo macro.

---

## Adding a new profile (template)
Name (evidence tag) · Style sentence (ONE, reusable verbatim) · Lighting grammar · Camera tendencies · Materials/texture words · Anti-slop specifics · Model routing · Video motion feel. Ground in accepted prompts when possible; tag DRAFT until corpus-validated; append changelog here + mirror to `skills/siamshort-module-style-profiles`.

## Changelog
- 2026-08-02 created: 7 seed profiles (6 RECIPE, 1 DRAFT) — owner-requested style layer

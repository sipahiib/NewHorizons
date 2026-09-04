# Repository Guidelines
## Project Layout
Keep researched stories and source links in `video/SOURCES.md`. Store narration and scene manifests under `video/`, reusable channel branding under `assets/branding/`, and motion clips under `assets/motion/`. Rendering scripts belong in `video/`; the only finished delivery should be `build/video/newhorizons.mp4`.

Use `NewHorizons` as the only project and workflow-skill name. The skill must be named `newhorizons-start`; do not retain the legacy project name in code, documentation, folder names, configuration, or generated metadata.


## Rules
Sources.md altına yazılan yeni haberlerle ilgili şunları yap:

* Haber seçimini daralt: 5 haberin hepsi eşit önemde olmasın. 1 ana haber (minimum 1.5 dakika) + 4 destek haber (her bir destek haberi minimum 45 saniye) yap. Ana haber, geniş kitleyi ilgilendiren ve güçlü görseli olan bir gelişme olsun. 

İlk 20 saniyeyi güçlendir: Videoya kanal introsuyla değil, haftanın en çarpıcı gelişmesiyle başla.

* video formatı:
0:00-0:05
Şöyle bir çarpıcı cümleyle başla: "Bu hafta bilim insanları X konusunda şaşırtıcı bir sonuç açıkladı, keşfetti, vs."
0:05–0:12 — Hook
Haftanın en dikkat çekici gelişmesini profesyonel bir görselle göster.
0:12–0:20 — Çerçeve
Buna benzer cümle oluştur: “Ayrıca 4 önemli gelişme daha var. En ilginciyle başlayalım...”

* Haberlerde şu soruların cevaplarını işle:
Ne oldu?
Kim yaptı / kaynak ne?
Neden önemli?
İzleyiciyi nasıl etkileyebilir?
Özellikle son maddeyi ihmal etme. “Yeni teleskop verileri yayınlandı” yerine “Bu, Dünya benzeri gezegenleri bulma ihtimalimizi neden artırıyor?” gibi anlat.

## Approval Before Production
Before producing a new video, read `video/SOURCES.md` and show the user the proposed topics, sources, and motion-video candidates. Do not render until the user approves them. Research exactly five high-quality, current, relevant, and engaging animated clips or short videos per topic. Prefer footage from cited source pages and authoritative publishers; do not use the legacy `png/` folder.

Before starting each new production cycle, remove every `.mp3` and `.mp4` left from the previous cycle so old narration, source footage, main renders, or Reels cannot be mixed into the new work. Resolve the exact previous-cycle paths first and preserve non-media project files, scripts, manifests, branding, and the newly approved inputs.

## Video Format & Visual Direction
Render at 1920×1080, 60 fps, H.264/AAC; never render in 4K. Target five minutes. Give the main first story minimum 1.5 minutes and each of the four supporting stories about 45 seconds. Do not use still images in news content. Every topic must use exactly five animated clips or short videos. For the 1.5-2 minute main story, keep each clip on screen for 20–24 seconds. For each supporting story, keep each clip on screen for 8–9 seconds. Never place the channel cover at the beginning; open immediately with a motion-footage hook. The static channel cover may appear only behind the closing CTA. Avoid a slide-deck appearance. Show only headings and exceptional one-sentence takeaways; animate those phrases in and out with restrained professional effects.

## Instagram Reels
For each new main-video cycle, research exactly three independent Reels topics, one from each recurring category:

1. Sports Biomechanics and Physics
2. Hands-on Science at Home for Young Explorers
3. Advances in AI for Archaeology

En önemli gelişmelere, yeni bir şey öğreten haberlere ve pratik/teknik açıdan işe yarayan gelişmelere öncelik ver. Bilgileri güncel ve güvenilir kaynaklardan doğrula; mümkün olduğunda aynı konuyu tekrarlama. Benim onayıma sun haberleri ve hangi haberleri seçeceğimi sor. 

Append these three candidates below the main-video stories in `video/SOURCES.md`; never delete or replace the main-video topics. For each candidate, record the angle, why it is engaging, factual sources, and high-quality motion-video candidates. Present all three to the user and wait for explicit approval before downloading media, writing final narration, or rendering. After approval, produce exactly one English Reels video for each approved topic, for three Reels in total.

Each Reels video must be 30–35 seconds. Show YouTube (`@newhorizons_21`) and Instagram like/follow calls during the closing.

Instagram Reels videolarını daima 1080×1920 piksel, 9:16 dikey ve 60 fps olarak üret. Yatay kaynak görüntüleri kırpma; görüntünün tamamını ortada göster ve kalan dikey alanı aynı görüntüden oluşturulan, koyulaştırılmış bulanık arka planla doldur.

Seslendirmeyi gerçek süresi ölçülmüş olarak 30 saniyelik pencereye yerleştir ve konuşmanın video bitmeden tamamlanmasını sağla. Kapanıştan sonra kısa bir görsel nefes payı bırak.

Reels kapanış payı, konuşmanın gerçek bitişinden video sonuna kadar en fazla 4 saniye olmalıdır. Daha uzun sessiz kapanış bırakma; toplam süreyi 30–35 saniye içinde sesin ölçülen bitişine göre ayarla.

Instagram Reels seslendirmelerinde ücretsiz Microsoft Edge TTS `en-GB-RyanNeural` sesini `-2%` sabit hızla kullan. vidIQ veya yerel macOS Daniel sesini kullanma. Kullanıcıdan yeni bir ses onayı alınmadıkça başka bir sese geçme.


## Narration & Closing
Produce all future videos exclusively in English. This English-only rule also applies to Instagram Reels.

Do not begin with the fixed phrase “First of our news is.” Before every new video, present several concise, audience-grabbing English hook options tailored to the main story and wait for the user's choice. Do not lock or render the narration before that approval. The selected first sentence should create curiosity and pair naturally with the opening motion footage.

Use the approved British male narrator `en-GB-RyanNeural` without clipped words or unexplained silence. The hook, narration, headings, exceptional one-sentence takeaways, thumbnail copy, and CTA labels must use natural English. Do not use the previous Turkish introduction or closing. End exactly: “That was our latest news. Stay with science, and stay tuned.” During the final 10 seconds, use the approved cinematic-glass CTA with English labels: a softly entering glass panel, a brief Like-icon response, a light accent on the Subscribe button, and a restrained animated notification bell. Do not display the channel name or `@newhorizons_21` on the main video’s closing screen.

Mention at most one important financial figure or financial point per topic. Do not dwell on prices, fees, valuations, revenue, or profit.

## Verification, Cleanup & Delivery
Verify resolution, frame rate, target duration, continuous audio, scene timing, overlays, the motion-footage opening, and final CTA. After every successful render, delete obsolete outputs, temporary audio, extracted frames, contact sheets, caches, and disposable render intermediates. Preserve approved source assets, scripts, manifests, branding, and the verified `newhorizons.mp4`.

After verification and cleanup, ask whether the user wants the result pushed to GitHub. Never push without explicit approval; confirm the remote or branch if unclear.

When committing or pushing to GitHub, exclude the entire `build/video/editorial-en/` directory and all files beneath it.

Never add, commit, or push `.mp3` or `.mp4` files. Keep all generated audio, source footage, Reels, and finished video binaries local; GitHub should contain only the scripts, manifests, text, metadata, and other non-audio/non-video project files needed to reproduce them.

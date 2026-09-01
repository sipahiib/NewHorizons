# Repository Guidelines


## Project Layout

Keep researched stories and source links in `video/SOURCES.md`. Store narration and scene manifests under `video/`, reusable channel branding under `assets/branding/`, and motion clips under `assets/motion/`. Rendering scripts belong in `video/`; the only finished delivery should be `build/video/newhorizons.mp4`.


## Rules
Sources.md altına yazılan yeni haberlerle ilgili şunları yap:

* Haber seçimini daralt: 5 haberin hepsi eşit önemde olmasın. 1 ana haber + 4 destek haber yap. Ana haber, geniş kitleyi ilgilendiren ve güçlü görseli olan bir gelişme olsun. 

İlk 15 saniyeyi güçlendir: Videoya kanal introsuyla değil, haftanın en çarpıcı gelişmesiyle başla. Örneğin: “Bu hafta bilim dünyasında yapay zekâdan Mars’a kadar üç gelişme öne çıktı. Ama bir tanesi günlük hayatımızı beklenenden çok daha erken değiştirebilir.”

* video formatı:
0:00–0:15 — Hook
Haftanın en dikkat çekici 2–3 gelişmesini çok kısa göster.
0:15–0:30 — Çerçeve
“Bu hafta seçtiğim 5 bilimsel gelişme ve neden önemli oldukları…”

* Haberlerde şu soruların cevaplarını işle:
Ne oldu?
Kim yaptı / kaynak ne?
Neden önemli?
İzleyiciyi nasıl etkileyebilir?
Özellikle son maddeyi ihmal etme. “Yeni teleskop verileri yayınlandı” yerine “Bu, Dünya benzeri gezegenleri bulma ihtimalimizi neden artırıyor?” gibi anlat.

* Thumbnail
1 ana görsel + 2–4 kelime olsun.
Örnek: AI BREAKTHROUGH? veya SPACE JUST CHANGED.
Köşeye küçük şekilde “This Week” eklenebilir.

## Approval Before Production

Before producing a new video, read `video/SOURCES.md` and show the user the proposed topics, sources, and motion-video candidates. Do not render until the user approves them. Research exactly five high-quality, current, relevant, and engaging animated clips or short videos per topic. Prefer footage from cited source pages and authoritative publishers; do not use the legacy `png/` folder.

## Video Format & Visual Direction

Render at 1920×1080, 60 fps, H.264/AAC; never render in 4K. Target three minutes, with roughly one minute per topic. Do not use still images in news content. Every topic must use exactly five animated clips or short videos, each lasting 10–12 seconds. Never place the channel cover at the beginning; open immediately with a motion-footage hook. The static channel cover may appear only behind the closing CTA. Avoid a slide-deck appearance. Show only headings and exceptional one-sentence takeaways; animate those phrases in and out with restrained professional effects.

## Instagram Reels
Her ana video sonrasında, ek olarak her konu için 1 Instagram reels videosu oluştur; her Reels 30–35 saniye aralığında ve İngilizce olsun. Kapanışta YouTube (`@newhorizons_21`) ve Instagram hesaplarını beğenme ve takip etme butonları göster.

Instagram Reels videolarını daima 1080×1920 piksel, 9:16 dikey ve 60 fps olarak üret. Yatay kaynak görüntüleri kırpma; görüntünün tamamını ortada göster ve kalan dikey alanı aynı görüntüden oluşturulan, koyulaştırılmış bulanık arka planla doldur.

Her Reels için ana videodan bağımsız, kısa ve konuya özel yeni bir İngilizce tanıtım metni yaz; ana videodaki konuşmayı birebir kullanma. Seslendirmeyi gerçek süresi ölçülmüş olarak 30 saniyelik pencereye yerleştir ve konuşmanın video bitmeden tamamlanmasını sağla. Kapanıştan sonra kısa bir görsel nefes payı bırak.

Reels kapanış payı, konuşmanın gerçek bitişinden video sonuna kadar en fazla 4 saniye olmalıdır. Daha uzun sessiz kapanış bırakma; toplam süreyi 30–35 saniye içinde sesin ölçülen bitişine göre ayarla.

Instagram Reels seslendirmelerinde ücretsiz Microsoft Edge TTS `en-GB-RyanNeural` sesini `-2%` sabit hızla kullan. vidIQ veya yerel macOS Daniel sesini kullanma. Kullanıcıdan yeni bir ses onayı alınmadıkça başka bir sese geçme.


## Narration & Closing

Produce all future videos exclusively in English. Do not generate Turkish narration, Turkish on-screen text, Turkish thumbnails, Turkish CTA labels, or a separate Turkish video. This English-only rule also applies to Instagram Reels.

Use the approved British male narrator `en-GB-RyanNeural` without clipped words or unexplained silence. The hook, narration, headings, exceptional one-sentence takeaways, thumbnail copy, and CTA labels must use natural English. Do not use the previous Turkish introduction or closing. End exactly: “That was our latest news. Stay with science, and stay tuned.” During the final 10 seconds, use the approved cinematic-glass CTA with English labels: a softly entering glass panel, a brief Like-icon response, a light accent on the Subscribe button, and a restrained animated notification bell. Do not display the channel name or `@newhorizons_21` on the main video’s closing screen.

Mention at most one important financial figure or financial point per topic. Do not dwell on prices, fees, valuations, revenue, or profit.

## Verification, Cleanup & Delivery

Verify resolution, frame rate, target duration, continuous audio, scene timing, overlays, the motion-footage opening, and final CTA. After every successful render, delete obsolete outputs, temporary audio, extracted frames, contact sheets, caches, and disposable render intermediates. Preserve approved source assets, scripts, manifests, branding, and the verified `newhorizons.mp4`.

After verification and cleanup, ask whether the user wants the result pushed to GitHub. Never push without explicit approval; confirm the remote or branch if unclear.

When committing or pushing to GitHub, exclude the entire `build/video/editorial-en/` directory and all files beneath it.

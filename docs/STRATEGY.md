# Group II Trading Strategy — استراتژی معاملاتی گروه دوم
Source: transcripts of 4 videos (II.1–II.4), Persian. Timestamps refer to `[HH:MM:SS]` inside each `work\transcript_iiN.txt`.
منبع: متن هر ۴ ویدیو. تایم‌استمپ‌ها به داخل فایل متن همان ویدیو ارجاع می‌دهند.

> ⚠️ This is a reconstruction from speech-to-text transcripts WITHOUT the chart video.
> Many rules are chart-dependent ("this ceiling / this floor"). Items marked ❓ need your confirmation.
> این بازسازی از روی متنِ گفتار است بدون تصویر چارت؛ موارد ❓ نیاز به تأیید شما دارد.

---

## 1. Methodology Overview — نمای کلی سبک

**EN:** A proprietary method rooted in RTM / Supply-Demand / QM vocabulary (QM, FTC, RTP, RTO, stop-hunts),
but the instructor explicitly says he often teaches the OPPOSITE of ICT/RTM. No sessions, killzones, or liquidity-pool
model were mentioned. The core thesis:

> **Price moves from a balanced place to an unbalanced place — balanced in TIME, unbalanced in PRICE.**
> Valuable trade locations = zones that are time-balanced but price-unbalanced.

**فا:** سبک اختصاصی مدرس بر پایه‌ی ادبیات RTM و عرضه/تقاضا (QM، شکار استاپ و...) است، ولی مدرس صریحاً می‌گوید
جاهای زیادی خلاف ICT/RTM حرف می‌زند. خبری از سشن، کیل‌زون و مدل نقدینگی نیست. تز اصلی:
**قیمت از جای متعادل به جای نامتعادل می‌رود — از نظر زمانی متعادل، از نظر قیمتی نامتعادل.**
جاهای ارزشمند برای ترید، همان ناحیه‌هایی هستند که از لحاظ زمانی متعادل و از لحاظ قیمتی نامتعادل‌اند.
(II.1 [00:00:00], [03:20:00] — «درک با ترید متفاوته»: همه‌جای مارکت قابل فهم است ولی همه‌جا قابل ترید نیست.)

- Primary timeframe: **1-minute** (single-TF trading; do not mix TF confirmations). — تایم‌فریم اصلی: **۱ دقیقه**.
- **Your markets (confirmed): US30, NAS100, US500, XAUUSD, BTC, EURUSD — Timeframes M1 + M5.**
  Rules were demoed on tiny-range crypto scalps; on M5/indices the same structures apply but range height and
  buffer must be re-scaled (see §2.6). — **نمادهای تو (تأیید شد): US30، NAS100، US500، XAUUSD، BTC، EURUSD — تایم‌فریم M1 و M5.**
- **Your risk (confirmed): 0.5% per trade.** No daily-stop/session/news rule was found in transcripts — set your own
  (suggestion: max 2 losses or −1% per day, no trading into high-impact news). — **ریسک تو (تأیید شد): ۰٫۵٪ هر ترید.**

---

## 2. Building Blocks — اجزای استراتژی

### 2.1 Range: Internal vs External — رنج داخلی و خارجی (II.2)

**EN:**
- Price is ALWAYS inside two ranges at once: an **internal** and an **external** range → 4 lines:
  internal ceiling, external ceiling, internal floor, external floor.
- How to draw: find 2 opposite **Majors** (a valid bullish Major, then a valid bearish Major before it).
  If you can't find the opposite Major inside the current leg, step one high back — the hidden opposite Major appears.
- Special case — **merged lines (یکی شدن)**: when internal ceiling = external ceiling (or floors), that side
  **WILL be swept/touched** — price has no other way. (II.2 [00:10:00], [00:40:00])
- Ranges are fractal/nested: after a ceiling is taken, redraw. One candle normally CANNOT break the internal
  floor and the external floor at the same time and still target the far side.

**فا:**
- قیمت همیشه هم‌زمان داخل دو رنج است: داخلی و خارجی → ۴ خط: سقف/کف داخلی و سقف/کف خارجی.
- رسم: ۲ ماجور مخالف پیدا کن (یک ماجور صعودی معتبر، بعد یک ماجور نزولی قبل از آن).
  اگر ماجور مخالف داخل لگ فعلی دیده نشد، یک سقف به عقب برگرد تا ماجور پنهان دیده شود.
- حالت خاص «یکی شدن»: وقتی سقف داخلی = سقف خارجی شود (یا کف‌ها)، آن سمت **حتماً دیده/سوئیپ می‌شود**.
- رنج‌ها فرکتالی و تودرتو هستند؛ بعد از زده شدن سقف، از نو رسم کن.

### 2.2 Equilibrium (تعادل) — 4 kinds (II.2) — ✅ VERIFIED WITH SCREENSHOTS

**EN (verified 2026-10-08 from user screenshots, BTC 1m Bybit Jan 2023):**
- The 4 lines exist exactly as taught and are labeled on chart (screenshot 3): فرکتال خارجی / فرکتال داخلی /
  لگ خارجی / لگ داخلی (fractal ext/int, leg ext/int).
- **How to draw (confirmed):** TradingView Fib tool anchored at **leg start (0) → consumption extreme (1)**;
  the **0.5 line extended** = equilibrium (screenshots 1–2: fib 18787.0 → 19036.2, 0.5 = 18911.5;
  fib 18787.5 → top, 0.5 = 18804.0). Retracement-style fibs (0.5 at 21055 in screenshot 6) mark the same 50% logic
  on smaller legs.
- **Overlap rule (confirmed):** shaded box-zones are drawn where internal + external 50% lines coincide
  (screenshot 1: boxes ~18900–18920 sitting on the 18911.5 fib line). Overlap = keep the zone, drop the rest.
- **Price behavior (confirmed):** screenshot 6 shows price returning to the 0.5 line (~21055) then continuing up to
  21139 — «return to equilibrium, then go». Screenshot 4 shows a range high/low pair swept and then price running
  to the external target (~20862.5).
- **External equilibrium = horizontal ray (✅ CONFIRMED by user, red-circled line):** Fib from leg start → consumption
  point, take the **50%**, draw it as a **horizontal ray extended to the right** (screenshot: fib high 19036.2 →
  18895.0, 0.5 = 18965.5, ray drawn at ~18964.5 across the whole chart). Untouched ray = must-see magnet / «خط قطعی».
  (Screenshot 1-red-circle, II.1 [00:50:00].)
- Untouched = magnet (must-see); touched = balanced. Premium/Discount = this 50%.

**EN:**
- **Fractal equilibrium internal/external**: Fib 50% from leg start to consumption point. Untouched = magnet (must-see);
  touched = balanced. The instructor equates Premium/Discount to this 50%.
- **Leg (time) equilibrium internal/external**: a leg is "balanced" when time-balanced (mouse/ruler test from
  decision point to extreme — ❓ exact procedure unclear). "Power 1" = unbalanced one side, "Power 2" = both sides.
- Trading use: price should come **balanced → sit on balanced → go to unbalanced target**.
  If price takes an unbalanced ceiling WITHOUT equilibrating first, it must come back to the leftover equilibrium.
- Where internal + external equilibrium overlap = highest-value filter zone.

**فا:**
- **تعادل فرکتالی داخلی/خارجی**: فیبوی ۵۰٪ از شروع لگ تا نقطه‌ی مصرف. دست‌نخورده = آهن‌ربا (باید دیده شود)؛ لمس‌شده = متعادل.
- **تعادل لگی/زمانی داخلی/خارجی**: لگ وقتی متعادل است که از نظر زمانی متعادل باشد (❓ روش دقیق خط‌کشی نامشخص).
- کاربرد: قیمت باید **متعادل بیاید، روی متعادل بنشیند، بعد به هدف نامتعادل برود**.
  اگر سقف نامتعادل را بدون تعادل دیدن بزند، باید به تعادلِ باقی‌مانده برگردد.
- جایی که تعادل داخلی و خارجی هم‌پوشانی دارند = بهترین ناحیه‌ی فیلتر.

### 2.3 Minor-Major (مینور-ماجور شدن) — the permission (II.1–II.4)

**EN:** A minor swing becomes a major when its extreme is broken + opposite close. **No analysis before a
minor is majored** — the break is your "permission" to analyze and trade. Inside bars = reversal sign.
❓ Exact candle-count/close rules need the chart videos.

**فا:** وقتی اکستریم یک سوینگ مینور شکسته شود + کلوز مخالف بدهد، مینور به ماجور تبدیل می‌شود.
**قبل از ماجور شدن، هیچ تحلیلی نکن** — شکست همان «اجازه»‌ی تحلیل و ترید است. اینسایدبار = نشانه‌ی برگشت.

### 2.4 Corresponding High & Low — سقف و کف متناظر (II.3, core entry model)

**EN:**
1. Start from a **Fractal 0**. Price leaves it and dumps → a **Low** forms on a Minor-Major candle
   (≈ two same-color candles closing into/above each other).
2. Price rises **without touching Fractal 0 again** → 1–2 candles close under each other → a **High** forms.
3. That High **corresponds** to that Low → you now have a "view" on both.
- **Invalidation:** (a) price revisits the level AS Fractal 0 → dead (other side stays valid);
  (b) more than **2 closes** beyond the level → dead (dojis/inside bars not counted); (c) a wick counts as a close
  (shadow in current TF = close in lower TF).
- **Trigger:** price returns to the level (NOT as Fractal 0) + Minor-Major confirmation candle → enter at its close:
  Buy at Corresponding Low, Sell at Corresponding High.
- **Skip filter:** if the entry candle itself already took the opposite side's TP1, skip the trade.
- **Escalation pattern:** a Sell that fails TP1 → the Buy after it is BETTER; if that Buy passes TP1 then gives a Sell →
  that Sell is even better (each next signal in sequence outranks the previous).

**فا:**
1. از یک **فرکتال صفر** شروع کن. قیمت از آن خارج و ریزش می‌کند → با کندل مینور-ماجور یک **کف** ساخته می‌شود.
2. قیمت **بدون برگشت به فرکتال صفر** بالا می‌رود → با ۱–۲ کلوز زیر هم یک **سقف** ساخته می‌شود.
3. آن سقف، **متناظر** آن کف است → حالا روی هر دو «دید» داری.
- **ابطال:** (الف) برگشت قیمت به سطح در قالب فرکتال صفر؛ (ب) بیش از **۲ کلوز** پشت سطح (دوجی/اینسایدبار حساب نیست)؛ (ج) شدو = کلوز.
- **تریگر:** برگشت قیمت به سطح (نه در قالب فرکتال صفر) + کندل تأیید مینور-ماجور → ورود در کلوز آن کندل:
  در کف متناظر **بای**، در سقف متناظر **سل**.
- **فیلتر رد:** اگر خود کندل ورود، TP1 سمت مخالف را دیده باشد، ترید را رد کن.
- **الگوی تشدید:** سلی که به TP1 نرسد → بایِ بعد از آن **بهتر** است؛ و سلِ بعد از آن باز هم بهتر (هر سیگنال بعدی در زنجیره، از قبلی بهتر است).

### 2.5 Targets ladder — نردبان تارگت (II.1, II.3)

**EN:** Targets are **multiples of risk, where 1x = the SL distance ≈ range height (confirmed by you)**:
1 – 3 – 6 – 9 – 10 – 12 – 18 – 20 – 24 – 40 – 48 – 50 – 66 – 80 – 90…
(II.3 [00:10:00]: «به اندازه همون رنج باید استاپ بذارم… تارگت یک بر اساس این استاپه» — SL equals the range,
TP1 = 1× that distance.)
- **TP1** = decision zone → move stop to **breakeven (risk-free)**.
- **TP3** = important → exit **30%**, stop to entry (fully risk-free).
- Hold the rest for TP6 / TP9 / TP10+. Strong momentum through TP1 implies TP3; through TP3 implies TP6.
- ❓ Base unit never formally defined (entry→SL distance? range height?). Needs a worked example.

**فا:** تارگت‌ها **مضربی از ریسک** هستند: ۱ – ۳ – ۶ – ۹ – ۱۰ – ۱۲ – ۱۸ – ...
- **TP1** = ناحیه‌ی تصمیم → استاپ به **سر‌به‌سر**.
- **TP3** = مهم → خروج **۳۰٪**، استاپ به نقطه‌ی ورود (کاملاً ریسک‌فری).
- بقیه برای TP6 به بعد نگه داشته شود. عبور قدرتمند از TP1 یعنی TP3؛ از TP3 یعنی TP6.
- ❓ واحد مبنا (فاصله‌ی ورود تا استاپ؟ ارتفاع رنج؟) رسماً تعریف نشده — یک مثال عددی لازم است.

### 2.6 Stop loss & buffer — استاپ و بافر (II.3)

**EN:** Theory = SL exactly at the level. Real trading in tiny ranges (spread 0.5 e.g. Bybit BTC): add **1 point
buffer** above the High (sell) / below the Low (buy). With buffer, theoretical targets shrink
(e.g. theoretical TP18 → real TP9). Tight obvious stops get hunted — place beyond the sweep projection.
- **Screenshot evidence (screenshot 5, BTC 16522 barcode chop):** the position tool sits exactly on this kind of
  micro-range — entry dotted line ~16522, stop zone below, TP box above. Confirms entries happen INSIDE chop with
  buffer, not on clean swings. Screenshot 2 shows the same long-position tool (green box) with projected zigzag path.
- ⚠️ YOUR MARKETS: on US30/NAS100/XAUUSD the "1 point" of BTC-perp is meaningless — scale buffer as
  **max(spread × 2, 0.1 × range height)** until the instructor's rule is clarified. — روی نمادهای تو «۱ پوینت»
  معنایی ندارد؛ تا روشن شدن قانون، بافر = بیشترِ (۲× اسپرد، ۰٫۱× ارتفاع رنج).

**فا:** در تئوری استاپ دقیقاً روی سطح؛ در عمل (رنج‌های ریز با اسپرد) **۱ پوینت بافر** بالای سقف (سل) / زیر کف (بای).
با بافر، تارگت‌ها کوچک می‌شوند (مثلاً TP18 تئوریک → TP9 واقعی). استاپ‌های تنگ و واضح هانت می‌شوند — پشت پرتابه‌ی سوئیپ بگذار.

### 2.7 Filters & counting — فیلترها (II.2, II.4)

**EN:**
- **Divergence (RSI)** = only a "cheat for the eye" to spot where a good minor-major is likely — NEVER an entry alone.
  Best: external divergence + internal/external equilibrium overlap ("super setup").
- **Leg counting rule (✅ CONFIRMED by counting screenshot, BTC 1m):**
  1. Count the candles of a leg with the ruler (use ONE consistent method for all legs — tool reading).
  2. Reduce to a single digit by summing digits (digital root): 18 → 1+8 = **9**, 25 → 2+5 = **7**.
  3. **Even (2,4,6,8) = balanced leg (متعادل) / Odd (1,3,5,7,9) = imbalanced leg (نامتعادل).**
  Chart labels confirm: «2 = even», «18 = 9 = odd», «25 = 7 = odd», «7 = odd imb.», «5 = odd imb.».
  Small-leg 0.5 fibs (21120 / 21112 / 21055 / 21049.5) mark each leg's equilibrium in the same screenshot.
  ❓ STILL OPEN: the «coefficient» (ضریب) comparison BETWEEN two legs — hinted in II.4, formula not shown.
- **Max 2 steps:** a move of 1–2 steps then continuation is fine; **3+ steps one side = story changes completely**, reset counts.
- **Preferred trade:** don't take every signal — there is one best ("preferred") trade per chart/day; let the first
  bad sell happen, take the return to the internal floor instead.

**فا:**
- **واگرایی (RSI)** فقط «چشم‌یار» برای حدس جای مینور-ماجور خوب است — **هرگز به‌تنهایی ورود نیست**.
  بهترین حالت: واگرایی خارجی + هم‌پوشانی تعادل داخلی/خارجی («سوپر ستاپ»).
- **زوج/فرد بودن تعداد کندل + ریشه‌ی ۳-۶-۹** به‌عنوان پروکسی تعادل (زوج = متعادل‌تر). ❓ فرمول دقیق ضریب بین لگ‌ها گفته نشد.
- **حداکثر ۲ گام:** حرکت ۱–۲ گامی و ادامه طبیعی است؛ **۳ گام و بیشتر به یک سمت = داستان عوض می‌شود**، شمارش ریست.
- **ترید ارجح:** هر سیگنالی را نگیر — هر روز/چارت یک بهترین ترید دارد؛ بگذار سلِ بد اول اتفاق بیفتد، برگشت به کف داخلی را بگیر.

---

## 3. Unified Trade Plan — پلن یکپارچه‌ی معامله

### Step 1 — Map the structure (نقشه‌ی ساختار)
1. Draw internal/external range (4 lines) from 2 opposite Majors. — رنج داخلی/خارجی را با ۲ ماجور مخالف رسم کن.
2. Draw the 4 equilibriums (fractal + leg, internal + external). Mark untouched (must-see) vs touched. — ۴ تعادل را رسم و دست‌نخورده/لمس‌شده را مشخص کن.
3. Note merged lines (internal = external) → that side WILL sweep. — خطوط یکی‌شده = آن سمت حتماً سوئیپ می‌شود.

### Step 2 — Wait for permission (انتظار اجازه)
4. Do NOTHING until a minor majors (extreme broken + opposite close). — تا مینور ماجور نشده، هیچ کاری نکن.
5. Build/confirm the Corresponding High/Low pair from Fractal 0. — جفت سقف/کف متناظر را از فرکتال صفر بساز.

### Step 3 — Entry (ورود)
6. Price returns to the Corresponding level (not as Fractal 0, ≤2 closes). — برگشت قیمت به سطح متناظر.
7. Minor-Major confirmation candle → enter at close (Buy at Low / Sell at High). — کندل تأیید → ورود در کلوز.
8. Skip if entry candle already took opposite TP1; skip if 3+ one-sided steps. — فیلترهای رد.

### Step 4 — Manage (مدیریت)
9. SL = level ± 1-point buffer (beyond sweep, never at the obvious extreme). — استاپ = سطح ± ۱ پوینت بافر.
10. TP1 → breakeven. TP3 → close 30%, stop to entry. Hold rest for 6/9/10+. — مدیریت نردبانی.
11. If a signal fails TP1, the NEXT opposite signal is higher quality — take it. — سیگنال بعدی در زنجیره بهتر است.

### Step 5 — Invalidation (ابطال)
- Level revisited as Fractal 0 → pair dead. — سطح در قالب فرکتال صفر دیده شود.
- 3rd close beyond level → dead. — کلوز سوم پشت سطح.
- Both sides time-balanced + only fractal magnets left ("power-2 close") → flat, wait for new pivot. — هر دو سمت متعادل شوند → فلت و انتظار پیوت جدید.

---

## 4. Pre-trade Checklist — چک‌لیست قبل از ورود

- [ ] 4 range lines drawn? (internal/external ceiling + floor) — ۴ خط رنج رسم شده؟
- [ ] Untouched vs touched equilibriums marked? — تعادل‌های دست‌نخورده مشخص شده؟
- [ ] Any merged line? (expect sweep there, not a reversal entry) — خط یکی‌شده هست؟ (انتظار سوئیپ، نه ورود برگشتی)
- [ ] Minor majored = permission granted? — مینور ماجور شد (اجازه صادر شد)؟
- [ ] Valid Corresponding pair (from Fractal 0, ≤2 closes, not killed)? — جفت متناظر معتبر است؟
- [ ] Confirmation candle closed (Buy at Low / Sell at High)? — کندل تأیید کلوز داد؟
- [ ] Entry candle didn't already take opposite TP1? — کندل ورود TP1 مخالف را ندیده؟
- [ ] Steps ≤ 2 to this side? — گام‌ها حداکثر ۲ است؟
- [ ] SL placed beyond sweep + buffer? — استاپ پشت سوئیپ + بافر است؟
- [ ] TP ladder + TP1→BE / TP3→30% plan set? — نردبان TP و برنامه‌ی مدیریت مشخص است؟

---

## 5. Open Questions for You — سؤالات باز (❓)

1. **Symbol & broker:** ✅ answered — US30, NAS100, US500, XAUUSD, BTC, EURUSD on M1/M5.
   ⚠️ Open: how to scale the 1-point buffer per symbol (points vs ATR)? — بافر هر نماد چطور مقیاس شود؟
2. **Fractal-0 (best-effort from text, needs chart check):** F0 = one leg from its origin; it is "consumed" (مصرف شده)
   when price returns with a reversal reaction + upward confirmation (II.1 [00:30:00]).
   Internal equilibrium = Fib 50% of F0's internal space; external = from start of the F0 leg to the consumption
   point, 50% extended (II.1 [00:40:00]). A SECOND external-drawing model exists but was truncated in transcript
   (II.1 [00:50:00]) → screenshot requested below.
3. **Target base unit:** ✅ answered — 1x = range height (≈ entry→SL distance).
4. **Buffer rule** — 0.5 vs 1 point, when which; fixed ticks or ATR/spread multiple? — قانون بافر؟
5. **Major/Minor (best-effort from text):** Minor-Major ≈ two same-color candles closing into/above each other
   (e.g. green + green closing above the prior high validates a floor — II.3 [00:00:00]); entries use «دو کندل ورود» —
   if the level breaks with THREE candles, no entry (II.1 [01:10:00]). Wick-vs-close edge cases → screenshot below.
6. **Leg-equilibrium drawing procedure + even/odd + 3-6-9 coefficient formula** (II.4 hints, never revealed). — فرمول ضریب لگ‌ها؟
7. **Risk per trade** ✅ answered — 0.5%. **Still open: daily stop, session, news filter** (none in transcripts).
8. ~~Chart screenshots~~ → see screenshot list at the end of §5 (requested below).

---

## 6. Suggested Next Steps — گام‌های بعدی پیشنهادی

1. You answer §5 (at least #1 and #7) — تو به بخش ۵ جواب بده (حداقل ۱ و ۷).
2. Forward-test the checklist on 10–20 live/demo setups in a journal (setup screenshot + which checklist boxes
   passed + outcome). — فورواردتست چک‌لیست روی ۱۰–۲۰ ستاپ دمو/لایو با ژورنال.
3. Then we can encode the mechanical parts (range lines, equilibrium 50%, close-counting, TP ladder) into an
   indicator/EA or a backtest script. — بعد بخش‌های مکانیکی را به اندیکاتور/اکسپرت یا اسکریپت بک‌تست تبدیل می‌کنیم.

# Internship pages

The layout and rules for every internship page on the site. RoBIM and Toyota are built this way; copy their markup in `index.html` rather than writing a new page from scratch. For where those two pages stand right now, read `_docs/handoff-robim-toyota.md`.

This repo is public and GitHub Pages serves it as johnsonyep.com, so nothing confidential goes in these docs or the page. Any company-specific confidentiality rules live in the session's private memory, not here.

## Steps for a new page or a big change

1. Sync with GitHub as `CLAUDE.md` says.
2. Interview the user (the grilling skill) until every fact on the page is confirmed: what they built themselves and what others did, numbers, which names they allow (a plant's city, for example), the video links and the images. Read their code if they share it; it can catch a wrong claim on the page. Write only what they confirmed, and ask rather than infer.
3. Build the page in the order under **Page structure**, and register it (**Registering a new page**).
4. Write the text with the humanizer skill (**Writing**), and draw a diagram for every step (**Diagrams**).
5. Run every check under **Checks**, then commit locally. Push only when the user asks: a push deploys the live site.

## Page structure

Inside `<div id="cat-<id>" class="cat-detail" style="display:none">`, in this order:

1. **Heading.** `.panel-heading` with the full company name (RoBIM Technologies, Toyota Boshoku), and `.panel-sub` with the role exactly as the resume words it and the dates.
2. **Overview** (`.overview`):
   - `.overview-lead`: a pitch of one to three sentences saying what the user built, readable by someone with no technical background.
   - `.demo`: the video player, when there are demo videos. One tab per video, the most impressive first, labelled like the project or the video's YouTube title. No caption under the player.
   - Background: one `.context-part` (label plus paragraph) about the company or site. Use a `.context-grid` around two of them.
   - `dl.overview-facts`: the setup (robots, camera, controllers and so on), a "Built with" row of tags, and a "Projects" row of jump links to each project.
   - No result tiles or stat cards. The user removed them from RoBIM.
3. **Projects** (`.group` of `.project`), most important first. Each one has:
   - `h2.project-title`, a `.stack` of tags, and a `.btn-row` (Watch Demo, View Code). Keep each project's own Watch Demo button even when its video is in the player, because the printable summary takes its links from those buttons.
   - Images in an `.img-grid`, when there are any.
   - `.whi` with three blocks:
     - **What:** a paragraph.
     - **How:** a stepper when the work is a real process of four or more steps (Survey Scan, AMR Rack Delivery). Otherwise a paragraph (HMI Development).
     - **Impact:** outcomes and numbers, when the user has some. Leave the block out when there are none, as on RoBIM.
   - When one piece of work mixes two stories (the AMR robot system and its camera pipeline), split it into two projects, each with its own stepper.

## Registering a new page

- **Homepage card:** a `.cat-btn` in the Internships group of `#cat-hub`, newest first. It needs:
  - the logo, the full company name, the role, and exactly three skill tags
  - a `.cat-btn-date` with `.date-start` ("Sep 2026") and `.date-end` ("to now", or "to May 2026") spans
  - for a current role, the `is-now` class on the button and a `.now-chip` after the title

  The Internships and Design Teams groups are `.cat-section-timeline`, which gives each group its own line, running from its first card's dot to its last. Personal Projects stays off the line. The homepage has no page heading and no pictures on the cards, by the user's choice.
- **Router:** add the id to `validCats`.
- **Print summary:** add `cat-<id>` to `PRINT_CATEGORIES`.
- The resume links to `johnsonyep.com/#<id>`, so a page's id never changes once published.

## Steppers

Copy an existing `.stepper` and keep its structure:
- a tablist of `.stepper-tab` buttons, each with a 24×24 line icon, the step number, and the step title as `title`
- one `.stepper-panel` per step, holding the diagram, a "Step N of M" eyebrow, `h3.step-title`, `p.step-lead` (the step in one sentence) and body paragraphs
- the `.stepper-nav` buttons

Ids follow `<project-id>-tab-N` and `<project-id>-step-N`, and only panel 1 starts visible. No script changes are needed: `setupTabs` wires up every `.stepper` and `.demo`, and the print summary lists step titles on its own.

## Demo player

Copy the `.demo` block from either page. Tab and panel ids (`demo-tab-<key>`, `demo-<key>`) must be unique across the whole site. Before adding a video, check two things:
- YouTube allows embedding it: `https://www.youtube.com/oembed?url=<link>&format=json` returns 200 with an iframe.
- Its thumbnail exists: `https://i.ytimg.com/vi/<id>/maxresdefault.jpg`.

The player only loads YouTube when clicked. On a page opened from disk, YouTube refuses to play (Error 153), so the thumbnail opens YouTube instead. Test playback through a local server.

## Writing

- Use the humanizer skill. The reader is a recruiter with no robotics background, so use plain words and short sentences.
- Write the user's own work in first person, and credit others where the user did ("with the kaizen team"). Leave out what they didn't do.
- Every claim comes from the user or their code. No invented reasons, results or numbers.
- No em dashes. Use straight quotes.
- **Wikipedia links:** link a hard term the first time it appears on the page, never twice on one page. Use `<a class="wiki" href="https://en.wikipedia.org/wiki/<Article>" target="_blank" rel="noopener">`, and check that the article exists.
- **Definitions:** add a `WIKI_DEFS` entry keyed by the article path, in one or two plain sentences written for how the page uses the term. A link with no entry shows no definition box. When no article fits exactly, link the closest one and let the definition say what the page means (AprilTag links to "Fiducial marker").

## Diagrams

- **Content:** one diagram per step, with one main idea. The accent colour (`.key`, `.key-head`, `text.em`) marks only that idea; everything else stays neutral.
- **Clarity:** draw objects to be recognizable on sight (a robot on wheels, a camera with a lens, a rack of parts). Use the fewest shapes and labels possible, with labels placed next to what they name. No legends and no numbered badges.
- **Building them:** use `_docs/diagram_kit.py`, which has the parts, a preview command and the Toyota diagrams as examples. Diagrams are 360 wide. Their look comes from the `.step-diagram` rules in `index.html`; add a new class there, using theme variables, so both themes work.
- **Review:** look at every diagram in both themes and inside its stepper, at desktop and phone width. Check that no label overlaps a shape or gets clipped.

## Media

- **Photos:**
  - Remove all metadata, especially location, but keep the colour profile.
  - Resize so the long side is 2048 px, and save as JPEG at quality 85.
  - Name it `Images/<Company> <What>.jpg`.
  - A portrait photo in a landscape slot uses `style="height: 100%; object-fit: contain;"` so it shows whole.
- **Videos:** use the user's YouTube link as they gave it.
- **Clips in steppers:** a short clip with no sound can take a step's diagram slot. AMR Rack Delivery step 1 is the example; copy its `figure.step-clip` markup. The script under `/* ── Step clips ── */` plays it muted on a loop only while it's on screen, and with reduced motion turned on it shows the still frame and controls instead.
  - Convert it with ffmpeg to H.264 MP4 at 1280×720 and 30 fps, with no audio, no metadata (the location especially) and `-movflags +faststart`.
  - iPhone clips are HDR (HLG). Tone-map them to standard colour, or they look washed out in browsers. This is the filter chain step 1 used, after `setpts=PTS/2.5,fps=30` for the speed-up:

    ```
    zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,scale=1280:720,format=yuv420p
    ```
  - Save the clip's first frame beside it as the `poster`, named `<name> poster.jpg`.
  - Name the clip `Media/<Company> <What>.mp4`, and keep the original in `References/`, which git ignores.
  - If the clip is sped up, say so in an `.img-caption` under it ("2.5× speed"), and give the video an `aria-label` that describes it in one sentence.
  - When the reader needs a key to follow the clip, put a `ul.clip-legend` in the `figcaption`, one item per state with a coloured `.light` dot. AMR Rack Delivery step 4 is the example, with the call buttons' lights.

## Checks

- **Serve it** from the repo with `python3 -m http.server 4817 --bind 127.0.0.1`, and look at desktop, 390 px and 320 px wide in both themes. The page must be exactly as wide as the screen at every width.
- **Click through it:**
  - steps, using the tabs, the arrow keys, and Previous and Next
  - the video player: it plays, switching tabs stops it, and leaving the page stops it
  - definition boxes: on hover, and on tap with phone emulation
  - the print summary (`buildPrintSummary(null, 'full')` in the console)
  - the console, which must show no errors
- **Commit** with the same author identity as earlier commits (`git log -1 --format='%an <%ae>'`).

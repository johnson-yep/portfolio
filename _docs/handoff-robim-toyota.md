# Handoff: RoBIM and Toyota pages

Snapshot as of 2026-11-03. The rules for building internship pages are in `_docs/internship-layout.md`; this file is the state of the two pages built so far, and why they look the way they do. Update it when that changes.

## Status

- Both pages are finished. On 2026-10-31 the two CAD screenshots of the gripper attachment were added to RoBIM's Gripper Attachment section, and all three of its images (two CAD views and the photo) were cropped to 3:4 so they match.
- On 2026-11-03 the diagram in step 1 of Toyota's AMR Rack Delivery ("Ready the racks") was replaced with a looping clip of the robot hooking onto a rack and towing it away. The same day, its step 2 and 3 diagrams were redrawn. The clip, the redrawn diagrams and a same-day wording fix (the robot serves one moulding machine, not several) are committed locally; push only when the user asks.
- The pages went live on 2026-10-30, and the CAD images went live on 2026-10-31. Push only when the user asks, since a push deploys johnsonyep.com.
- `_config.yml` keeps `CLAUDE.md` off the website.

## Where things live in `index.html`

Search for these:

| What | Search for |
| --- | --- |
| The two pages | `<div id="cat-robim"`, `<div id="cat-toyota"` |
| Their homepage cards | `navigate('robim')`, `navigate('toyota')` inside `#cat-hub` |
| Shared page styles (overview, demo player, steppers) | `/* ── INTERNSHIP PAGES` |
| Diagram styles | `.step-diagram` |
| Definition box styles | `.wiki-tip` |
| Tab behaviour, shared by steppers and players | `/* ── Tabs ── */` (`setupTabs`) |
| Steppers' Previous and Next | `/* ── Steppers ── */` |
| Video players | `/* ── Demo players` |
| Definitions for Wikipedia links | `WIKI_DEFS` |
| Printable summary | `buildPrintSummary`, `PRINT_CATEGORIES` |

## RoBIM page (`#robim`)

- **Heading:** RoBIM Technologies, "Robotics & Software Engineering Intern", Sep 2026 to present. The title matches the user's resume. Headings use the full company name, and the prose says "RoBIM".
- **Overview:** the pitch, a player (Survey Scan, Pick and Place), "RoBIM and the HIVE", "Where I started", and the setup list. The result tiles (2.5× faster scans, 0.836 mAP) were removed on purpose; those numbers stay on the resume only. The videos carry their own captions, so the player has none.
- **Projects:**
  - Survey Scan: a 9-step stepper.
  - Pick and Place: a 5-step stepper.
  - Gripper Attachment: three 3:4 images in a row: the CAD model from the outside and the inside, then the photo on the robot. The CAD screenshots were enlarged to 768×1024 so they open at the same size as the photo in the zoom view.
- **Diagrams:** RoBIM's 14 diagrams were drawn with an earlier generator that wasn't kept. Edit their SVG in place, or redraw one with `_docs/diagram_kit.py`.
- **Content rules:** RoBIM has confidentiality rules for what the write-up may say. They're in the session's private memory, not in this public repo. Check them before editing RoBIM text, and ask the user if they aren't available.

## Toyota page (`#toyota`)

- **Heading:** Toyota Boshoku, "Robotics Engineering Intern", Jan to May 2026.
- **Overview:**
  - the pitch
  - a player (AMR Rack Delivery, Unload Station HMI, Screw Station HMI)
  - "Toyota Boshoku", naming the plant in Elmira, Ontario, which the user allowed
  - the setup list
- **Projects:**
  - AMR Rack Delivery: a 7-step stepper. Step 1 shows a looping clip, `Media/Toyota AMR Hook Demo.mp4`, at 2.5× speed with a "2.5× speed" caption. The original 39-second iPhone video is in `References/`, which git ignores. The user may still want it trimmed after seeing it.
  - Drop-off Vision System: a 6-step stepper, with the two camera images and the View Code button.
  - HMI Development: paragraphs only, since its How is too short for steps.
- **Diagrams:** `_docs/diagram_kit.py` reproduces all 13 exactly. The page shows 12 of them now, since the step 1 diagram was replaced by the clip; the kit still has it.
  - AMR Rack Delivery steps 2 and 3 were redrawn on 2026-11-03, because the user found the old ones said too little. Step 2 is a made-up floor map, not the plant's real layout. It shows the route between two docking points, a no-go zone, a speed-limit zone, and the robot with its two protective fields, "slow down" and "stop". Step 3 is the full-rack mission as a list of four actions, with a retry loop on each drive and a branch to "alert operators" when the mission fails. How operators got the alert isn't recorded, so no device is drawn; if the user names it, draw that device.
  - The kit runs with Python 3.13, installed for the user with winget on 2026-11-03 (`python` or `py` in a new terminal).
- **Code:** the vision program is at github.com/johnson-yep/amr-rack-detection. The GitHub account was renamed from PrestigeGiraffe, and the old address only redirects.

Facts the user confirmed (2026-10-30), so later edits don't undersell or overstate the work:

- **What the user built:** the whole AMR rack-delivery system, not just the vision program.
- **Robot work:**
  - MiR missions: full racks of freshly injection-moulded door parts go from the injection moulding machine to the drop-off lanes, empty racks go back, and other racks go elsewhere in the plant. Missions retry when stuck and alert operators on failure. The robot mainly serves that one machine, which makes all the door parts (confirmed 2026-11-03).
  - The robot's map, docking points, zones and charging.
  - Setting and adjusting the protective fields. They also replaced broken laser scanners a few times.
  - The hook and rack sizes, and printing the AprilTags.
  - Hook bars and tag frames on the racks, with the kaizen team: 7 rack types that the robot recognizes and tows (confirmed 2026-11-03).
- **Controls:**
  - Wireless buttons through a Banner DXM100 wired into the PLC's inputs.
  - Ladder logic that queues requests and calls missions through the MiR API.
  - An HMI status screen for the robot.
- **Lane choice:** the vision program sends the outermost free spot in each lane. PLC logic picks the lane, starting from the lane at the top of the camera's view. If the heartbeat stops, the robot falls back to checking each lane with its own sensors.
- **Rollout:** planning the layout (pick-up, drop-off and paths) with team members and operators, commissioning, training, work instructions and production support. Training went to 2 to 5 team leaders, who trained the other operators as needed (confirmed 2026-11-03). They also tracked analytics (racks moved in total and by type, distance, mission and idle time), but no longer have access to the figures. "Over 100 rack moves a shift" counts all missions.
- **Not the user's:** choosing, mounting and cabling the camera. Maintenance did that. The vision program runs on a maintenance computer that was already running.

## Known quirks

- **Videos from disk:** YouTube's player won't run on a page opened straight from disk (Error 153). There the thumbnail opens YouTube instead. Test playback at localhost.
- **AMR video thumbnail:** it's the video's own warped bird's-eye frame, with black edges. The user can set a custom thumbnail on YouTube.
- **Narrow phones:** the top menu is tightened for phones so every page fits 320 px.
- **Definition boxes:** they open on hover with a mouse. On touch screens the first tap shows the box and a second tap opens Wikipedia.

"""Drawing kit for the step diagrams on the internship pages.

Each diagram is a function returning (height, parts, description): the SVG
height for a 360-wide viewBox, a list of SVG snippets built from the parts
below, and the screen-reader description. svg(fn) wraps it as the
<svg class="step-diagram"> that goes first in a stepper panel.

The look comes from the .step-diagram rules in index.html (the classes used
here: device, frame, view, key, key-head, em, note, dash, faint, mask, hook,
nogo, ok, tag-bg, tag-ink, tag-ring). Add a new class there, with theme colours from CSS
variables, rather than hard-coding colours here.

The Toyota diagrams below double as examples. RoBIM's diagrams were drawn
with an earlier version of this kit that wasn't kept; their shapes (boards,
arm, gripper) can be copied from their SVGs in index.html.

    python3 _docs/diagram_kit.py preview /tmp/diagrams.html   # every diagram, both themes
    python3 _docs/diagram_kit.py svg amr-cv 2                  # one diagram, to paste in
"""
import html
import math
import sys


def n(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def pt(x, y):
    return f'{n(x)} {n(y)}'


def text(x, y, s, anchor='middle', cls=None):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    c = f' class="{cls}"' if cls else ''
    return f'<text x="{n(x)}" y="{n(y)}"{a}{c}>{html.escape(s)}</text>'


def rect(x, y, w, h, cls='', rx=0):
    r = f' rx="{n(rx)}"' if rx else ''
    c = f' class="{cls}"' if cls else ''
    return f'<rect{c} x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{r}/>'


def circle(x, y, r, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<circle{c} cx="{n(x)}" cy="{n(y)}" r="{n(r)}"/>'


def path(d, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<path{c} d="{d}"/>'


def arrow(x1, y1, x2, y2, key=True, curve=None):
    """Arrow from (x1, y1) to (x2, y2); accent when key. curve bends it
    through a control point."""
    if curve:
        cx, cy = curve
        a = math.atan2(y2 - cy, x2 - cx)
    else:
        a = math.atan2(y2 - y1, x2 - x1)
    ux, uy = math.cos(a), math.sin(a)
    ex, ey = x2 - 6 * ux, y2 - 6 * uy
    d = f'M{pt(x1, y1)} Q{pt(*curve)} {pt(ex, ey)}' if curve else f'M{pt(x1, y1)} L{pt(ex, ey)}'
    bx, by = x2 - 9 * ux, y2 - 9 * uy
    px, py = -uy * 4.5, ux * 4.5
    head = f'M{pt(x2, y2)} L{pt(bx + px, by + py)} L{pt(bx - px, by - py)} Z'
    return path(d, 'key' if key else '') + path(head, 'key-head' if key else 'lens')


def floor(x0, x1, y):
    hatch = ' '.join(f'M{pt(x, y)} l-6 7' for x in range(int(x0) + 10, int(x1), 12))
    return path(f'M{pt(x0, y)} H{n(x1)}') + path(hatch, 'hatch')


def camera(cx, cy):
    return (rect(cx - 13, cy - 15, 9, 5, 'device', 1.5) + rect(cx - 17, cy - 11, 34, 22, 'device', 4)
            + circle(cx, cy, 7, 'device') + circle(cx, cy, 3, 'lens'))


def door_part(x, y, w, h):
    """A moulded car door seen from the side: slanted window frame at the
    front and a window opening above the panel."""
    return (path(f'M{pt(x, y + h * 0.42)} L{pt(x + w * 0.38, y)} H{n(x + w - 2)} Q{pt(x + w, y)} {pt(x + w, y + 3)} '
                 f'V{n(y + h - 3)} Q{pt(x + w, y + h)} {pt(x + w - 3, y + h)} H{n(x + 3)} Q{pt(x, y + h)} {pt(x, y + h - 3)} Z', 'frame')
            + path(f'M{pt(x + w * 0.42, y + 4)} H{n(x + w - 4)} V{n(y + h * 0.38)} H{n(x + 6)} Z', 'faint'))


def rack_side(x, y, w, h, parts=3):
    """A wheeled rack of door parts seen from the side."""
    out = [path(f'M{pt(x, y)} V{n(y + h)} M{pt(x + w, y)} V{n(y + h)} M{pt(x, y)} H{n(x + w)} M{pt(x, y + h)} H{n(x + w)}', ''),
           circle(x + 10, y + h + 6, 5.5, 'device'), circle(x + w - 10, y + h + 6, 5.5, 'device')]
    pw = (w - 12) / parts
    for i in range(parts):
        out.append(door_part(x + 6 + i * pw, y + 10, pw - 6, h - 20))
    return ''.join(out)


def rack_top(x, y, w, h, cls='device'):
    """A rack seen from above: frame with a cross brace."""
    return rect(x, y, w, h, cls, 2) + path(f'M{pt(x + 3, y + 3)} L{pt(x + w - 3, y + h - 3)} M{pt(x + w - 3, y + 3)} L{pt(x + 3, y + h - 3)}', 'faint')


def apriltag(x, y, s):
    """A square AprilTag: black border with a block pattern."""
    c = s / 6
    cells = [(1, 1), (2, 1), (4, 1), (1, 2), (3, 2), (2, 3), (4, 3), (1, 4), (3, 4), (4, 4)]
    return (rect(x, y, s, s, 'tag-bg')
            + ''.join(rect(x + i * c, y + j * c, c, c, 'tag-ink') for i, j in cells)
            + path(f'M{pt(x, y)} h{n(s)} v{n(s)} h{n(-s)} Z M{pt(x + c, y + c)} v{n(4 * c)} h{n(4 * c)} v{n(-4 * c)} Z', 'tag-ring'))


def robot_side(x, y, hook_to=None):
    """MiR robot from the side: low body on wheels, hook arm on top reaching
    right to hook_to (x)."""
    out = [rect(x, y, 84, 20, 'device', 4), circle(x + 14, y + 22, 5, 'device'), circle(x + 70, y + 22, 5, 'device'),
           rect(x + 6, y + 5, 10, 4, 'faint', 1)]
    if hook_to:
        out.append(path(f'M{pt(x + 46, y)} V{n(y - 12)} H{n(hook_to)} V{n(y - 4)}', 'hook'))
    return ''.join(out)


def robot_top(cx, cy, w=26, h=18):
    """MiR robot from above, facing right."""
    return rect(cx - w / 2, cy - h / 2, w, h, 'device', 4) + path(f'M{pt(cx + w / 2 - 6, cy - 4)} L{pt(cx + w / 2 - 2, cy)} L{pt(cx + w / 2 - 6, cy + 4)}', '')


def plc(x, y):
    """PLC: a rack of modules with status lights."""
    out = [rect(x, y, 56, 40, 'device', 3)]
    for i in range(4):
        mx = x + 5 + i * 12.5
        out.append(rect(mx, y + 6, 9, 28, 'frame', 1.5))
        out.append(circle(mx + 4.5, y + 11, 1.4, 'key-head' if i == 0 else 'lens'))
    return ''.join(out)


def wireless_box(x, y):
    """DXM100-style wireless controller: box with an antenna."""
    return (rect(x, y, 44, 30, 'device', 3) + path(f'M{pt(x + 34, y)} V{n(y - 14)}') + circle(x + 34, y - 15, 2, 'lens')
            + rect(x + 7, y + 8, 18, 6, 'frame', 1.5) + circle(x + 10, y + 21, 1.6, 'lens') + circle(x + 16, y + 21, 1.6, 'lens'))


def push_button(cx, base_y):
    """Wireless push button on a small post."""
    return (rect(cx - 13, base_y - 14, 26, 14, 'device', 3) + path(f'M{pt(cx - 8, base_y - 14)} A8 8 0 0 1 {pt(cx + 8, base_y - 14)} Z', 'key-head'))


def waves(cx, cy, key=True):
    cls = 'key' if key else ''
    return ''.join(path(f'M{pt(cx - r * 0.7, cy - r * 0.7)} A{n(r)} {n(r)} 0 0 1 {pt(cx + r * 0.7, cy - r * 0.7)}', cls) for r in (6, 11))


def screen(x, y, w, h):
    """An HMI touchscreen: bezel and display."""
    return rect(x, y, w, h, 'device', 6) + rect(x + 7, y + 7, w - 14, h - 14, 'frame', 3)


def truss(x0, x1, y):
    web = ' '.join(f'M{pt(x, y)} L{pt(x + 12, y + 14)} L{pt(x + 24, y)}' for x in range(int(x0), int(x1) - 23, 24))
    return path(f'M{pt(x0, y)} H{n(x1)} M{pt(x0, y + 14)} H{n(x1)}') + path(web, 'faint')


def lane_grid(x, y, w, h, spots, full, mark=None, pct=None, cls_full='device'):
    """A lane seen from above split into spots; full lists the full spot
    indexes, mark outlines one spot in the accent colour."""
    sw = w / spots
    out = [rect(x, y, w, h, 'frame', 3)]
    for i in range(1, spots):
        out.append(path(f'M{pt(x + i * sw, y)} V{n(y + h)}', 'faint'))
    for i in full:
        out.append(rack_top(x + i * sw + 4, y + 4, sw - 8, h - 8, cls_full))
    if mark is not None:
        out.append(rect(x + mark * sw + 2, y + 2, sw - 4, h - 4, 'key', 2))
    if pct:
        for i, p in enumerate(pct):
            out.append(text(x + (i + 0.5) * sw, y + h + 15, p, cls='em' if i in full else None))
    return ''.join(out)


# ── AMR Rack Delivery ──

def amr_1():
    out = [floor(10, 350, 128),
           rack_side(170, 44, 150, 70, parts=3),
           rect(150, 92, 22, 7, 'key-head', 2),
           apriltag(176, 56, 20),
           robot_side(4, 100, hook_to=88),
           text(146, 100, 'hook bar', anchor='end', cls='em'),
           text(186, 38, 'AprilTag', cls='em')]
    return 140, out, ("A robot with a hook beside a wheeled rack of door parts. The rack has a hook bar for the robot "
                      "to grip and an AprilTag the robot reads to recognize it")


def amr_2():
    out = [rect(10, 10, 340, 146, 'frame', 8),
           rect(24, 34, 56, 46, 'device', 3), text(52, 98, 'machines'),
           rect(140, 24, 74, 42, 'view', 3), text(177, 49, 'slow'),
           rect(140, 104, 74, 38, 'nogo', 3), text(177, 128, 'no-go', cls='note'),
           path('M80 57 C 120 57 120 86 177 86 S 246 86 260 64', 'key dash')]
    for i in range(3):
        out.append(rect(270, 26 + i * 18, 66, 14, 'frame', 2))
    out += [circle(80, 57, 4, 'key-head'), circle(262, 60, 4, 'key-head'), text(303, 98, 'lanes'),
            robot_top(177, 86)]
    return 166, out, ("A map of the plant floor with the robot's path from the moulding machines to the drop-off lanes, "
                      "docking points at each end, a slow zone and a no-go zone")


def amr_3():
    out = [rect(118, 52, 88, 46, 'device', 3), text(162, 79, 'machines'),
           rect(258, 16, 88, 40, 'frame', 3), text(302, 41, 'lanes'),
           rect(258, 98, 88, 40, 'frame', 3), text(302, 123, 'other areas'),
           arrow(206, 64, 256, 38), arrow(206, 86, 256, 112),
           arrow(24, 75, 116, 75),
           text(226, 36, 'full racks', anchor='end', cls='em'), text(226, 128, 'other racks', anchor='end', cls='em'),
           text(68, 66, 'empty racks', cls='em')]
    return 148, out, ("The robot's missions as routes: full racks from the moulding machines to the drop-off lanes, "
                      "racks to other areas of the plant, and empty racks back to the machines")


def amr_4():
    out = [push_button(36, 92), waves(36, 72), text(36, 112, 'button'),
           wireless_box(96, 62), text(118, 112, 'DXM100'),
           path('M140 77 H176', 'key'), plc(178, 57), text(206, 112, 'PLC'),
           arrow(240, 77, 284, 77), text(262, 66, 'MiR API', cls='em'),
           rect(288, 66, 60, 16, 'device', 4), circle(298, 85, 4, 'device'), circle(338, 85, 4, 'device'),
           text(318, 112, 'robot')]
    return 120, out, ("A wireless button press goes to the DXM100, which is wired into the PLC, and the PLC starts the "
                      "robot's mission through the MiR API")


def amr_5():
    out = []
    for i in range(3):
        full = [[4, 5], [2, 3, 4, 5], [0, 1, 2, 3, 4, 5]][i]
        out.append(lane_grid(62, 24 + i * 40, 276, 28, 6, full, mark=3 if i == 0 else None))
    out += [robot_top(28, 38), arrow(44, 38, 244, 38), text(269, 16, 'drop here', cls='em'),
            text(200, 160, 'lanes are checked from the top', cls='note')]
    return 168, out, ("Three lanes of spots seen from above, with racks filling each lane from the far end. The robot "
                      "drives into the top lane, the first with room, to its outermost free spot")


def amr_6():
    out = [screen(84, 10, 192, 118), path('M168 128 V142 M146 142 H190'),
           text(110, 46, 'status', anchor='start'), rect(178, 35, 74, 15, 'key-head', 7.5),
           text(215, 46, 'running', cls='on-accent'),
           text(110, 74, 'mission', anchor='start'), rect(178, 65, 74, 12, 'frame', 3), text(215, 75, 'to lanes', cls='small'),
           text(110, 102, 'faults', anchor='start'), circle(184, 98, 5, 'ok'), text(196, 102, 'none', anchor='start', cls='small')]
    return 148, out, "An HMI touchscreen showing the robot's status, its current mission and any faults"


def amr_7():
    steps = ['plan layout', 'test', 'train', 'support']
    out = [path('M52 50 H308', 'faint')]
    for i, s in enumerate(steps):
        x = 52 + i * 85.3
        out += [circle(x, 50, 15, 'device'), path(f'M{pt(x - 6, 50)} l4.5 4.5 l8 -9', 'key'), text(x, 88, s)]
    return 100, out, ("The rollout in order: planning the layout with the team and operators, testing on the line, "
                      "training operators, and supporting the system in production")


# ── Drop-off Vision System ──

def cv_1():
    out = [truss(14, 346, 10), path('M180 24 V36'), camera(180, 52),
           path('M180 62 L112 148 L248 148 Z', 'view'),
           floor(10, 350, 148),
           rack_side(120, 92, 56, 44, parts=2), rack_side(184, 92, 56, 44, parts=2),
           rect(290, 90, 50, 32, 'device', 3), rect(295, 95, 40, 22, 'frame', 2), path('M315 122 V128'),
           path('M282 128 H348 M288 128 V148 M342 128 V148'),
           path('M197 52 C 236 52 266 92 288 104', 'key dash'),
           text(14, 44, 'roof truss', anchor='start', cls='note'),
           text(244, 48, 'video', anchor='start', cls='em'), text(315, 80, 'computer')]
    return 160, out, ("A camera hanging from the roof trusses looks down on racks in the drop-off lanes and streams video "
                      "to a nearby maintenance computer")


def cv_2():
    out = [rect(10, 14, 128, 100, 'frame', 6),
           path('M44 32 L104 32 L126 98 L22 98 Z'),
           path('M64 32 Q 58 66 57 98 M84 32 Q 90 66 91 98', 'faint'),
           arrow(146, 66, 214, 66), text(180, 56, 'homography', cls='em'),
           rect(222, 14, 128, 100, 'frame', 6),
           rect(240, 32, 92, 66), path('M270.7 32 V98 M301.3 32 V98', 'faint'),
           text(74, 132, 'camera view'), text(286, 132, "bird's-eye view")]
    for x, y in ((44, 32), (104, 32), (126, 98), (22, 98)):
        out.append(circle(x, y, 4, 'key-head'))
    return 142, out, ("The camera's angled view of the lanes, with four corner points, warped by a homography into a "
                      "straight-down bird's-eye view where the lanes are square")


def cv_3():
    out = [rect(10, 14, 140, 92, 'frame', 6), rect(210, 14, 140, 92, 'frame', 6)]
    racks = [(28, 30), (78, 30), (52, 66), (102, 66)]
    for x, y in racks:
        out.append(rack_top(x, y, 34, 24))
        out.append(rect(x + 200, y, 34, 24, 'mask', 2))
    out += [arrow(158, 60, 202, 60), text(180, 50, 'HSV', cls='em'),
            text(80, 124, 'frame'), text(280, 124, 'rack pixels', cls='em')]
    return 134, out, ("A camera frame of racks, and the same frame after picking out pixels in the racks' colour range, "
                      "where only the racks remain")


def cv_4():
    out = [rect(30, 30, 300, 40, 'frame', 3)]
    sw = 50
    for i in range(1, 6):
        out.append(path(f'M{30 + i * sw} 30 V70', 'faint'))
    pct = ['2%', '4%', '1%', '68%', '81%', '77%']
    for i in range(3, 6):
        out.append(rect(30 + i * sw + 8, 36, sw - 16, 28, 'mask', 2))
    out.append(rect(30 + 1 * sw + 30, 52, 10, 8, 'mask', 1))
    for i, p in enumerate(pct):
        out.append(text(30 + (i + 0.5) * sw, 88, p, cls='em' if i >= 3 else None))
    out += [text(105, 20, 'free'), text(255, 20, 'full', cls='em'), path('M180 26 V96', 'dash')]
    return 104, out, ("One lane split into six spots, each labelled with its share of rack-coloured pixels. Spots above "
                      "the threshold count as full")


def cv_5():
    out = [lane_grid(14, 40, 210, 32, 6, [3, 4, 5], mark=2),
           arrow(232, 50, 276, 50), text(254, 40, 'spot 3', cls='em'),
           path('M232 74 h8 v-7 h8 v7 h8 v-7 h8 v7 h6', ''),
           text(254, 94, 'heartbeat'),
           plc(282, 40), text(310, 96, 'PLC')]
    out.append(text(14 + 2.5 * 35, 92, 'outermost free', cls='em'))
    return 106, out, ("A lane with racks in its last three spots. The program sends the outermost free spot, spot 3, to "
                      "the PLC, along with a heartbeat signal that flips on every write")


def cv_6():
    out = [rect(70, 8, 220, 102, 'frame', 6),
           path('M128 26 L232 26 L262 94 L98 94 Z'),
           path('M163 26 L153 94 M197 26 L207 94', 'faint')]
    for x, y in ((128, 26), (232, 26), (262, 94), (98, 94)):
        out.append(circle(x, y, 4.5, 'key-head'))
    sliders = [('colour', 0.35), ('lens', 0.6), ('threshold', 0.45)]
    for i, (label, v) in enumerate(sliders):
        y = 130 + i * 20
        out += [text(150, y + 4, label, anchor='end'), path(f'M162 {y} H290', 'faint'), circle(162 + 128 * v, y, 5, 'device')]
    out.append(text(180, 19, 'corner points', cls='em'))
    return 180, out, ("The calibration screen: the live view with four draggable corner points for the bird's-eye view, "
                      "and sliders for the colour range, lens correction and detection threshold")


DIAGRAMS = {
    'amr-delivery': [amr_1, amr_2, amr_3, amr_4, amr_5, amr_6, amr_7],
    'amr-cv': [cv_1, cv_2, cv_3, cv_4, cv_5, cv_6],
}

ICON_ATTRS = ('viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"')
ICONS = {
    'amr-delivery': [
        '<rect x="6" y="4" width="14" height="13" rx="1"/><path d="M6 10.5h14M2.5 15h3.5"/><circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/>',
        '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
        '<path d="M4 8h13M14 5l3 3-3 3"/><path d="M20 16H7M10 13l-3 3 3 3"/>',
        '<rect x="5" y="14" width="14" height="6" rx="1.5"/><path d="M8.5 14a3.5 3.5 0 0 1 7 0"/><path d="M7.5 8.5a6.5 6.5 0 0 1 9 0"/>',
        '<path d="M12 21s-5.5-5.4-5.5-9.5a5.5 5.5 0 0 1 11 0C17.5 15.6 12 21 12 21z"/><circle cx="12" cy="11.5" r="2"/>',
        '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8.5 20h7M6.5 8h6M6.5 11.5h9"/>',
        '<path d="M10 6.5h10M10 12h10M10 17.5h10"/><path d="M3.5 6.5l1.5 1.5 2.5-3M3.5 12l1.5 1.5 2.5-3M3.5 17.5l1.5 1.5 2.5-3"/>',
    ],
    'amr-cv': [
        '<rect x="3" y="8" width="18" height="12" rx="2"/><circle cx="12" cy="14" r="3.5"/><path d="M7 8V6h5v2"/>',
        '<path d="M7 5h10l3.5 14h-17z"/><path d="M10.5 5l-1.5 14M13.5 5l1.5 14"/>',
        '<path d="M12 3.5s6 6.5 6 10.5a6 6 0 0 1-12 0c0-4 6-10.5 6-10.5z"/>',
        '<rect x="3" y="7" width="18" height="10" rx="1"/><path d="M9 7v10M15 7v10"/><path d="M16.8 12l1.2 1.3 1.9-2.3"/>',
        '<rect x="15" y="6" width="6" height="12" rx="1"/><path d="M3 12h9M9 9l3 3-3 3"/>',
        '<path d="M4 7h16M4 12h16M4 17h16"/><circle cx="9" cy="7" r="1.8" fill="currentColor" stroke="none"/><circle cx="15" cy="12" r="1.8" fill="currentColor" stroke="none"/><circle cx="7" cy="17" r="1.8" fill="currentColor" stroke="none"/>',
    ],
}



def svg(fn):
    height, parts, label = fn()
    return (f'<svg class="step-diagram" viewBox="0 0 360 {height}" role="img" aria-label="{html.escape(label)}" '
            f'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
            + ''.join(parts) + '</svg>')


def icon(project, i):
    return f'<svg {ICON_ATTRS}>{ICONS[project][i]}</svg>'


def preview(out):
    """Write a page showing every diagram and tab icon in dark and light."""
    import os
    import re
    page = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html'), encoding='utf-8').read()
    themes = re.search(r'(:root \{.*?\n        \}\n\n        \[data-theme="dark"\] \{.*?\n        \})', page, re.S).group(1)
    css = '\n'.join(line for line in page.split('\n') if line.strip().startswith('.step-diagram'))
    rows = []
    for project, fns in DIAGRAMS.items():
        for i, fn in enumerate(fns):
            rows.append(f'<h2>{project} step {i + 1}</h2><div class="row"><div class="cell" data-theme="dark">{svg(fn)}</div>'
                        f'<div class="cell">{svg(fn)}</div><div class="cell icon" data-theme="dark">{icon(project, i)}</div></div>')
    open(out, 'w', encoding='utf-8').write(f'''<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{themes}
body {{ margin: 0; padding: 16px; font-family: Inter, sans-serif; background: #777; }}
h2 {{ font-size: 12px; margin: 14px 0 6px; color: #fff; }}
.row {{ display: grid; grid-template-columns: 440px 440px 60px; gap: 10px; align-items: start; }}
.cell {{ background: var(--surface); color: var(--body); padding: 12px; border-radius: 10px; }}
.icon {{ color: var(--accent); }} .icon svg {{ width: 28px; height: 28px; }}
{css}
</style>{''.join(rows)}''')


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        preview(sys.argv[2])
    else:
        print(svg(DIAGRAMS[sys.argv[2]][int(sys.argv[3]) - 1]))

"""
Misaaq Takhmeen PDF Generator — Al-Kanz font edition
Usage: python3 generate_pdf.py              (uses sample data)
       python3 generate_pdf.py '{"token":"001","its":"1234567",...}'
Place Al-Kanz_0.ttf in the same folder as this script.
"""
import os, sys, json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

FONT_DIR = os.path.dirname(os.path.abspath(__file__))
pdfmetrics.registerFont(TTFont('AlKanz',      os.path.join(FONT_DIR, 'Al-Kanz_0.ttf')))
pdfmetrics.registerFont(TTFont('FreeSerif',   '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerifBold','/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'))

# ── Arabic reshaper ──────────────────────────────────────────
ARABIC_FORMS = {
    0x0627:('\uFE8D','\uFE8E','\uFE8D','\uFE8E'),0x0628:('\uFE8F','\uFE90','\uFE91','\uFE92'),
    0x062A:('\uFE95','\uFE96','\uFE97','\uFE98'),0x062B:('\uFE99','\uFE9A','\uFE9B','\uFE9C'),
    0x062C:('\uFE9D','\uFE9E','\uFE9F','\uFEA0'),0x062D:('\uFEA1','\uFEA2','\uFEA3','\uFEA4'),
    0x062E:('\uFEA5','\uFEA6','\uFEA7','\uFEA8'),0x062F:('\uFEA9','\uFEAA','\uFEA9','\uFEAA'),
    0x0630:('\uFEAB','\uFEAC','\uFEAB','\uFEAC'),0x0631:('\uFEAD','\uFEAE','\uFEAD','\uFEAE'),
    0x0632:('\uFEAF','\uFEB0','\uFEAF','\uFEB0'),0x0633:('\uFEB1','\uFEB2','\uFEB3','\uFEB4'),
    0x0634:('\uFEB5','\uFEB6','\uFEB7','\uFEB8'),0x0635:('\uFEB9','\uFEBA','\uFEBB','\uFEBC'),
    0x0636:('\uFEBD','\uFEBE','\uFEBF','\uFEC0'),0x0637:('\uFEC1','\uFEC2','\uFEC3','\uFEC4'),
    0x0638:('\uFEC5','\uFEC6','\uFEC7','\uFEC8'),0x0639:('\uFEC9','\uFECA','\uFECB','\uFECC'),
    0x063A:('\uFECD','\uFECE','\uFECF','\uFED0'),0x0641:('\uFED1','\uFED2','\uFED3','\uFED4'),
    0x0642:('\uFED5','\uFED6','\uFED7','\uFED8'),0x0643:('\uFED9','\uFEDA','\uFEDB','\uFEDC'),
    0x0644:('\uFEDD','\uFEDE','\uFEDF','\uFEE0'),0x0645:('\uFEE1','\uFEE2','\uFEE3','\uFEE4'),
    0x0646:('\uFEE5','\uFEE6','\uFEE7','\uFEE8'),0x0647:('\uFEE9','\uFEEA','\uFEEB','\uFEEC'),
    0x0648:('\uFEED','\uFEEE','\uFEED','\uFEEE'),0x064A:('\uFEF1','\uFEF2','\uFEF3','\uFEF4'),
    0x0649:('\uFEEF','\uFEF0','\uFEEF','\uFEF0'),0x0623:('\uFE83','\uFE84','\uFE83','\uFE84'),
    0x0625:('\uFE87','\uFE88','\uFE87','\uFE88'),0x0622:('\uFE81','\uFE82','\uFE81','\uFE82'),
    0x0626:('\uFE89','\uFE8A','\uFE8B','\uFE8C'),0x0629:('\uFE93','\uFE94','\uFE93','\uFE94'),
    0x06AF:('\uFB92','\uFB93','\uFB94','\uFB95'),0x0679:('\uFB66','\uFB67','\uFB68','\uFB69'),
}
NON_JOINING = {0x0627,0x062F,0x0630,0x0631,0x0632,0x0648,0x0649,0x0622,0x0623,0x0625,0x0629,0x0621}

def is_arabic(c):
    o = ord(c)
    return (0x0600 <= o <= 0x06FF) or (0x0750 <= o <= 0x077F)

def reshape(text):
    words = text.split(' '); result = []
    for word in words:
        if not any(is_arabic(c) for c in word):
            result.append(word); continue
        chars = list(word); n = len(chars); shaped = []
        for i, ch in enumerate(chars):
            o = ord(ch)
            if o not in ARABIC_FORMS: shaped.append(ch); continue
            pc = i > 0 and ord(chars[i-1]) in ARABIC_FORMS and ord(chars[i-1]) not in NON_JOINING
            nc = i < n-1 and is_arabic(chars[i+1])
            f = ARABIC_FORMS[o]
            if pc and nc and o not in NON_JOINING: shaped.append(f[3])
            elif pc: shaped.append(f[1])
            elif nc and o not in NON_JOINING: shaped.append(f[2])
            else: shaped.append(f[0])
        result.append(''.join(reversed(shaped)))
    return ' '.join(reversed(result))

# ── PDF generator ────────────────────────────────────────────
def generate_pdf(data, out_path):
    pw, ph = A4
    cv = canvas.Canvas(out_path, pagesize=A4)
    mg = 50; tl = mg; tr = pw - mg; tw = tr - tl

    C = Color
    border = C(0.3,0.25,0.2); lc   = C(0.7,0.65,0.6)
    dark   = C(0.12,0.09,0.07); lbg  = C(0.97,0.96,0.95)
    thbg   = C(0.91,0.88,0.84); trbg = C(0.98,0.97,0.95)
    body   = C(0.08,0.06,0.05); ltxt = C(0.2,0.17,0.13)

    def Y(y_from_top): return ph - y_from_top

    # Borders
    cv.setStrokeColor(border); cv.setLineWidth(1.5)
    cv.rect(tl-8, Y(ph-40), tw+16, ph-80, fill=0, stroke=1)
    cv.setLineWidth(0.5)
    cv.rect(tl-2, Y(ph-46), tw+4, ph-92, fill=0, stroke=1)

    yt = 50

    # Title (Al-Kanz for Arabic)
    cv.setFont('AlKanz', 20); cv.setFillColor(dark)
    cv.drawCentredString(pw/2, Y(yt+16), reshape('ميثاق فارم'))
    yt += 34

    cv.setStrokeColor(lc); cv.setLineWidth(0.5)
    cv.line(tl, Y(yt), tr, Y(yt)); yt += 18

    # Subtitle
    cv.setFillColor(dark)
    # Draw "فرزند ني Details" — Arabic right, Latin left, centred as a group
    cv.setFont('AlKanz', 13)
    ar_part = reshape('فرزند ني')
    ar_w = cv.stringWidth(ar_part, 'AlKanz', 13)
    lat_w = cv.stringWidth(' Details', 'FreeSerif', 13)
    group_w = ar_w + lat_w
    x_start = pw/2 - group_w/2
    cv.setFont('FreeSerif', 13)
    cv.drawString(x_start, Y(yt+12), ' Details')
    cv.setFont('AlKanz', 13)
    cv.drawString(x_start + lat_w, Y(yt+12), ar_part)
    yt += 24
    cv.line(tl, Y(yt), tr, Y(yt))

    rH = 36; lW = 145

    def drow(label, value, tall=False):
        nonlocal yt
        h = 52 if tall else rH
        ry = Y(yt+h)
        cv.setStrokeColor(lc); cv.setLineWidth(0.4)
        cv.setFillColor(lbg); cv.rect(tl, ry, tw, h, fill=1, stroke=1)
        cv.rect(tl, ry, lW, h, fill=1, stroke=0)
        cv.setStrokeColor(lc); cv.line(tl+lW, ry, tl+lW, ry+h)
        # Label in FreeSerifBold (Latin)
        cv.setFillColor(ltxt); cv.setFont('FreeSerifBold', 10)
        if tall:
            cv.drawString(tl+8, ry+h-18, label.split('&')[0].strip())
            cv.drawString(tl+8, ry+8, (label.split('&')[1].strip() if '&' in label else ''))
        else:
            cv.drawString(tl+8, ry+h/2+4, label)
        # Value in FreeSerif (to avoid Arabic-Indic numeral conversion)
        cv.setFont('FreeSerif', 11); cv.setFillColor(body)
        cv.drawString(tl+lW+10, ry+h/2+4, value or '')
        yt += h

    drow('TOKEN NO',       data.get('token',''))
    drow('ITS  NO',        data.get('its',''))
    drow('NAME',           data.get('name',''))
    drow('PLACE & MOHALLAH', data.get('place',''), tall=True)
    drow('MOBILE  NO',    data.get('mobile',''))

    # TAKHMEEN header
    ry = Y(yt+rH)
    cv.setFillColor(thbg); cv.setStrokeColor(lc)
    cv.rect(tl, ry, tw, rH, fill=1, stroke=1)
    cv.setFont('FreeSerifBold', 13); cv.setFillColor(dark)
    cv.drawCentredString(pw/2, ry+rH/2+4, 'TAKHMEEN')
    yt += rH

    alW = lW + 40

    def trow(arabic_label, value, label_font='AlKanz'):
        nonlocal yt
        ry = Y(yt+rH)
        cv.setStrokeColor(lc); cv.setLineWidth(0.4)
        cv.setFillColor(trbg); cv.rect(tl, ry, tw, rH, fill=1, stroke=1)
        cv.line(tl+alW, ry, tl+alW, ry+rH)
        cv.setFont(label_font, 12); cv.setFillColor(ltxt)
        cv.drawRightString(tl+alW-8, ry+rH/2+4, reshape(arabic_label))
        cv.setFont('FreeSerif', 11); cv.setFillColor(body)
        cv.drawString(tl+alW+10, ry+rH/2+4, value or '')
        yt += rH

    trow('نجوى الشكر',  data.get('njawa',''))
    trow('صلة الامام',  data.get('sila',''))
    trow('هدية السلام', data.get('hadiya',''))
    trow('سركاري لاگٹ', data.get('sarkari',''), label_font='FreeSerif')

    # Signature line — draw actual line + Al-Kanz label
    yt += 20
    sig_y = Y(yt+12)
    cv.setStrokeColor(lc); cv.setLineWidth(0.8)
    cv.line(tl+20, sig_y-2, tl+170, sig_y-2)   # drawn line instead of underscores
    cv.setFont('AlKanz', 12); cv.setFillColor(ltxt)
    cv.drawString(tl+185, sig_y, reshape('دستخط العامل'))
    yt += 30

    # Instructions divider
    cv.setStrokeColor(lc); cv.setLineWidth(0.5)
    cv.line(tl, Y(yt), tr, Y(yt)); yt += 16
    cv.setFont('FreeSerifBold', 10); cv.setFillColor(dark)
    cv.drawCentredString(pw/2, Y(yt+10), 'INSTRUCTIONS'); yt += 20

    cv.setFont('FreeSerif', 9); cv.setFillColor(C(0.28,0.23,0.18))
    for ln in [
        'This form is for Indian nationals (only). Register via Misaaq and submit this Takhmeen form.',
        'After filling, WhatsApp to +91 88664 85353. Mumineen must use the iPhone app.',
        "Login to ITS52.com on the live date using Farzand's ITS to complete Self Allocation.",
        'Use the platform to pay Njawa al-Shukr, Silat al-Imam, Hadiyat al-Salam, and Sarkari Lakat online.'
    ]:
        cv.drawCentredString(pw/2, Y(yt+9), ln); yt += 14

    cv.save()
    print(f'Saved: {out_path}')

if __name__ == '__main__':
    data = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {
        'token':'14475008', 'its':'30153829',
        'name':'Hussain bhai Naeem bhai Gittham',
        'place':'Orange County USA', 'mobile':'+1 (949) 617 7900',
        'njawa':'$1786', 'sila':'110', 'hadiya':'110', 'sarkari':'110'
    }
    out = data.pop('out', f"Misaaq_Takhmeen_{data.get('its','form')}.pdf")
    generate_pdf(data, out)

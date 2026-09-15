import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import datetime
import os

st.set_page_config(page_title="Biały Montaż - Kosztorys", layout="centered")

# --- CZCIONKA OBSŁUGUJĄCA POLSKIE ZNAKI ---
if os.path.exists("Roboto.ttf"):
    pdfmetrics.registerFont(TTFont("PolskiFont", "Roboto.ttf"))
    FONT_NORMAL = "PolskiFont"
    FONT_BOLD = "PolskiFont"
else:
    FONT_NORMAL = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

st.title("💡 Kosztorys: Biały Montaż")
st.caption("Kalkulator doboru osprzętu modułowego, ramek i robocizny instalacyjnej")

# 1. DANE ZLECENIA I SERIA OSPRZĘTU
with st.expander("1. Dane zlecenia i specyfikacja serii", expanded=True):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        firma = st.text_input("Wykonawca:", value="Elektro-Instal Jan Kowalski")
        klient = st.text_input("Inwestor:", value="Jan Nowak")
    with col_d2:
        nr_oferty = st.text_input("Numer oferty:", value="BM/2026/01")
        adres = st.text_input("Adres inwestycji:", value="ul. Modrzewiowa 12, Warszawa")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        seria_osprzetu = st.selectbox(
            "Seria osprzętu:",
            ["Kontakt-Simon 54 Premium", "Kontakt-Simon 10", "Schneider Sedna Design", "Legrand Niloe Step", "Ospel Sonata"]
        )
    with col_s2:
        kolor_osprzetu = st.selectbox(
            "Kolor osprzętu / klawiszy:",
            ["Biały", "Antracyt mat", "Czarny mat", "Srebrny mat", "Kremowy", "Inox / Stal"]
        )

# Domyślna stawka robocizny za montaż 1 modułu/mechanizmu
with st.expander("Stawka robocizny", expanded=False):
    robocizna_stawka_modul = st.number_input("Stawka robocizny za montaż 1 mechanizmu/punktu (zł):", value=25.0, step=2.0)
    robocizna_stawka_lampa = st.number_input("Stawka robocizny za montaż 1 lampy / kinkietu (zł):", value=75.0, step=5.0)

# 2. GNIAZDA 230V I SPECJALNE
with st.expander("2. Gniazda (230V, bryzgoszczelne, USB, Siła)", expanded=False):
    st.markdown("**Gniazda wtykowe**")
    cg1, cg2 = st.columns(2)
    q_g1 = cg1.number_input("Gniazdo pojedyncze 230V z uziemieniem (szt.):", value=35, step=1)
    p_g1 = cg2.number_input("Cena materiału za gniazdo pojedyncze (zł):", value=16.50, step=1.0)

    q_g2 = cg1.number_input("Gniazdo podwójne do ramki (szt.):", value=10, step=1)
    p_g2 = cg2.number_input("Cena materiału za gniazdo podwójne (zł):", value=24.00, step=1.0)

    q_g_ip = cg1.number_input("Gniazdo z klapką IP44 łazienka/kuchnia (szt.):", value=4, step=1)
    p_g_ip = cg2.number_input("Cena materiału IP44 z klapką (zł):", value=22.00, step=1.0)

    q_g_usb = cg1.number_input("Gniazdo podwójne z ładowarką USB-A+C (szt.):", value=2, step=1)
    p_g_usb = cg2.number_input("Cena materiału za gniazdo USB (zł):", value=115.00, step=5.0)

    q_g_sila = cg1.number_input("Gniazdo siłowe 16A/32A natynkowe/stałe (szt.):", value=1, step=1)
    p_g_sila = cg2.number_input("Cena materiału gniazdo siłowe (zł):", value=65.00, step=5.0)

# 3. ŁĄCZNIKI I STEROWANIE OŚWIETLENIEM
with st.expander("3. Łączniki, ściemniacze i żaluzje", expanded=False):
    cl1, cl2 = st.columns(2)
    q_sw1 = cl1.number_input("Łącznik 1-biegunowy (pojedynczy) [szt.]:", value=8, step=1)
    p_sw1 = cl2.number_input("Cena mat. łącznik 1-bieg. (zł):", value=15.00, step=1.0)

    q_sw2 = cl1.number_input("Łącznik świecznikowy (podwójny) [szt.]:", value=6, step=1)
    p_sw2 = cl2.number_input("Cena mat. łącznik świecznikowy (zł):", value=18.50, step=1.0)

    q_sw_sch = cl1.number_input("Łącznik schodowy / krzyżowy [szt.]:", value=6, step=1)
    p_sw_sch = cl2.number_input("Cena mat. schodowy/krzyżowy (zł):", value=21.00, step=1.0)

    q_sw_zal = cl1.number_input("Łącznik żaluzjowy (roletowy) [szt.]:", value=4, step=1)
    p_sw_zal = cl2.number_input("Cena mat. łącznik żaluzjowy (zł):", value=28.00, step=1.0)

    q_sw_dim = cl1.number_input("Ściemniacz obrotowy / LED [szt.]:", value=1, step=1)
    p_sw_dim = cl2.number_input("Cena mat. ściemniacz LED (zł):", value=145.00, step=5.0)

# 4. TELETECHNIKA
with st.expander("4. Gniazda teletechniczne (LAN, TV, SAT, Audio)", expanded=False):
    ct1, ct2 = st.columns(2)
    q_rj45 = ct1.number_input("Gniazdo komputerowe RJ45 kat. 6 (szt.):", value=6, step=1)
    p_rj45 = ct2.number_input("Cena mat. gniazdo RJ45 kat. 6 (zł):", value=32.00, step=2.0)

    q_tv = ct1.number_input("Gniazdo TV-R-SAT końcowe (szt.):", value=3, step=1)
    p_tv = ct2.number_input("Cena mat. gniazdo TV/SAT (zł):", value=29.00, step=2.0)

# 5. RAMKI WIELOKROTNE
with st.expander("5. Ramki wielokrotne", expanded=False):
    cr1, cr2 = st.columns(2)
    q_r1 = cr1.number_input("Ramka pojedyncza 1-krotna (szt.):", value=15, step=1)
    p_r1 = cr2.number_input("Cena ramki 1x (zł):", value=6.50, step=0.5)

    q_r2 = cr1.number_input("Ramka 2-krotna (szt.):", value=12, step=1)
    p_r2 = cr2.number_input("Cena ramki 2x (zł):", value=11.50, step=1.0)

    q_r3 = cr1.number_input("Ramka 3-krotna (szt.):", value=8, step=1)
    p_r3 = cr2.number_input("Cena ramki 3x (zł):", value=16.50, step=1.0)

    q_r4 = cr1.number_input("Ramka 4-krotna (szt.):", value=3, step=1)
    p_r4 = cr2.number_input("Cena ramki 4x (zł):", value=24.00, step=1.0)

    q_r5 = cr1.number_input("Ramka 5-krotna (szt.):", value=1, step=1)
    p_r5 = cr2.number_input("Cena ramki 5x (zł):", value=36.00, step=2.0)

# 6. OŚWIETLENIE (MONTAŻ OPRAW)
with st.expander("6. Montaż opraw oświetleniowych (Lampy, Kinkiety, LED)", expanded=False):
    co1, co2 = st.columns(2)
    q_lampa_wisz = co1.number_input("Montaż lampy wiszącej / żyrandola (szt.):", value=5, step=1)
    p_lampa_wisz = co2.number_input("Stawka montażu lampy wiszącej (zł):", value=robocizna_stawka_lampa, step=5.0)

    q_spot = co1.number_input("Montaż oczka / oprawy wpuszczanej LED (szt.):", value=18, step=1)
    p_spot = co2.number_input("Stawka montażu oczka LED (zł):", value=30.0, step=5.0)

    q_kinkiet = co1.number_input("Montaż kinkietu ściennego (szt.):", value=4, step=1)
    p_kinkiet = co2.number_input("Stawka montażu kinkietu (zł):", value=50.0, step=5.0)

    q_led_m = co1.number_input("Montaż taśmy LED w profilu [mb]:", value=10, step=1)
    p_led_m = co2.number_input("Stawka montażu LED (zł/mb):", value=40.0, step=5.0)

# PODATKI
vat_dict = {"8% (Mieszkaniowy)": 0.08, "23% (Komercyjny / Faktura)": 0.23, "0% (Zwolnienie z VAT)": 0.00}
vat_choice = st.selectbox("Stawka podatku VAT:", list(vat_dict.keys()))
vat_rate = vat_dict[vat_choice]

# POZYCJE KOSZTORYSOWE: (Nazwa, Ilość, Jm, Cena_mat_j., Montaz_j.)
positions = [
    # Gniazda
    (f"Gniazdo 230V pojedyncze ({seria_osprzetu}, {kolor_osprzetu})", q_g1, "szt.", p_g1, robocizna_stawka_modul),
    (f"Gniazdo 230V podwójne ({seria_osprzetu}, {kolor_osprzetu})", q_g2, "szt.", p_g2, robocizna_stawka_modul),
    (f"Gniazdo IP44 bryzgoszczelne z klapką ({kolor_osprzetu})", q_g_ip, "szt.", p_g_ip, robocizna_stawka_modul),
    (f"Gniazdo zintegrowane 2xUSB A+C ({kolor_osprzetu})", q_g_usb, "szt.", p_g_usb, robocizna_stawka_modul),
    ("Gniazdo siłowe 16A/32A", q_g_sila, "szt.", p_g_sila, 60.0),
    # Łączniki
    (f"Łącznik 1-biegunowy pojedynczy ({kolor_osprzetu})", q_sw1, "szt.", p_sw1, robocizna_stawka_modul),
    (f"Łącznik świecznikowy podwójny ({kolor_osprzetu})", q_sw2, "szt.", p_sw2, robocizna_stawka_modul),
    (f"Łącznik schodowy / krzyżowy ({kolor_osprzetu})", q_sw_sch, "szt.", p_sw_sch, robocizna_stawka_modul),
    (f"Łącznik żaluzjowy roletowy ({kolor_osprzetu})", q_sw_zal, "szt.", p_sw_zal, robocizna_stawka_modul),
    (f"Ściemniacz oświetlenia LED ({kolor_osprzetu})", q_sw_dim, "szt.", p_sw_dim, robocizna_stawka_modul),
    # Teletechnika
    (f"Gniazdo komputerowe RJ45 kat. 6 ({kolor_osprzetu})", q_rj45, "szt.", p_rj45, robocizna_stawka_modul + 10.0),
    (f"Gniazdo R-TV-SAT końcowe ({kolor_osprzetu})", q_tv, "szt.", p_tv, robocizna_stawka_modul),
    # Ramki (tylko materiał, montaż wliczony w montaż punktu)
    (f"Ramka 1-krotna ({seria_osprzetu}, {kolor_osprzetu})", q_r1, "szt.", p_r1, 0.0),
    (f"Ramka 2-krotna ({seria_osprzetu}, {kolor_osprzetu})", q_r2, "szt.", p_r2, 0.0),
    (f"Ramka 3-krotna ({seria_osprzetu}, {kolor_osprzetu})", q_r3, "szt.", p_r3, 0.0),
    (f"Ramka 4-krotna ({seria_osprzetu}, {kolor_osprzetu})", q_r4, "szt.", p_r4, 0.0),
    (f"Ramka 5-krotna ({seria_osprzetu}, {kolor_osprzetu})", q_r5, "szt.", p_r5, 0.0),
    # Lampy (sama usługa montażu powierzonych opraw)
    ("Montaż lampy wiszącej / żyrandola", q_lampa_wisz, "szt.", 0.0, p_lampa_wisz),
    ("Montaż wpustu sufitowego / oczka LED", q_spot, "szt.", 0.0, p_spot),
    ("Montaż kinkietu ściennego", q_kinkiet, "szt.", 0.0, p_kinkiet),
    ("Montaż taśmy LED w profilu aluminiowym", q_led_m, "mb", 0.0, p_led_m),
]

# OBLICZENIA SUMARYCZNE
total_material = sum(q * p_mat for _, q, _, p_mat, _ in positions if q > 0)
total_work = sum(q * p_work for _, q, _, _, p_work in positions if q > 0)
total_net = total_material + total_work
total_vat = total_net * vat_rate
total_gross = total_net + total_vat

st.divider()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Materiał (Osprzęt)", f"{total_material:,.2f} zł")
k2.metric("Robocizna", f"{total_work:,.2f} zł")
k3.metric("Suma Netto", f"{total_net:,.2f} zł")
k4.metric("DO ZAPŁATY (Brutto)", f"{total_gross:,.2f} zł")

# --- GENERATOR DOKUMENTU PDF ---
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=35, rightMargin=35, topMargin=35, bottomMargin=35)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=16, leading=20, textColor=colors.HexColor("#0f172a"))
    text_bold = ParagraphStyle('TBold', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9, leading=12)
    text_normal = ParagraphStyle('TNorm', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=8, leading=10)
    text_center = ParagraphStyle('TCtr', parent=text_normal, alignment=1)
    text_right = ParagraphStyle('TRgt', parent=text_normal, alignment=2)
    header_style = ParagraphStyle('Hdr', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8, leading=10, textColor=colors.HexColor("#0f172a"))

    elements = []

    elements.append(Paragraph("KOSZTORYS I ZESTAWIENIE: BIAŁY MONTAŻ", title_style))
    elements.append(Paragraph(f"Nr oferty: <b>{nr_oferty}</b> | Data: {datetime.date.today().strftime('%d.%m.%Y')}", text_normal))
    elements.append(Paragraph(f"Specyfikacja osprzętu: <b>{seria_osprzetu}</b> | Wykończenie/Kolor: <b>{kolor_osprzetu}</b>", text_normal))
    elements.append(Spacer(1, 10))

    parties_data = [
        [Paragraph(f"<b>WYKONAWCA:</b><br/>{firma}", text_normal),
         Paragraph(f"<b>INWESTOR:</b><br/>{klient}<br/>Adres: {adres}", text_normal)]
    ]
    t_parties = Table(parties_data, colWidths=[260, 260])
    t_parties.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_parties)
    elements.append(Spacer(1, 12))

    table_data = [[
        Paragraph("Wyszczególnienie osprzętu i robocizny", header_style),
        Paragraph("Ilość", header_style),
        Paragraph("Jm", header_style),
        Paragraph("Cena jedn.", header_style),
        Paragraph("Wartość", header_style)
    ]]

    for name, q, unit, p_mat, p_work in positions:
        if q > 0:
            unit_total = p_mat + p_work
            line_total = q * unit_total
            table_data.append([
                Paragraph(name, text_normal),
                Paragraph(str(q), text_center),
                Paragraph(unit, text_center),
                Paragraph(f"{unit_total:.2f} zł", text_right),
                Paragraph(f"{line_total:.2f} zł", text_right)
            ])

    t_items = Table(table_data, colWidths=[260, 45, 35, 80, 100])
    t_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_items)
    elements.append(Spacer(1, 10))

    summary_data = [
        [Paragraph("Suma Materiał (osprzęt):", text_normal), Paragraph(f"{total_material:,.2f} zł", text_right)],
        [Paragraph("Suma Robocizna (montaż):", text_normal), Paragraph(f"{total_work:,.2f} zł", text_right)],
        [Paragraph("Suma Netto łączna:", text_bold), Paragraph(f"<b>{total_net:,.2f} zł</b>", text_right)],
        [Paragraph(f"Podatek VAT ({int(vat_rate*100)}%):", text_normal), Paragraph(f"{total_vat:,.2f} zł", text_right)],
        [Paragraph("<b>DO ZAPŁATY BRUTTO:</b>", text_bold), Paragraph(f"<b>{total_gross:,.2f} zł</b>", text_right)]
    ]
    t_sum = Table(summary_data, colWidths=[150, 100], hAlign='RIGHT')
    t_sum.setStyle(TableStyle([
        ('LINEABOVE', (0,2), (1,2), 0.5, colors.grey),
        ('LINEABOVE', (0,4), (1,4), 1.5, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_sum)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Podpis wykonawcy: ...........................................", text_normal))

    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_file = generate_pdf()
st.download_button(
    label="📥 Pobierz Kosztorys Białego Montażu w PDF",
    data=pdf_file,
    file_name=f"Bialy_Montaz_{nr_oferty.replace('/', '_')}.pdf",
    mime="application/pdf",
    use_container_width=True
)

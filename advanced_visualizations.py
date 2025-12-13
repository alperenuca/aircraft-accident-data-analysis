import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Stil ayarları
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 60)
print("   HAVACILİK GÜVENLİĞİ - GELİŞMİŞ GÖRSELLEŞTİRME ANALİZİ")
print("=" * 60)

#Elimde bulunan dataset
FILE_PATH = 'Airplane_Crashes_and_Fatalities_Since_1908.csv'

DTYPE_MAPPING = {
    'Fatalities': float,
    'Aboard': float
}

try:
    df = pd.read_csv(
        FILE_PATH, 
        encoding='latin1', 
        on_bad_lines='skip', 
        sep=',', 
        engine='python',
        dtype=DTYPE_MAPPING
    ) 
except FileNotFoundError:
    print(f"HATA: '{FILE_PATH}' dosyası bulunamadı!")
    exit()

df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True).str.strip()
df.rename(columns={'Date': 'CrashDate'}, inplace=True)

df = df[['CrashDate', 'Time', 'Location', 'Operator', 'Type', 'Fatalities', 'Aboard', 'Summary']]
df.dropna(subset=['Fatalities', 'Aboard'], inplace=True)

df['Year'] = pd.to_datetime(df['CrashDate'], errors='coerce').dt.year
df.dropna(subset=['Year'], inplace=True)
df['Year'] = df['Year'].astype(int)

df['FatalityRatio'] = df['Fatalities'] / df['Aboard']
df.loc[df['Aboard'] == 0, 'FatalityRatio'] = 0
df.loc[df['FatalityRatio'] > 1, 'FatalityRatio'] = 1

df['Decade'] = (df['Year'] // 10) * 10
df['Is_Fatal'] = (df['FatalityRatio'] >= 0.5).astype(int)

df['Operator_Category'] = df['Operator'].apply(
    lambda x: 'Askeri' if 'Military' in str(x) or 'Air Force' in str(x) or 'Army' in str(x) or 'Navy' in str(x) or 'Marine' in str(x)
    else 'Sivil'
)

print(f"\n✓ Toplam {len(df)} kaza analiz edilecek")
print(f"✓ Tarih aralığı: {df['Year'].min()} - {df['Year'].max()}")

# GRAFİK 1: PASTA GRAFİĞİ - Askeri vs Sivil Kazalar
print("\n[1/10] Pasta Grafik: Askeri vs Sivil Kaza Dağılımı")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

#Kaza sayısı
operator_counts = df['Operator_Category'].value_counts()
colors = ['#ff6b6b', '#4ecdc4']
explode = (0.05, 0.05)

ax1.pie(operator_counts, labels=operator_counts.index, autopct='%1.1f%%',
        startangle=90, colors=colors, explode=explode, shadow=True,
        textprops={'fontsize': 12, 'weight': 'bold'})
ax1.set_title('Kaza Sayısı Dağılımı\n(Askeri vs Sivil)', fontsize=14, weight='bold')

#Toplam hayatını kaybeden sayısı
fatalities_by_category = df.groupby('Operator_Category')['Fatalities'].sum()
ax2.pie(fatalities_by_category, labels=fatalities_by_category.index, autopct='%1.1f%%',
        startangle=90, colors=colors, explode=explode, shadow=True,
        textprops={'fontsize': 12, 'weight': 'bold'})
ax2.set_title('Toplam Ölüm Dağılımı\n(Askeri vs Sivil)', fontsize=14, weight='bold')

plt.tight_layout()
plt.savefig('viz_1_pie_military_vs_civil.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_1_pie_military_vs_civil.png")
plt.close()


# GRAFİK 2: YATAY BAR CHART - En Çok Kaza Yapan 20 Operatör
print("[2/10] Yatay Bar Chart: En Çok Kaza Yapan Operatörler")

top_operators = df['Operator'].value_counts().head(20)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top_operators)), top_operators.values, 
               color=plt.cm.Reds(np.linspace(0.4, 0.9, len(top_operators))))

ax.set_yticks(range(len(top_operators)))
ax.set_yticklabels(top_operators.index, fontsize=10)
ax.set_xlabel('Kaza Sayısı', fontsize=12, weight='bold')
ax.set_title(f'En Çok Kaza Yapan 20 Operatör ({df["Year"].min()}-{df["Year"].max()})', fontsize=14, weight='bold')
ax.invert_yaxis()

for i, (bar, value) in enumerate(zip(bars, top_operators.values)):
    ax.text(value + 1, i, str(int(value)), va='center', fontsize=9, weight='bold')

plt.tight_layout()
plt.savefig('viz_2_bar_top_operators.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_2_bar_top_operators.png")
plt.close()

# GRAFİK 3: SCATTER PLOT - Uçaktaki Kişi Sayısı vs Ölüm Oranı
print("[3/10] Scatter Plot: Uçak Kapasitesi vs Ölüm Oranı")

fig, ax = plt.subplots(figsize=(12, 7))

scatter = ax.scatter(df['Aboard'], df['FatalityRatio'], 
                     c=df['Year'], cmap='viridis', 
                     alpha=0.6, s=30, edgecolors='black', linewidth=0.5)

ax.set_xlabel('Uçaktaki Kişi Sayısı', fontsize=12, weight='bold')
ax.set_ylabel('Ölüm Oranı (Fatality Ratio)', fontsize=12, weight='bold')
ax.set_title('Uçak Kapasitesi ile Ölüm Oranı İlişkisi', fontsize=14, weight='bold')
ax.set_xlim(0, 600)
ax.grid(True, alpha=0.3)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Yıl', fontsize=11, weight='bold')

plt.tight_layout()
plt.savefig('viz_3_scatter_capacity_vs_fatality.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_3_scatter_capacity_vs_fatality.png")
plt.close()

# GRAFİK 4: ÇOKLU ÇİZGİ GRAFİĞİ - Dekatlara Göre Trend
print("[4/10] Çizgi Grafik: Dekatlara Göre Kaza ve Ölüm Trendi")

decade_stats = df.groupby('Decade').agg({
    'Fatalities': 'sum',
    'Operator': 'count'
}).rename(columns={'Operator': 'Crash_Count'})

fig, ax1 = plt.subplots(figsize=(14, 7))

color1 = '#e74c3c'
ax1.set_xlabel('Dekat (On Yıl)', fontsize=12, weight='bold')
ax1.set_ylabel('Toplam Kaza Sayısı', color=color1, fontsize=12, weight='bold')
line1 = ax1.plot(decade_stats.index, decade_stats['Crash_Count'], 
                 color=color1, marker='o', linewidth=3, markersize=8, label='Kaza Sayısı')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
color2 = '#3498db'
ax2.set_ylabel('Toplam Ölüm Sayısı', color=color2, fontsize=12, weight='bold')
line2 = ax2.plot(decade_stats.index, decade_stats['Fatalities'], 
                 color=color2, marker='s', linewidth=3, markersize=8, label='Ölüm Sayısı')
ax2.tick_params(axis='y', labelcolor=color2)

ax1.set_title(f'Havacılık Kazaları ve Ölümleri - Dekat Bazlı Trend ({df["Year"].min()}-{df["Year"].max()})', 
              fontsize=14, weight='bold')

# X ekseninde tüm dekatları göster
ax1.set_xticks(decade_stats.index)
ax1.set_xticklabels(decade_stats.index, rotation=45, ha='right')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=11)

plt.tight_layout()
plt.savefig('viz_4_line_decade_trends.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_4_line_decade_trends.png")
plt.close()


# GRAFİK 5: HEATMAP - Yıllara ve Operatör Kategorisine Göre Ortalama Ölüm
print("[5/10] Heatmap: Yıl ve Operatör Kategorisine Göre Ortalama Ölüm")

# 5 yıllık periyotlar oluştur
df['Period'] = (df['Year'] // 5) * 5
period_operator_avg = df.pivot_table(
    values='Fatalities', 
    index='Operator_Category', 
    columns='Period', 
    aggfunc='mean'
)

# Son 20 periyodu al (100 yıl)
period_operator_avg = period_operator_avg.iloc[:, -20:]

fig, ax = plt.subplots(figsize=(16, 5))
sns.heatmap(period_operator_avg, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Ortalama Ölüm Sayısı'}, linewidths=0.5, ax=ax)
ax.set_title('5 Yıllık Periyotlarda Ortalama Ölüm Sayısı (Askeri vs Sivil)', 
             fontsize=14, weight='bold')
ax.set_xlabel('Periyot (5 Yıllık)', fontsize=12, weight='bold')
ax.set_ylabel('Operatör Kategorisi', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig('viz_5_heatmap_period_operator.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_5_heatmap_period_operator.png")
plt.close()

# GRAFİK 6: VIOLIN PLOT - Ölüm Oranı Dağılımı (Askeri vs Sivil)
print("[6/10] Violin Plot: Ölüm Oranı Dağılımı Karşılaştırması")

fig, ax = plt.subplots(figsize=(10, 7))

violin_parts = ax.violinplot(
    [df[df['Operator_Category'] == 'Askeri']['FatalityRatio'].dropna(),
     df[df['Operator_Category'] == 'Sivil']['FatalityRatio'].dropna()],
    positions=[1, 2],
    showmeans=True,
    showmedians=True,
    widths=0.7
)

#Renk Ayarlarım
colors = ['#ff6b6b', '#4ecdc4']
for i, pc in enumerate(violin_parts['bodies']):
    pc.set_facecolor(colors[i])
    pc.set_alpha(0.7)

ax.set_xticks([1, 2])
ax.set_xticklabels(['Askeri', 'Sivil'], fontsize=12, weight='bold')
ax.set_ylabel('Ölüm Oranı (Fatality Ratio)', fontsize=12, weight='bold')
ax.set_title('Ölüm Oranı Dağılımı: Askeri vs Sivil Kazalar', fontsize=14, weight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('viz_6_violin_fatality_distribution.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_6_violin_fatality_distribution.png")
plt.close()


# GRAFİK 7: STACKED BAR - Dekatlara Göre Ölümcül vs Ölümsüz Kazalar
print("[7/10] Stacked Bar: Dekatlara Göre Kaza Şiddeti")

decade_severity = df.groupby(['Decade', 'Is_Fatal']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(14, 7))

decade_severity.plot(kind='bar', stacked=True, ax=ax, 
                     color=['#2ecc71', '#e74c3c'], width=0.8)

ax.set_xlabel('Dekat', fontsize=12, weight='bold')
ax.set_ylabel('Kaza Sayısı', fontsize=12, weight='bold')
ax.set_title('Dekatlara Göre Ölümcül ve Ölümsüz Kaza Dağılımı', fontsize=14, weight='bold')
ax.legend(['Ölümsüz (<%50 ölüm)', 'Ölümcül (≥%50 ölüm)'], fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('viz_7_stacked_bar_severity_by_decade.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_7_stacked_bar_severity_by_decade.png")
plt.close()


# GRAFİK 8: DONUT CHART - En Ölümcül 10 Uçak Tipi
print("[8/10] Donut Chart: En Ölümcül Uçak Tipleri")

# En çok ölüme neden olan uçak tipleri
aircraft_fatalities = df.groupby('Type')['Fatalities'].sum().nlargest(10)

fig, ax = plt.subplots(figsize=(10, 10))

colors_donut = plt.cm.Spectral(np.linspace(0.2, 0.8, len(aircraft_fatalities)))
wedges, texts, autotexts = ax.pie(aircraft_fatalities, labels=aircraft_fatalities.index,
                                    autopct='%1.1f%%', startangle=90, colors=colors_donut,
                                    pctdistance=0.85, textprops={'fontsize': 9})

# Donut efekti için merkeze beyaz daire
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
ax.add_artist(centre_circle)

ax.set_title('En Çok Ölüme Neden Olan 10 Uçak Tipi\n(Toplam Ölüm Sayısına Göre)', 
             fontsize=14, weight='bold', pad=20)

plt.tight_layout()
plt.savefig('viz_8_donut_aircraft_types.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_8_donut_aircraft_types.png")
plt.close()

# GRAFİK 9: AREA CHART - Yıllara Göre Kümülatif Ölüm
print("[9/10] Area Chart: Kümülatif Ölüm Trendi")

yearly_fatalities = df.groupby('Year')['Fatalities'].sum().sort_index()
cumulative_fatalities = yearly_fatalities.cumsum()

fig, ax = plt.subplots(figsize=(14, 7))

ax.fill_between(cumulative_fatalities.index, cumulative_fatalities.values, 
                alpha=0.7, color='#e74c3c', label='Kümülatif Ölüm')
ax.plot(cumulative_fatalities.index, cumulative_fatalities.values, 
        color='#c0392b', linewidth=2)

ax.set_xlabel('Yıl', fontsize=12, weight='bold')
ax.set_ylabel('Kümülatif Ölüm Sayısı', fontsize=12, weight='bold')
ax.set_title(f'Havacılık Tarihinde Kümülatif Ölüm Sayısı ({df["Year"].min()}-{df["Year"].max()})', 
             fontsize=14, weight='bold')

# X ekseninde her 10 yılda bir etiket göster
year_ticks = range(df['Year'].min(), df['Year'].max() + 1, 10)
ax.set_xticks(year_ticks)
ax.set_xticklabels(year_ticks, rotation=45, ha='right')

ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)


total_deaths = cumulative_fatalities.iloc[-1]
ax.axhline(y=total_deaths, color='red', linestyle='--', alpha=0.5)
ax.text(cumulative_fatalities.index[-1], total_deaths + 2000, 
        f'Toplam: {int(total_deaths):,}', fontsize=11, weight='bold', color='red')

plt.tight_layout()
plt.savefig('viz_9_area_cumulative_deaths.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_9_area_cumulative_deaths.png")
plt.close()


# GRAFİK 10: BOX PLOT - Dekatlara Göre Kaza Başına Ölüm Sayısı
print("[10/10] Box Plot: Dekatlara Göre Kaza Başına Ölüm Dağılımı")

# Son 100 yılı
recent_df = df[df['Year'] >= 1920]

fig, ax = plt.subplots(figsize=(14, 7))

box_data = [recent_df[recent_df['Decade'] == d]['Fatalities'].dropna() 
            for d in sorted(recent_df['Decade'].unique())]

bp = ax.boxplot(box_data, labels=sorted(recent_df['Decade'].unique()),
                patch_artist=True, showmeans=True, meanline=True)

# Renklendirme
colors_box = plt.cm.coolwarm(np.linspace(0, 1, len(bp['boxes'])))
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Dekat', fontsize=12, weight='bold')
ax.set_ylabel('Kaza Başına Ölüm Sayısı', fontsize=12, weight='bold')
ax.set_title(f'Dekatlara Göre Kaza Başına Ölüm Sayısı Dağılımı (1920-{df["Year"].max()})', 
             fontsize=14, weight='bold')
ax.grid(axis='y', alpha=0.3)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('viz_10_box_fatalities_by_decade.png', dpi=300, bbox_inches='tight')
print("  ✓ Kaydedildi: viz_10_box_fatalities_by_decade.png")
plt.close()


# ÖZET İSTATİSTİKLER
print("\n" + "=" * 60)
print("   ANALİZ TAMAMLANDI - ÖZET İSTATİSTİKLER")
print("=" * 60)

print(f"\n📊 Toplam Kaza Sayısı: {len(df):,}")
print(f"💀 Toplam Ölüm Sayısı: {int(df['Fatalities'].sum()):,}")
print(f"📅 Tarih Aralığı: {df['Year'].min()} - {df['Year'].max()}")
print(f"⚠️  Ölümcül Kaza Oranı (≥%50): {df['Is_Fatal'].mean()*100:.1f}%")
print(f"✈️  En Tehlikeli Operatör: {df.groupby('Operator')['Fatalities'].sum().idxmax()}")
print(f"📈 En Kötü Yıl: {df.groupby('Year')['Fatalities'].sum().idxmax()} "
      f"({int(df.groupby('Year')['Fatalities'].sum().max())} ölüm)")

print("\n✅ 10 adet görselleştirme başarıyla oluşturuldu!")
print("=" * 60)

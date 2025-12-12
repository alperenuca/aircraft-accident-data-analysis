# Havacılık Kaza Verisi Analizi | Aircraft Accident Data Analysis

[Türkçe](#türkçe) | [English](#english)

---

## Türkçe

### Proje Hakkında

Bu çalışma, 1908-2009 yılları arasında gerçekleşen 5.246 havacılık kazasının kapsamlı istatistiksel analizini ve görselleştirmesini içermektedir. Proje, havacılık güvenliği alanında tarihsel verilerin sistematik olarak incelenmesi ve çeşitli analitik yöntemlerle yorumlanması amacıyla geliştirilmiştir.

### Araştırma Kapsamı

Çalışma kapsamında, bir asrı aşkın süreçte meydana gelen havacılık kazaları; operatör kategorileri, uçak tipleri, zamansal trendler ve ölüm oranları açısından detaylı olarak incelenmiştir. Analiz sürecinde Python programlama dili ve ilgili veri bilimi kütüphaneleri kullanılarak 10 farklı görselleştirme türü üretilmiştir.

### Metodoloji

#### Veri Hazırlama

- Eksik ve hatalı kayıtların temizlenmesi
- Veri tutarlılığının sağlanması
- Kategorik değişkenlerin standardizasyonu

#### Özellik Mühendisliği

- Ölüm oranı (fatality ratio) hesaplaması
- Dekat bazlı zaman gruplandırması
- Operatör kategorilerinin (askeri/sivil) belirlenmesi

#### Sınıflandırma Kriteri

Kazalar, uçaktaki toplam kişi sayısına göre ölüm oranı ≥%50 olması durumunda "ölümcül" olarak sınıflandırılmıştır. Bu eşik değer, kaza şiddetinin objektif bir şekilde değerlendirilmesi için belirlenmiştir.

### Analiz Bulguları

#### Temel İstatistikler

- **Toplam Kaza Sayısı**: 5.246
- **Toplam Kayıp**: 105.358 kişi
- **İncelenen Dönem**: 1908-2009 (101 yıl)
- **Ölümcül Kaza Oranı**: %85
- **En Yüksek Kayıp Yaşanan Yıl**: 1972 (2.937 kişi)

#### Operatör Analizi

- En fazla kaza: Aeroflot (179 kaza, 7.156 kayıp)
- Askeri operatörler: %15 (789 kaza)
- Sivil operatörler: %85 (4.457 kaza)

#### Uçak Tipi Analizi

- En yüksek kayıp: Douglas DC-3 (4.792 kişi)
- Toplam 10 farklı uçak tipi detaylı olarak incelenmiştir

### Görselleştirme Türleri

Araştırma kapsamında üretilen 10 farklı görselleştirme türü:

1. Pasta Grafiği - Askeri/sivil kaza dağılımı
2. Yatay Çubuk Grafik - Operatör bazlı kaza sıralaması
3. Dağılım Grafiği - Kapasite-ölüm oranı ilişkisi
4. Çoklu Çizgi Grafik - Dekat bazlı trend analizi
5. Isı Haritası - Periyodik ortalama kayıp analizi
6. Violin Plot - Ölüm oranı dağılım karşılaştırması
7. Yığılmış Çubuk Grafik - Şiddet bazlı dekat analizi
8. Halka Grafik - Uçak tipi bazlı kayıp dağılımı
9. Alan Grafiği - Kümülatif kayıp trendi
10. Kutu Grafiği - Kaza başına kayıp dağılımı

### Kullanılan Teknolojiler

- **Python 3.x**: Temel programlama dili
- **pandas**: Veri manipülasyonu ve analizi
- **numpy**: Sayısal hesaplamalar
- **matplotlib**: Görselleştirme altyapısı
- **seaborn**: İstatistiksel görselleştirme

### Kurulum ve Kullanım

#### Gereksinimler

```bash
pip install -r requirements.txt
```

#### Çalıştırma

```bash
python advanced_visualizations.py
```

Program çalıştırıldığında, proje dizininde 10 adet PNG formatında görselleştirme dosyası oluşturulacaktır.

### Veri Seti

Veri seti, 1908-2009 yılları arasındaki havacılık kazalarına ilişkin aşağıdaki bilgileri içermektedir:

- Tarih, saat ve konum bilgisi
- Operatör ve uçak tipi
- Uçaktaki toplam kişi sayısı
- Kayıp sayısı
- Kaza özeti

**Kaynak**: Tarihsel havacılık kaza kayıtları

### Doğrulama

Tüm istatistiksel hesaplamalar ve bulgular, ham veri seti ile karşılaştırmalı olarak doğrulanmıştır. Veri bütünlüğü ve hesaplama doğruluğu test edilmiş, yanıltıcı bilgi içermediği teyit edilmiştir.

### Lisans

Bu proje MIT Lisansı altında açık kaynak olarak sunulmaktadır.

### Yazar

Alperen Uca

---

## English

### About the Project

This study presents a comprehensive statistical analysis and visualization of 5,246 aviation accidents that occurred between 1908 and 2009. The project was developed with the aim of systematically examining historical data in the field of aviation safety and interpreting it through various analytical methods.

### Research Scope

Within the scope of this study, aviation accidents spanning over a century have been examined in detail in terms of operator categories, aircraft types, temporal trends, and fatality ratios. During the analysis process, 10 different types of visualizations were generated using the Python programming language and related data science libraries.

### Methodology

#### Data Preparation

- Cleaning of missing and erroneous records
- Ensuring data consistency
- Standardization of categorical variables

#### Feature Engineering

- Calculation of fatality ratio
- Decade-based temporal grouping
- Determination of operator categories (military/civilian)

#### Classification Criterion

Accidents were classified as "fatal" when the fatality ratio relative to the total number of people aboard was ≥50%. This threshold value was determined for objective assessment of accident severity.

### Analysis Findings

#### Key Statistics

- **Total Number of Accidents**: 5,246
- **Total Fatalities**: 105,358 persons
- **Period Examined**: 1908-2009 (101 years)
- **Fatal Accident Rate**: 85%
- **Year with Highest Fatalities**: 1972 (2,937 persons)

#### Operator Analysis

- Highest accident count: Aeroflot (179 accidents, 7,156 fatalities)
- Military operators: 15% (789 accidents)
- Civilian operators: 85% (4,457 accidents)

#### Aircraft Type Analysis

- Highest fatalities: Douglas DC-3 (4,792 persons)
- A total of 10 different aircraft types were examined in detail

### Visualization Types

Ten different types of visualizations produced within the scope of the research:

1. Pie Chart - Military/civilian accident distribution
2. Horizontal Bar Chart - Operator-based accident ranking
3. Scatter Plot - Capacity-fatality ratio relationship
4. Multi-Line Chart - Decade-based trend analysis
5. Heatmap - Periodic average fatality analysis
6. Violin Plot - Fatality ratio distribution comparison
7. Stacked Bar Chart - Severity-based decade analysis
8. Donut Chart - Aircraft type-based fatality distribution
9. Area Chart - Cumulative fatality trend
10. Box Plot - Fatalities per accident distribution

### Technologies Used

- **Python 3.x**: Primary programming language
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Visualization infrastructure
- **seaborn**: Statistical visualization

### Installation and Usage

#### Requirements

```bash
pip install -r requirements.txt
```

#### Execution

```bash
python advanced_visualizations.py
```

When the program is executed, 10 visualization files in PNG format will be created in the project directory.

### Dataset

The dataset contains the following information regarding aviation accidents between 1908-2009:

- Date, time, and location information
- Operator and aircraft type
- Total number of people aboard
- Number of fatalities
- Accident summary

**Source**: Historical aviation accident records

### Validation

All statistical calculations and findings have been validated comparatively against the raw dataset. Data integrity and computational accuracy have been tested and confirmed to contain no misleading information.

### License

This project is provided as open source under the MIT License.

### Author

Alperen Uca

---

**Repository**: https://github.com/alperenuca/aircraft-accident-data-analysis

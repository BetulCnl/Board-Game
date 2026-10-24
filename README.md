# Lords of the Polywarphism

Pygame ile yazılmış, ızgara tabanlı, çok oyunculu bir strateji oyunu. Nesne yönelimli programlama dersi projesi; asıl amaç savaşçı türlerini kalıtım ve çok biçimlilik (polymorphism) ile modellemek.

Hatice Reyhan Çalışkan ve Betül Canol, Kocaeli Sağlık ve Teknoloji Üniversitesi, Bilgisayar Mühendisliği (Mart 2024).

## Oyun

- Tahta boyutu seçilir: 8x8, 16x16, 24x24, 32x32 ya da 8–32 arası özel bir boyut.
- 1–4 oyuncu girilir, eksik kalan yerleri botlar doldurur. Her oyuncu bir köşeden başlar.
- Her oyuncu 200 kaynakla başlar ve bir turda en fazla 2 savaşçı yerleştirebilir.
- Oyuncu bilgileri (isim, kaynak, can) ekranın köşelerinde kendi renginde gösterilir.

| Savaşçı | Maliyet | Can | Hasar | Menzil (yatay / dikey / çapraz) |
|---|---|---|---|---|
| Muhafız (Guardian) | 10 | 80 | 20 | 1 / 1 / 1 |
| Okçu (Archer) | 20 | 30 | 60 | 2 / 2 / 2 |
| Topçu (Artillery) | 50 | 30 | 100 | 2 / 2 / 0 |
| Atlı (Cavalry) | 30 | 40 | 30 | 0 / 0 / 3 |
| Sağlıkçı (Healer) | 10 | 100 | 0 (50 iyileştirir) | 2 / 2 / 2 |

Tüm savaşçılar `Warrior` sınıfından türer ve `attack_enemy` metodunu kendine göre ezer.

## Kontroller

1. Tahtada boş bir kareye tıkla (seçilen kare kırmızıyla çerçevelenir).
2. Tekrar tıkla, açılan listeden `1`–`5` tuşlarıyla savaşçıyı seç.
3. Kaynak yetiyorsa savaşçı yerleşir. Turdaki hak dolunca sıra sonraki oyuncuya geçer.

## Çalıştırma

```bash
pip install pygame
python 220501001_Hatice_Reyhan_Calskan_220501009_Betul_Canol.py
```

Dosyanın sonunda yalnızca `game = Game()` var, `game.run()` çağrılmıyor. Oyunun açılması için son satırın altına `game.run()` eklemek gerekiyor.

## Durum

Tamamlanmamış bir ödev. Savaşçıları yerleştirme ve tur sırası çalışıyor; saldırı, hasar ve kazanma koşulu oyuna bağlanmadı. "Pass" butonunun tıklama alanı tanımlı ama ekrana çizilmiyor.

## Dosyalar

- `*.py`: oyunun tamamı (tek dosya)
- `*.pdf`: proje raporu (gereksinimler, tasarım, ekran görüntüleri)

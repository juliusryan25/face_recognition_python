from package import datetime

absen_masuk_start = datetime.now().replace(hour=7, minute=30, second=0, microsecond=0)
absen_masuk_end = datetime.now().replace(hour=9, minute=23, second=0, microsecond=0)
absen_pulang_start = datetime.now().replace(hour=9, minute=23, second=30, microsecond=0)
absen_pulang_end = datetime.now().replace(hour=5, minute=59, second=0, microsecond=0)
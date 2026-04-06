import pytest
import pandas as pd
import os
import psutil
import time

@pytest.fixture
def generator_csv(tmp_path):
    """Pravi 100 CSV fajlova sa po 5.000 redova"""
    d = tmp_path / "data_9"
    d.mkdir()
    for i in range(1000):
        fajl = d / f"test_{i}.csv"
        df = pd.DataFrame({'id': range(5000), 'val': [i * 1.5] * 5000})
        df.to_csv(fajl, index=False)
    return d

def test_performance_report(generator_csv):
    proc = psutil.Process(os.getpid())
    mem_start = proc.memory_info().rss / (1024 * 1024)
    start_time = time.time()

    fajlovi = list(generator_csv.glob("*.csv"))
    ukupno_redova = 0
    
    for f in fajlovi:
        df = pd.read_csv(f)
        ukupno_redova += len(df)

    trajanje = time.time() - start_time
    mem_end = proc.memory_info().rss / (1024 * 1024)

    print(f"\n--- PAJTEST_9 IZVEŠTAJ ---")
    print(f"Obrađeno redova: {ukupno_redova}")
    print(f"Vreme: {trajanje:.3f}s")
    print(f"Dodatni RAM: {mem_end - mem_start:.2f} MB")

    assert ukupno_redova == 5000000

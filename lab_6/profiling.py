import cProfile
import pstats
from memory_profiler import profile
from line_profiler import LineProfiler
from pyheat import PyHeat
import os

# Импортируем основной модуль программы
import main

# Путь для сохранения результатов профилирования
OUTPUT_DIR = os.path.abspath("./profiling_results")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def run_with_cprofile():
    """
    Выполняет профилирование программы с использованием cProfile
    и сохраняет результаты.
    """
    profiler = cProfile.Profile()
    profiler.enable()

    # Выполняем основную функцию
    main.main()

    profiler.disable()

    # Сохраняем результаты
    stats_path = os.path.join(OUTPUT_DIR, "cprofile_output.txt")
    with open(stats_path, "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.sort_stats('cumtime').print_stats()
    print(f"cProfile results saved to {stats_path}")

def run_with_memory_profiler():
    """
    Выполняет профилирование программы с использованием memory_profiler
    и выводит построчное использование памяти.
    """
    @profile
    def profiled_main():
        main.main()

    profiled_main()

def run_with_line_profiler():
    """
    Выполняет профилирование программы с использованием line_profiler
    для построчного анализа времени выполнения.
    """
    profiler = LineProfiler()
    profiler.add_function(main.main)  # Добавляем функцию для профилирования

    profiler.enable_by_count()
    main.main()
    profiler.disable()

    # Сохраняем результаты
    stats_path = os.path.join(OUTPUT_DIR, "line_profiler_output.txt")
    with open(stats_path, "w") as f:
        profiler.print_stats(stream=f)
    print(f"LineProfiler results saved to {stats_path}")

def run_with_pyheat():
    """
    Выполняет визуализацию профилирования с использованием PyHeat
    и сохраняет тепловую карту как PNG.
    """
    heatmap_path = os.path.join(OUTPUT_DIR, "pyheat_output.png")
    ph = PyHeat(main.__file__)
    ph.create_heatmap()
    ph.show_heatmap(heatmap_path)  # Сохраняем тепловую карту в PNG
    print(f"PyHeat heatmap saved to {heatmap_path}")

def main_analysis():
    """
    Запускает все методы профилирования.
    """
    print("Running cProfile...")
    run_with_cprofile()

    print("\nRunning memory_profiler...")
    run_with_memory_profiler()

    print("\nRunning line_profiler...")
    run_with_line_profiler()

    print("\nRunning PyHeat...")
    run_with_pyheat()


if __name__ == "__main__":
    main_analysis()

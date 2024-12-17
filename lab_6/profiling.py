import cProfile
import pstats
from memory_profiler import profile
from line_profiler import LineProfiler
import os

# Импортируем основной модуль программы
import main
import optimized_code

# Путь для сохранения результатов профилирования
OUTPUT_DIR = os.path.abspath("./profiling_results")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def run_with_cprofile(file,saving_file):
    """
    Выполняет профилирование программы с использованием cProfile
    и сохраняет результаты.
    """
    profiler = cProfile.Profile()
    profiler.enable()

    # Выполняем основную функцию
    file.main()

    profiler.disable()

    # Сохраняем результаты
    stats_path = os.path.join(OUTPUT_DIR, saving_file)
    with open(stats_path, "w") as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.sort_stats('cumtime').print_stats()
    print(f"cProfile results saved to {stats_path}")

def run_with_memory_profiler(file):
    """
    Выполняет профилирование программы с использованием memory_profiler
    и выводит построчное использование памяти.
    """
    @profile
    def profiled_main():
        file.main()

    profiled_main()

def run_with_line_profiler(file,saving_file):
    """
    Выполняет профилирование программы с использованием line_profiler
    для построчного анализа времени выполнения.
    """
    profiler = LineProfiler()
    profiler.add_function(file.main)  # Добавляем функцию для профилирования
    profiler.add_function(file.frequency_bitwise_test)  # Профилируем частотный тест
    profiler.add_function(file.similar_sequences_test)  # Профилируем тест последовательностей
    profiler.add_function(file.longest_ones_sequence_test)  # Профилируем тест на длинные последовательности

    profiler.enable_by_count()
    file.main()
    profiler.disable()

    # Сохраняем результаты
    stats_path = os.path.join(OUTPUT_DIR, saving_file)
    with open(stats_path, "w") as f:
        profiler.print_stats(stream=f)
    print(f"LineProfiler results saved to {stats_path}")

def main_analysis():
    """
    Запускает все методы профилирования.
    """
    print("Running cProfile...")
    run_with_cprofile(main, "cprofile_output.txt")

    print("\nRunning memory_profiler...")
    run_with_memory_profiler(main)
    print ("Результат memory_profiler для исходного кода")

    print("\nRunning line_profiler...")
    run_with_line_profiler(main, "line_profiler_output.txt")

def optimized_code_analysis():
    """
    Запускает все методы профилирования.
    """
    print("Running cProfile...")
    run_with_cprofile(optimized_code, "cprofile_output_for_optimized_code.txt")

    print("\nRunning memory_profiler...")
    run_with_memory_profiler(optimized_code)
    print ("Результат memory_profiler для оптимизированного кода")

    print("\nRunning line_profiler...")
    run_with_line_profiler(optimized_code, "line_profiler_output_for_optimized_code.txt")

if __name__ == "__main__":
    main_analysis()
    optimized_code_analysis()

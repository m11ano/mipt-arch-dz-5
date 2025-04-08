import requests
import time
import tracemalloc
import functools

# Добавим декоратор профилировщика
def profile_memory_usage(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[PROFILE] Запуск функции: {func.__name__}")
        tracemalloc.start()
        start_time = time.time()

        result = func(*args, **kwargs)

        _, peak = tracemalloc.get_traced_memory()
        end_time = time.time()
        tracemalloc.stop()

        print(f"[PROFILE] Время выполнения: {end_time - start_time:.2f} секунд")
        print(f"[PROFILE] Пиковое использование памяти: {peak / 1024 / 1024:.2f} МБ")
        return result
    return wrapper

def get_text(url):
    response = requests.get(url)
    return response.text

# добавил замыкание для кеширования результата по url
# убрал split, всё делаем в один проход
def count_word_frequencies(url):
    cache = {}
    is_сached = False

    def counter(word):
        nonlocal is_сached 
        if is_сached == False:
            is_сached = True
            text = get_text(url)
            current_word = ""
            for ch in text:
                if ch != ' ':
                    current_word += ch
                elif current_word:
                    cache[current_word] = cache.get(current_word, 0) + 1
                    current_word = ""
            if current_word:
                cache[current_word] = cache.get(current_word, 0) + 1
        return cache.get(word, 0)
    
    return counter

@profile_memory_usage
def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    # создаем функцию для подсчета по url
    counter = count_word_frequencies(url)

    # считаем частоту сразу в один проход вместе с чтением файла
    frequencies = {}
    with open(words_file, 'r') as file:
        for line in file:
            word = line.strip()
            if word:
                frequencies[word] = counter(word)
    
    print(frequencies)

if __name__ == "__main__":
    main()
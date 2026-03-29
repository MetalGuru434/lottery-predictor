#!/usr/bin/env python3
"""
АВТОМАТИЧЕСКИЙ ПРОГНОЗ ЛОТЕРЕИ 6 ИЗ 49
С интеграцией Google Drive и генерацией 16 специальных комбинаций
"""

import json
import urllib.request
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import ast
import warnings
warnings.filterwarnings('ignore')

class LotteryPredictor:
    """
    Класс для прогнозирования лотереи с Google Drive интеграцией
    """
    
    def __init__(self, csv_path='circulation_data.csv'):
        self.csv_path = csv_path
        self.df = None
        self.online_data = None
        self.frequency_table = None
        self.mean_ranks = []
        self.scaler = StandardScaler()
        self.models = {}
        
    def load_csv_data(self):
        """Загрузка данных из CSV файла"""
        print("\n" + "="*80)
        print("ШАГ 1: ЗАГРУЗКА ДАННЫХ ИЗ CSV")
        print("="*80)
        
        try:
            self.df = pd.read_csv(self.csv_path, header=None, 
                                 names=['id', 'date', 'numbers'])
            
            # Парсим числа из строки
            self.df['numbers'] = self.df['numbers'].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            
            print(f"\n✅ Загружено из CSV: {len(self.df):,} тиражей")
            print(f"\n📊 Первый тираж:")
            print(f"   ID: {self.df.iloc[0]['id']}")
            print(f"   Дата: {self.df.iloc[0]['date']}")
            print(f"   Числа: {self.df.iloc[0]['numbers']}")
            
            print(f"\n📊 Последний тираж в CSV:")
            print(f"   ID: {self.df.iloc[-1]['id']}")
            print(f"   Дата: {self.df.iloc[-1]['date']}")
            print(f"   Числа: {self.df.iloc[-1]['numbers']}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Файл {self.csv_path} не найден")
            return False
        except Exception as e:
            print(f"❌ Ошибка чтения CSV: {e}")
            return False
    
    def load_online_data(self):
        """Загрузка последних данных онлайн"""
        print("\n" + "="*80)
        print("ШАГ 2: ЗАГРУЗКА ПОСЛЕДНИХ ДАННЫХ ОНЛАЙН")
        print("="*80)
        
        url = 'https://johannesfriedrich.github.io/LottoNumberArchive/Lottonumbers_tidy_complete.json'
        
        try:
            print(f"\n📥 Загрузка данных из: {url}")
            with urllib.request.urlopen(url, timeout=60) as response:
                self.online_data = json.loads(response.read().decode())
            
            print(f"✅ Загружено онлайн: {len(self.online_data):,} записей")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка загрузки онлайн: {e}")
            print(f"⚠️ Продолжаю с данными из CSV")
            return False
    
    def prepare_online_draws(self):
        """Подготовка тиражей из онлайн данных"""
        if not self.online_data:
            return []
        
        # Фильтруем только Lottozahl
        lotto_data = [x for x in self.online_data if x.get('variable') == 'Lottozahl']
        
        # Группируем по тиражам
        draws = {}
        for entry in lotto_data:
            draw_id = entry['id']
            if draw_id not in draws:
                draws[draw_id] = {
                    'numbers': [],
                    'date': entry.get('date', '')
                }
            draws[draw_id]['numbers'].append(entry['value'])
        
        # Фильтруем полные тиражи
        valid_draws = []
        for draw_id, draw_info in sorted(draws.items()):
            if len(draw_info['numbers']) == 6:
                valid_draws.append({
                    'id': draw_id,
                    'date': draw_info['date'],
                    'numbers': sorted(draw_info['numbers'])
                })
        
        return valid_draws
    
    def update_csv_if_needed(self):
        """Проверка и обновление CSV базы"""
        print("\n" + "="*80)
        print("ШАГ 3: ПРОВЕРКА И ОБНОВЛЕНИЕ БАЗЫ")
        print("="*80)
        
        online_draws = self.prepare_online_draws()
        
        if not online_draws:
            print("⚠️ Нет онлайн данных для обновления")
            return
        
        last_online_draw = online_draws[-1]
        last_csv_draw_id = self.df.iloc[-1]['id']
        
        print(f"\n📊 Сравнение:")
        print(f"   Последний в CSV:    ID {last_csv_draw_id}")
        print(f"   Последний онлайн:   ID {last_online_draw['id']}")
        
        if last_online_draw['id'] <= last_csv_draw_id:
            print(f"\n✅ База актуальна, обновление не требуется")
            return
        
        print(f"\n📥 Обнаружены новые тиражи: {last_online_draw['id'] - last_csv_draw_id}")
        
        # Добавляем новые тиражи
        new_rows = []
        for draw in online_draws:
            if draw['id'] > last_csv_draw_id:
                new_rows.append({
                    'id': draw['id'],
                    'date': draw['date'],
                    'numbers': draw['numbers']
                })
        
        if new_rows:
            new_df = pd.DataFrame(new_rows)
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            
            # Сохраняем обновленный CSV
            self.df.to_csv(self.csv_path, index=False, header=False)
            
            print(f"✅ Добавлено {len(new_rows)} новых тиражей")
            print(f"✅ CSV обновлен: {self.csv_path}")
            
            print(f"\n📊 Новый последний тираж:")
            print(f"   ID: {self.df.iloc[-1]['id']}")
            print(f"   Дата: {self.df.iloc[-1]['date']}")
            print(f"   Числа: {self.df.iloc[-1]['numbers']}")
    
    def calculate_frequencies(self):
        """Расчет частот появления чисел"""
        print("\n" + "="*80)
        print("ШАГ 4: РАСЧЕТ ЧАСТОТ")
        print("="*80)
        
        frequencies = {i: 0 for i in range(1, 50)}
        
        for _, row in self.df.iterrows():
            for number in row['numbers']:
                frequencies[number] += 1
        
        # Сортируем по частоте
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        # Создаем таблицу рангов
        self.frequency_table = {}
        for rank, (number, freq) in enumerate(sorted_freq, 1):
            self.frequency_table[number] = {
                'rank': rank,
                'frequency': freq
            }
        
        print(f"\n📊 Топ-10 самых частых чисел:")
        print(f"\n{'Ранг':>5} | {'Число':>6} | {'Частота':>10}")
        print("-" * 30)
        for rank, (number, freq) in enumerate(sorted_freq[:10], 1):
            print(f"{rank:>5} | {number:>6} | {freq:>10}")
        
        return self.frequency_table
    
    def calculate_mean_ranks(self):
        """Расчет средних рангов для каждого тиража"""
        print("\n" + "="*80)
        print("ШАГ 5: РАСЧЕТ СРЕДНИХ РАНГОВ")
        print("="*80)
        
        self.mean_ranks = []
        
        for _, row in self.df.iterrows():
            ranks = [self.frequency_table[num]['rank'] for num in row['numbers']]
            mean_rank = np.mean(ranks)
            self.mean_ranks.append(mean_rank)
        
        self.mean_ranks = np.array(self.mean_ranks)
        
        print(f"\n📊 Статистика средних рангов:")
        print(f"   Среднее:  {np.mean(self.mean_ranks):.4f}")
        print(f"   Медиана:  {np.median(self.mean_ranks):.4f}")
        print(f"   Ст.откл.: {np.std(self.mean_ranks):.4f}")
        print(f"   Мин:      {np.min(self.mean_ranks):.4f}")
        print(f"   Макс:     {np.max(self.mean_ranks):.4f}")
        
        return self.mean_ranks
    
    def prepare_sequences(self, lookback=10):
        """Подготовка последовательностей для обучения"""
        print("\n" + "="*80)
        print("ШАГ 6: ПОДГОТОВКА ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
        print("="*80)
        
        X, y = [], []
        
        for i in range(lookback, len(self.mean_ranks)):
            X.append(self.mean_ranks[i-lookback:i])
            y.append(self.mean_ranks[i])
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"\n✅ Подготовлено: {len(X):,} последовательностей")
        print(f"   Lookback: {lookback}")
        
        return X, y
    
    def train_models(self, X, y):
        """Обучение моделей"""
        print("\n" + "="*80)
        print("ШАГ 7: ОБУЧЕНИЕ МОДЕЛЕЙ")
        print("="*80)
        
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        # MLP
        print(f"\n🤖 Обучение нейронной сети...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        mlp = MLPRegressor(
            hidden_layer_sizes=(100, 50, 25),
            activation='relu',
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.2,
            n_iter_no_change=10
        )
        mlp.fit(X_train_scaled, y_train)
        mlp_pred = mlp.predict(X_test_scaled)
        mlp_mae = np.mean(np.abs(mlp_pred - y_test))
        
        self.models['mlp'] = mlp
        print(f"   MAE: {mlp_mae:.4f}")
        
        # Random Forest
        print(f"\n🌳 Обучение Random Forest...")
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        rf_pred = rf.predict(X_test)
        rf_mae = np.mean(np.abs(rf_pred - y_test))
        
        self.models['rf'] = rf
        print(f"   MAE: {rf_mae:.4f}")
        
        print(f"\n🏆 Модели обучены")
        
        return self.models
    
    def predict_next_draw(self, lookback=10):
        """Прогноз следующего тиража"""
        print("\n" + "="*80)
        print("ШАГ 8: ПРОГНОЗ СЛЕДУЮЩЕГО ТИРАЖА")
        print("="*80)
        
        last_sequence = self.mean_ranks[-lookback:]
        
        # Прогноз MLP
        last_sequence_scaled = self.scaler.transform(last_sequence.reshape(1, -1))
        mlp_prediction = self.models['mlp'].predict(last_sequence_scaled)[0]
        
        # Прогноз RF
        rf_prediction = self.models['rf'].predict(last_sequence.reshape(1, -1))[0]
        
        # Ансамбль
        ensemble_prediction = (mlp_prediction + rf_prediction) / 2
        
        print(f"\n🎯 ПРОГНОЗ СРЕДНЕГО РАНГА:")
        print(f"   MLP:      {mlp_prediction:.4f}")
        print(f"   RF:       {rf_prediction:.4f}")
        print(f"   АНСАМБЛЬ: {ensemble_prediction:.4f} ⭐")
        
        return ensemble_prediction
    
    def is_isolated(self, numbers):
        """Проверка что все числа изолированы (нет смежных)"""
        numbers = sorted(numbers)
        for i in range(len(numbers) - 1):
            if numbers[i+1] - numbers[i] == 1:
                return False
        return True
    
    def count_consecutive_pairs(self, numbers):
        """Подсчет пар смежных чисел"""
        numbers = sorted(numbers)
        pairs = 0
        i = 0
        while i < len(numbers) - 1:
            if numbers[i+1] - numbers[i] == 1:
                pairs += 1
                i += 2  # Пропускаем следующее число (уже в паре)
            else:
                i += 1
        return pairs
    
    def has_triplet(self, numbers):
        """Проверка наличия тройки смежных чисел"""
        numbers = sorted(numbers)
        for i in range(len(numbers) - 2):
            if numbers[i+1] - numbers[i] == 1 and numbers[i+2] - numbers[i+1] == 1:
                return True
        return False
    
    def count_even_odd(self, numbers):
        """Подсчет четных и нечетных"""
        even = sum(1 for n in numbers if n % 2 == 0)
        odd = 6 - even
        return even, odd
    
    def generate_combination(self, target_rank, isolated=True, consecutive_pairs=0, 
                           has_triplet_flag=False, even_count=3, max_attempts=10000):
        """Генерация одной комбинации с заданными условиями"""
        
        # Создаем список чисел с рангами
        numbers_pool = list(range(1, 50))
        
        for attempt in range(max_attempts):
            # Случайный выбор 6 чисел
            candidate = sorted(np.random.choice(numbers_pool, 6, replace=False))
            # Преобразуем в обычные int
            candidate = [int(x) for x in candidate]
            
            # Проверка условий
            if isolated and not self.is_isolated(candidate):
                continue
            
            if not isolated:
                # Для тройки используем consecutive_pairs=-1 как флаг
                if consecutive_pairs == -1:
                    # Проверяем наличие тройки
                    if not self.has_triplet(candidate):
                        continue
                else:
                    # Обычная проверка пар
                    actual_pairs = self.count_consecutive_pairs(candidate)
                    if actual_pairs != consecutive_pairs:
                        continue
            
            if has_triplet_flag and not self.has_triplet(candidate):
                continue
            
            even, odd = self.count_even_odd(candidate)
            if even != even_count:
                continue
            
            # Проверяем близость к целевому рангу
            actual_rank = np.mean([self.frequency_table[n]['rank'] for n in candidate])
            if abs(actual_rank - target_rank) < 3.0:  # Допустимое отклонение
                return candidate, actual_rank
        
        # Если не нашли идеальную, возвращаем лучшую
        best_candidate = None
        best_deviation = float('inf')
        
        for _ in range(1000):
            candidate = sorted(np.random.choice(numbers_pool, 6, replace=False))
            # Преобразуем в обычные int
            candidate = [int(x) for x in candidate]
            
            # Базовые условия
            if isolated and not self.is_isolated(candidate):
                continue
            
            if not isolated:
                # Для тройки используем consecutive_pairs=-1 как флаг
                if consecutive_pairs == -1:
                    if not self.has_triplet(candidate):
                        continue
                else:
                    if self.count_consecutive_pairs(candidate) != consecutive_pairs:
                        continue
            
            if has_triplet_flag and not self.has_triplet(candidate):
                continue
            
            even, odd = self.count_even_odd(candidate)
            if even != even_count:
                continue
            
            actual_rank = np.mean([self.frequency_table[n]['rank'] for n in candidate])
            deviation = abs(actual_rank - target_rank)
            
            if deviation < best_deviation:
                best_deviation = deviation
                best_candidate = candidate
        
        if best_candidate is not None:
            actual_rank = np.mean([self.frequency_table[n]['rank'] for n in best_candidate])
            return best_candidate, actual_rank
        
        return None, None
    
    def generate_16_combinations(self, target_rank):
        """Генерация 16 комбинаций по спецификации"""
        print("\n" + "="*80)
        print("ШАГ 9: ГЕНЕРАЦИЯ 16 КОМБИНАЦИЙ")
        print("="*80)
        
        print(f"\n🎯 Целевой средний ранг: {target_rank:.4f}")
        
        combinations = []
        
        # 1-4: Изолированные, 3 четных 3 нечетных
        print(f"\n📊 Генерация комбинаций 1-4: Изолированные, 3Ч 3Н...")
        for i in range(4):
            combo, rank = self.generate_combination(target_rank, isolated=True, even_count=3)
            if combo:
                combinations.append({
                    'id': i + 1,
                    'numbers': combo,
                    'rank': rank,
                    'type': 'Изолированные 3Ч/3Н'
                })
                print(f"   #{i+1}: {combo} (ранг: {rank:.2f})")
        
        # 5-6: Изолированные, 4 четных 2 нечетных
        print(f"\n📊 Генерация комбинаций 5-6: Изолированные, 4Ч 2Н...")
        for i in range(2):
            combo, rank = self.generate_combination(target_rank, isolated=True, even_count=4)
            if combo:
                combinations.append({
                    'id': i + 5,
                    'numbers': combo,
                    'rank': rank,
                    'type': 'Изолированные 4Ч/2Н'
                })
                print(f"   #{i+5}: {combo} (ранг: {rank:.2f})")
        
        # 7-8: Изолированные, 2 четных 4 нечетных
        print(f"\n📊 Генерация комбинаций 7-8: Изолированные, 2Ч 4Н...")
        for i in range(2):
            combo, rank = self.generate_combination(target_rank, isolated=True, even_count=2)
            if combo:
                combinations.append({
                    'id': i + 7,
                    'numbers': combo,
                    'rank': rank,
                    'type': 'Изолированные 2Ч/4Н'
                })
                print(f"   #{i+7}: {combo} (ранг: {rank:.2f})")
        
        # 9-10: Одна пара смежных, 3 четных 3 нечетных
        print(f"\n📊 Генерация комбинаций 9-10: 1 пара смежных, 3Ч 3Н...")
        for i in range(2):
            combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                    consecutive_pairs=1, even_count=3)
            if combo:
                combinations.append({
                    'id': i + 9,
                    'numbers': combo,
                    'rank': rank,
                    'type': '1 пара смежных 3Ч/3Н'
                })
                print(f"   #{i+9}: {combo} (ранг: {rank:.2f})")
        
        # 11: Одна пара смежных, 4 четных 2 нечетных
        print(f"\n📊 Генерация комбинации 11: 1 пара смежных, 4Ч 2Н...")
        combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                consecutive_pairs=1, even_count=4)
        if combo:
            combinations.append({
                'id': 11,
                'numbers': combo,
                'rank': rank,
                'type': '1 пара смежных 4Ч/2Н'
            })
            print(f"   #11: {combo} (ранг: {rank:.2f})")
        
        # 12: Одна пара смежных, 2 четных 4 нечетных
        print(f"\n📊 Генерация комбинации 12: 1 пара смежных, 2Ч 4Н...")
        combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                consecutive_pairs=1, even_count=2)
        if combo:
            combinations.append({
                'id': 12,
                'numbers': combo,
                'rank': rank,
                'type': '1 пара смежных 2Ч/4Н'
            })
            print(f"   #12: {combo} (ранг: {rank:.2f})")
        
        # 13: Две пары смежных, 3 четных 3 нечетных
        print(f"\n📊 Генерация комбинации 13: 2 пары смежных, 3Ч 3Н...")
        combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                consecutive_pairs=2, even_count=3)
        if combo:
            combinations.append({
                'id': 13,
                'numbers': combo,
                'rank': rank,
                'type': '2 пары смежных 3Ч/3Н'
            })
            print(f"   #13: {combo} (ранг: {rank:.2f})")
        
        # 14: Две пары смежных, 4 четных 2 нечетных
        print(f"\n📊 Генерация комбинации 14: 2 пары смежных, 4Ч 2Н...")
        combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                consecutive_pairs=2, even_count=4)
        if combo:
            combinations.append({
                'id': 14,
                'numbers': combo,
                'rank': rank,
                'type': '2 пары смежных 4Ч/2Н'
            })
            print(f"   #14: {combo} (ранг: {rank:.2f})")
        
        # 15: Две пары смежных, 2 четных 4 нечетных
        print(f"\n📊 Генерация комбинации 15: 2 пары смежных, 2Ч 4Н...")
        combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                consecutive_pairs=2, even_count=2)
        if combo:
            combinations.append({
                'id': 15,
                'numbers': combo,
                'rank': rank,
                'type': '2 пары смежных 2Ч/4Н'
            })
            print(f"   #15: {combo} (ранг: {rank:.2f})")
        
        # 16: Тройка смежных, 3 четных 3 нечетных
        print(f"\n📊 Генерация комбинации 16: Тройка смежных, 3Ч 3Н...")
        combo, rank = self.generate_combination(target_rank, isolated=False, 
                                                consecutive_pairs=-1,  # Специальный флаг для тройки
                                                has_triplet_flag=True, even_count=3,
                                                max_attempts=20000)  # Увеличиваем попытки
        if combo:
            combinations.append({
                'id': 16,
                'numbers': combo,
                'rank': rank,
                'type': 'Тройка смежных 3Ч/3Н'
            })
            print(f"   #16: {combo} (ранг: {rank:.2f})")
        else:
            print(f"   ⚠️ #16: Не удалось сгенерировать (попробуйте увеличить max_attempts)")
        
        return combinations
    
    def save_results(self, predicted_rank, combinations):
        """Сохранение результатов"""
        print("\n" + "="*80)
        print("ШАГ 10: СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
        print("="*80)
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'last_draw': {
                'id': int(self.df.iloc[-1]['id']),
                'date': self.df.iloc[-1]['date'],
                'numbers': self.df.iloc[-1]['numbers']
            },
            'predicted_rank': float(predicted_rank),
            'combinations': combinations
        }
        
        # JSON
        with open('prediction_16_combinations.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Результаты сохранены в: prediction_16_combinations.json")
        
        # CSV для удобства
        df_results = pd.DataFrame(combinations)
        df_results.to_csv('prediction_16_combinations.csv', index=False, encoding='utf-8')
        
        print(f"✅ Результаты сохранены в: prediction_16_combinations.csv")
        
        return result

def main():
    """Главная функция"""
    
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "АВТОМАТИЧЕСКИЙ ПРОГНОЗ ЛОТЕРЕИ 6 ИЗ 49".center(78) + "█")
    print("█" + "Google Drive + 16 специальных комбинаций".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    # Создаем предиктор
    predictor = LotteryPredictor('circulation_data.csv')
    
    # Шаг 1: Загрузка CSV
    if not predictor.load_csv_data():
        print("\n❌ Ошибка загрузки CSV. Завершение.")
        return
    
    # Шаг 2: Загрузка онлайн данных
    predictor.load_online_data()
    
    # Шаг 3: Обновление CSV
    predictor.update_csv_if_needed()
    
    # Шаг 4: Расчет частот
    predictor.calculate_frequencies()
    
    # Шаг 5: Расчет средних рангов
    predictor.calculate_mean_ranks()
    
    # Шаг 6: Подготовка последовательностей
    X, y = predictor.prepare_sequences(lookback=10)
    
    # Шаг 7: Обучение моделей
    predictor.train_models(X, y)
    
    # Шаг 8: Прогноз
    predicted_rank = predictor.predict_next_draw(lookback=10)
    
    # Шаг 9: Генерация 16 комбинаций
    combinations = predictor.generate_16_combinations(predicted_rank)
    
    # Шаг 10: Сохранение
    predictor.save_results(predicted_rank, combinations)
    
    # Итоговый вывод
    print("\n" + "="*80)
    print("🎯 ИТОГОВЫЙ ПРОГНОЗ")
    print("="*80)
    
    print(f"\n📅 Последний тираж: {predictor.df.iloc[-1]['id']} от {predictor.df.iloc[-1]['date']}")
    print(f"🎲 Прогнозируемый средний ранг: {predicted_rank:.4f}")
    print(f"\n📊 Сгенерировано комбинаций: {len(combinations)}")
    
    print("\n" + "="*80)
    print("✅ ПРОГНОЗ ЗАВЕРШЕН")
    print("="*80)
    
    print(f"\n💡 Файлы результатов:")
    print(f"   • prediction_16_combinations.json")
    print(f"   • prediction_16_combinations.csv")
    
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()

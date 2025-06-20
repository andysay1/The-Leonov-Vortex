import numpy as np

def calculate_vortex_vector(r, theta, p0, p1):
    """
    Реализация формулы: v(r, θ) = polar_vec(p1 · tanh(r), p0 + θ)
    Возвращает декартовы компоненты вектора (vx, vy).
    """
    magnitude = p1 * np.tanh(r)
    angle = p0 + theta
    vx = magnitude * np.cos(angle)
    vy = magnitude * np.sin(angle)
    return vx, vy

def calculate_vortex_from_xy(x, y, p0, p1, center_x=0, center_y=0):
    """Вспомогательная функция, которая работает с декартовыми координатами."""
    # Смещаем систему координат к центру вихря
    rel_x = x - center_x
    rel_y = y - center_y
    
    # Переводим в полярные
    r = np.hypot(rel_x, rel_y)
    if r < 1e-6: # Избегаем проблем в центре
        return 0.0, 0.0
    theta = np.arctan2(rel_y, rel_x)
    
    return calculate_vortex_vector(r, theta, p0, p1)

# --- ЧАСТЬ 1: ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ ---
def run_tests():
    """Запускает серию тестов для проверки свойств формулы."""
    print("--- ЗАПУСК ТЕСТОВ ---")
    
    # ... Ваши существующие тесты 1-4 остаются без изменений ...
    # Тест 1: Поведение в центре (r=0)
    vx, vy = calculate_vortex_vector(r=0, theta=0, p0=0.5, p1=1.2)
    assert vx == 0 and vy == 0, "Тест 1 ПРОВАЛЕН: Вектор в центре не нулевой!"
    print("✅ Тест 1 ПРОЙДЕН: Вектор в центре (r=0) нулевой, как и ожидалось.")

    # Тест 2: Поведение на большом расстоянии (r -> ∞)
    p1_test = 1.5
    vx, vy = calculate_vortex_vector(r=1000, theta=np.pi/4, p0=0.5, p1=p1_test)
    magnitude = np.sqrt(vx**2 + vy**2)
    assert np.isclose(magnitude, p1_test), f"Тест 2 ПРОВАЛЕН: Модуль {magnitude} не стремится к p1={p1_test}."
    print("✅ Тест 2 ПРОЙДЕН: Модуль на большом расстоянии насыщается до p1.")

    # Тест 3: Эффект p0 (идеальный вихрь)
    r_test, theta_test = 2, np.pi/6
    p0_vortex = np.pi / 2
    x, y = r_test * np.cos(theta_test), r_test * np.sin(theta_test)
    vx, vy = calculate_vortex_vector(r_test, theta_test, p0_vortex, p1=1.0)
    dot_product = x * vx + y * vy
    assert np.isclose(dot_product, 0), f"Тест 3 ПРОВАЛЕН: При p0=π/2 вектор не касательный."
    print("✅ Тест 3 ПРОЙДЕН: При p0=π/2 создается идеальный круговой вихрь.")
    
    # Тест 4: Эффект p1 (масштабирование силы)
    r_test, theta_test, p0_test = 1, np.pi, 0.5
    p1_base = 1.2
    vx1, vy1 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_base)
    vx2, vy2 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_base * 2)
    mag1 = np.sqrt(vx1**2 + vy1**2)
    mag2 = np.sqrt(vx2**2 + vy2**2)
    assert np.isclose(mag2 / mag1, 2.0), "Тест 4 ПРОВАЛЕН: Удвоение p1 не удваивает модуль."
    print("✅ Тест 4 ПРОЙДЕН: Параметр p1 корректно масштабирует силу вектора.")

    # --- НОВЫЕ ТЕСТЫ ---

    # Тест 5: Поведение при p0 = π (идеальный сток)
    # Ожидание: Вектор скорости должен быть направлен строго к центру.
    r_test, theta_test = 2.0, np.pi / 4
    p0_sink = np.pi
    vx, vy = calculate_vortex_vector(r_test, theta_test, p0_sink, p1=1.0)
    # Угол вектора скорости должен быть равен theta + π
    angle_of_velocity = np.arctan2(vy, vx)
    expected_angle = theta_test + np.pi
    # Нормализуем углы для сравнения
    assert np.isclose(np.sin(angle_of_velocity), np.sin(expected_angle)) and \
           np.isclose(np.cos(angle_of_velocity), np.cos(expected_angle)), \
           "Тест 5 ПРОВАЛЕН: При p0=π вектор не направлен к центру."
    print("✅ Тест 5 ПРОЙДЕН: При p0=π создается идеальный сток.")
    
    # Тест 6: Ротационная симметрия
    # Ожидание: Если повернуть точку, вектор скорости в ней тоже повернется.
    r_test, theta_test = 1.5, np.pi/3
    p0_test, p1_test = 0.5, 1.2
    rotation_angle = np.pi / 6 # Поворачиваем на 30 градусов
    
    vx1, vy1 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_test)
    vx2, vy2 = calculate_vortex_vector(r_test, theta_test + rotation_angle, p0_test, p1_test)
    
    # Поворачиваем первый вектор вручную
    vx1_rotated = vx1 * np.cos(rotation_angle) - vy1 * np.sin(rotation_angle)
    vy1_rotated = vx1 * np.sin(rotation_angle) + vy1 * np.cos(rotation_angle)
    
    assert np.isclose(vx1_rotated, vx2) and np.isclose(vy1_rotated, vy2), \
           "Тест 6 ПРОВАЛЕН: Формула не обладает ротационной симметрией."
    print("✅ Тест 6 ПРОЙДЕН: Формула обладает ротационной симметрией.")

    # Тест 7: Суперпозиция двух вихрей
    # Ожидание: В точке (0,0) между двумя вихрями в (-1,0) и (1,0)
    # вертикальные компоненты должны обнулиться, а горизонтальные - сложиться.
    p0, p1 = np.pi / 2, 1.0  # Два идеальных вихря
    center1_x, center1_y = -1, 0
    center2_x, center2_y = 1, 0
    
    # Вектор от первого вихря в точке (0,0)
    vx1, vy1 = calculate_vortex_from_xy(0, 0, p0, p1, center1_x, center1_y)
    # Вектор от второго вихря в точке (0,0)
    vx2, vy2 = calculate_vortex_from_xy(0, 0, p0, p1, center2_x, center2_y)
    
    # Суммарный вектор
    vx_sum, vy_sum = vx1 + vx2, vy1 + vy2
    
    # vy1 должен быть положительным (движение вверх), vy2 - отрицательным (движение вниз)
    assert np.isclose(vy_sum, 0.0), "Тест 7 ПРОВАЛЕН: Вертикальные компоненты не скомпенсировались."
    # Оба vx должны быть равны нулю
    assert np.isclose(vx_sum, 0.0), "Тест 7 ПРОВАЛЕН: Горизонтальные компоненты не равны нулю."
    print("✅ Тест 7 ПРОЙДЕН: Суперпозиция двух вихрей работает предсказуемо.")


    print("\n--- ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ! ---\n")

# --- ЧАСТЬ 2: ДЕМОНСТРАЦИЯ ---
def run_demonstration():
    # ... Ваша демонстрация остается без изменений ...
    pass # Заглушка, если вы хотите запустить только тесты

# --- Основной блок ---
if __name__ == "__main__":
    run_tests()
    # run_demonstration() # Можно закомментировать, если нужны только тесты

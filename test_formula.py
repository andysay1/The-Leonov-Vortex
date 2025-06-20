import numpy as np

# -----------------------------------------------------------------------------
#                   ОСНОВНЫЕ ФУНКЦИИ МОДЕЛИ
# -----------------------------------------------------------------------------

def calculate_vortex_vector(r, theta, p0, p1):
    """
    Реализация формулы "Вихрь Леонова": v(r, θ) = polar_vec(p1·tanh(r), p0+θ)
    Принимает полярные координаты и параметры, возвращает декартовы компоненты вектора (vx, vy).
    """
    magnitude = p1 * np.tanh(r)
    angle = p0 + theta
    vx = magnitude * np.cos(angle)
    vy = magnitude * np.sin(angle)
    return vx, vy

def calculate_vortex_from_xy(x, y, p0, p1, center_x=0, center_y=0):
    """
    Вспомогательная функция, которая работает с декартовыми координатами.
    Вычисляет вектор скорости в точке (x, y) для вихря с центром в (center_x, center_y).
    """
    # Смещаем систему координат к центру вихря
    rel_x, rel_y = x - center_x, y - center_y
    
    # Переводим в полярные координаты
    r = np.hypot(rel_x, rel_y)
    if r < 1e-9:  # Избегаем проблем в самом центре
        return 0.0, 0.0
    theta = np.arctan2(rel_y, rel_x)
    
    return calculate_vortex_vector(r, theta, p0, p1)

# -----------------------------------------------------------------------------
#        ФУНКЦИИ ДЛЯ ВЫЧИСЛЕНИЯ ДИВЕРГЕНЦИИ И РОТОРА (ВЕКТОРНЫЙ АНАЛИЗ)
# -----------------------------------------------------------------------------

def get_divergence(x, y, p0, p1, h=1e-6):
    """
    Численно вычисляет дивергенцию (∇·v) поля в точке (x, y).
    Дивергенция показывает, является ли точка источником или стоком.
    """
    # ∂vx/∂x ≈ (vx(x+h) - vx(x-h)) / (2h)
    vx_plus_h, _ = calculate_vortex_from_xy(x + h, y, p0, p1)
    vx_minus_h, _ = calculate_vortex_from_xy(x - h, y, p0, p1)
    dvx_dx = (vx_plus_h - vx_minus_h) / (2 * h)
    
    # ∂vy/∂y ≈ (vy(y+h) - vy(y-h)) / (2h)
    _, vy_plus_h = calculate_vortex_from_xy(x, y + h, p0, p1)
    _, vy_minus_h = calculate_vortex_from_xy(x, y - h, p0, p1)
    dvy_dy = (vy_plus_h - vy_minus_h) / (2 * h)
    
    return dvx_dx + dvy_dy

def get_curl_z(x, y, p0, p1, h=1e-6):
    """
    Численно вычисляет Z-компоненту ротора (∇×v) поля в точке (x, y).
    Ротор показывает "закрученность" поля.
    """
    # ∂vy/∂x ≈ (vy(x+h) - vy(x-h)) / (2h)
    _, vy_plus_h = calculate_vortex_from_xy(x + h, y, p0, p1)
    _, vy_minus_h = calculate_vortex_from_xy(x - h, y, p0, p1)
    dvy_dx = (vy_plus_h - vy_minus_h) / (2 * h)
    
    # ∂vx/∂y ≈ (vx(y+h) - vx(y-h)) / (2h)
    vx_plus_h, _ = calculate_vortex_from_xy(x, y + h, p0, p1)
    vx_minus_h, _ = calculate_vortex_from_xy(x, y - h, p0, p1)
    dvx_dy = (vx_plus_h - vx_minus_h) / (2 * h)
    
    return dvy_dx - dvx_dy

# -----------------------------------------------------------------------------
#                         ОСНОВНАЯ ТЕСТОВАЯ ФУНКЦИЯ
# -----------------------------------------------------------------------------

def run_all_tests():
    """Запускает полную серию тестов для всесторонней проверки "Вихря Леонова"."""
    print("--- ЗАПУСК ПОЛНОГО НАБОРА ТЕСТОВ ДЛЯ 'ВИХРЯ ЛЕОНОВА' ---\n")
    
    # --- БАЗОВЫЕ ТЕСТЫ ---
    print("--- Раздел 1: Базовые свойства и параметры ---")
    
    # Тест 1: Поведение в центре (r=0)
    vx, vy = calculate_vortex_vector(r=0, theta=0, p0=0.5, p1=1.2)
    assert np.isclose(vx, 0) and np.isclose(vy, 0), "Тест 1 ПРОВАЛЕН: Вектор в центре не нулевой!"
    print("✅ Тест 1 ПРОЙДЕН: Вектор в центре (r=0) нулевой.")

    # Тест 2: Поведение на большом расстоянии (r -> ∞)
    p1_test = 1.5
    vx, vy = calculate_vortex_vector(r=1000, theta=np.pi/4, p0=0.5, p1=p1_test)
    magnitude = np.hypot(vx, vy)
    assert np.isclose(magnitude, p1_test), f"Тест 2 ПРОВАЛЕН: Модуль {magnitude} не стремится к p1={p1_test}."
    print("✅ Тест 2 ПРОЙДЕН: Модуль на большом расстоянии насыщается до p1.")

    # Тест 3: Эффект p0 (идеальный вихрь)
    r_test, theta_test, p1_test = 2.0, np.pi/6, 1.0
    p0_vortex = np.pi / 2
    x, y = r_test * np.cos(theta_test), r_test * np.sin(theta_test)
    vx, vy = calculate_vortex_vector(r_test, theta_test, p0_vortex, p1_test)
    dot_product = x * vx + y * vy
    assert np.isclose(dot_product, 0), "Тест 3 ПРОВАЛЕН: При p0=π/2 вектор не касательный."
    print("✅ Тест 3 ПРОЙДЕН: При p0=π/2 создается идеальный круговой вихрь.")
    
    # Тест 4: Эффект p1 (масштабирование силы)
    r_test, theta_test, p0_test = 1.0, np.pi, 0.5
    p1_base = 1.2
    vx1, vy1 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_base)
    vx2, vy2 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_base * 2)
    mag1, mag2 = np.hypot(vx1, vy1), np.hypot(vx2, vy2)
    assert np.isclose(mag2 / mag1, 2.0), "Тест 4 ПРОВАЛЕН: Удвоение p1 не удваивает модуль."
    print("✅ Тест 4 ПРОЙДЕН: Параметр p1 корректно масштабирует силу вектора.")

    # --- ТЕСТЫ СИММЕТРИИ И СУПЕРПОЗИЦИИ ---
    print("\n--- Раздел 2: Симметрия и взаимодействие ---")

    # Тест 5: Поведение при p0 = π (идеальный сток)
    r_test, theta_test, p1_test = 2.0, np.pi / 4, 1.0
    p0_sink = np.pi
    vx, vy = calculate_vortex_vector(r_test, theta_test, p0_sink, p1_test)
    angle_of_velocity = np.arctan2(vy, vx)
    expected_angle = (theta_test + np.pi) % (2 * np.pi)
    # Нормализуем углы для корректного сравнения
    angle_of_velocity = (angle_of_velocity + 2 * np.pi) % (2 * np.pi)
    assert np.isclose(angle_of_velocity, expected_angle), "Тест 5 ПРОВАЛЕН: При p0=π вектор не направлен к центру."
    print("✅ Тест 5 ПРОЙДЕН: При p0=π создается идеальный сток.")
    
    # Тест 6: Ротационная симметрия
    r_test, theta_test, p0_test, p1_test = 1.5, np.pi/3, 0.5, 1.2
    rotation_angle = np.pi / 6
    vx1, vy1 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_test)
    vx2, vy2 = calculate_vortex_vector(r_test, theta_test + rotation_angle, p0_test, p1_test)
    vx1_rotated = vx1 * np.cos(rotation_angle) - vy1 * np.sin(rotation_angle)
    vy1_rotated = vx1 * np.sin(rotation_angle) + vy1 * np.cos(rotation_angle)
    assert np.isclose(vx1_rotated, vx2) and np.isclose(vy1_rotated, vy2), "Тест 6 ПРОВАЛЕН: Формула не обладает ротационной симметрией."
    print("✅ Тест 6 ПРОЙДЕН: Формула обладает ротационной симметрией.")

    # Тест 7: Суперпозиция двух вихрей
    p0, p1 = np.pi / 2, 1.0
    vx1, vy1 = calculate_vortex_from_xy(0, 0, p0, p1, center_x=-1)
    vx2, vy2 = calculate_vortex_from_xy(0, 0, p0, p1, center_x=1)
    vx_sum, vy_sum = vx1 + vx2, vy1 + vy2
    assert np.isclose(vy_sum, 0.0), "Тест 7 ПРОВАЛЕН: Вертикальные компоненты не скомпенсировались."
    assert np.isclose(vx_sum, 0.0), "Тест 7 ПРОВАЛЕН: Горизонтальные компоненты не равны нулю."
    print("✅ Тест 7 ПРОЙДЕН: Суперпозиция двух вихрей работает предсказуемо.")

    # --- ФУНДАМЕНТАЛЬНЫЕ ФИЗИЧЕСКИЕ ТЕСТЫ ---
    print("\n--- Раздел 3: Фундаментальные свойства (Векторный анализ) ---")

    # Тест 8: Идеальный вихрь (p0=π/2) должен быть несжимаемым (div ≈ 0)
    div = get_divergence(x=1.5, y=1.0, p0=np.pi / 2, p1=1.0)
    assert np.isclose(div, 0, atol=1e-5), f"Тест 8 ПРОВАЛЕН: Идеальный вихрь сжимаем, div = {div}"
    print("✅ Тест 8 ПРОЙДЕН: Идеальный вихрь (p0=π/2) несжимаем (поле соленоидальное).")
    
    # Тест 9: Чистый источник (p0=0) должен быть безвихревым (curl ≈ 0)
    curl = get_curl_z(x=1.5, y=1.0, p0=0, p1=1.0)
    assert np.isclose(curl, 0, atol=1e-5), f"Тест 9 ПРОВАЛЕН: Чистый источник имеет закрученность, curl = {curl}"
    print("✅ Тест 9 ПРОЙДЕН: Чистый источник (p0=0) безвихревой (поле потенциальное).")

    # Тест 10: Спиральный вихрь (p0=0.5) должен быть и сжимаемым, и вихревым
    div = get_divergence(x=1.5, y=1.0, p0=0.5, p1=1.0)
    curl = get_curl_z(x=1.5, y=1.0, p0=0.5, p1=1.0)
    assert not np.isclose(div, 0, atol=1e-5), f"Тест 10 ПРОВАЛЕН: Спиральный вихрь несжимаем, div = {div}"
    assert not np.isclose(curl, 0, atol=1e-5), f"Тест 10 ПРОВАЛЕН: Спиральный вихрь безвихревой, curl = {curl}"
    print("✅ Тест 10 ПРОЙДЕН: Спиральный вихрь является и сжимаемым, и вихревым.")
    
    print("\n\n--- 📜 ВЕРДИКТ: ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ! 📜 ---\n")
    print("Модель 'Вихрь Леонова' демонстрирует математическую состоятельность и физическую адекватность.")


# --- Основной блок для запуска тестов ---
if __name__ == "__main__":
    run_all_tests()

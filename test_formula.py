import numpy as np

def calculate_vortex_vector(r, theta, p0, p1):
    """
    Реализация формулы: v(r, θ) = polar_vec(p1 · tanh(r), p0 + θ)
    Возвращает декартовы компоненты вектора (vx, vy).
    """
    # Вычисляем компоненты полярного вектора
    magnitude = p1 * np.tanh(r)
    angle = p0 + theta
    
    # Переводим в декартовы компоненты
    vx = magnitude * np.cos(angle)
    vy = magnitude * np.sin(angle)
    
    return vx, vy

# --- ЧАСТЬ 1: ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ ---
def run_tests():
    """Запускает серию тестов для проверки свойств формулы."""
    print("--- ЗАПУСК ТЕСТОВ ---")
    
    # Тест 1: Поведение в центре (r=0)
    # Ожидание: Вектор должен быть нулевым, так как tanh(0) = 0.
    vx, vy = calculate_vortex_vector(r=0, theta=0, p0=0.5, p1=1.2)
    assert vx == 0 and vy == 0, "Тест 1 ПРОВАЛЕН: Вектор в центре не нулевой!"
    print("✅ Тест 1 ПРОЙДЕН: Вектор в центре (r=0) нулевой, как и ожидалось.")

    # Тест 2: Поведение на большом расстоянии (r -> ∞)
    # Ожидание: Модуль вектора должен стремиться к p1, так как tanh(r) -> 1.
    p1_test = 1.5
    vx, vy = calculate_vortex_vector(r=1000, theta=np.pi/4, p0=0.5, p1=p1_test)
    magnitude = np.sqrt(vx**2 + vy**2)
    assert np.isclose(magnitude, p1_test), f"Тест 2 ПРОВАЛЕН: Модуль {magnitude} не стремится к p1={p1_test}."
    print("✅ Тест 2 ПРОЙДЕН: Модуль на большом расстоянии насыщается до p1.")

    # Тест 3: Эффект p0 (скручивание)
    # Ожидание: при p0 = π/2, вектор должен быть строго касательным (перпендикулярным радиус-вектору).
    # Скалярное произведение радиус-вектора и вектора скорости должно быть равно 0.
    r_test, theta_test = 2, np.pi/6
    p0_vortex = np.pi / 2
    # Координаты точки
    x = r_test * np.cos(theta_test)
    y = r_test * np.sin(theta_test)
    # Компоненты вектора скорости в этой точке
    vx, vy = calculate_vortex_vector(r=r_test, theta=theta_test, p0=p0_vortex, p1=1.0)
    dot_product = x * vx + y * vy
    assert np.isclose(dot_product, 0), f"Тест 3 ПРОВАЛЕН: При p0=π/2 вектор не касательный (скалярное произведение = {dot_product})."
    print("✅ Тест 3 ПРОЙДЕН: При p0=π/2 создается идеальный круговой вихрь.")
    
    # Тест 4: Эффект p1 (масштабирование силы)
    # Ожидание: Удвоение p1 должно удвоить модуль вектора.
    r_test, theta_test, p0_test = 1, np.pi, 0.5
    p1_base = 1.2
    vx1, vy1 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_base)
    vx2, vy2 = calculate_vortex_vector(r_test, theta_test, p0_test, p1_base * 2)
    mag1 = np.sqrt(vx1**2 + vy1**2)
    mag2 = np.sqrt(vx2**2 + vy2**2)
    assert np.isclose(mag2 / mag1, 2.0), "Тест 4 ПРОВАЛЕН: Удвоение p1 не удваивает модуль."
    print("✅ Тест 4 ПРОЙДЕН: Параметр p1 корректно масштабирует силу (модуль) вектора.")
    
    print("\n--- ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ! ---\n")

# --- ЧАСТЬ 2: ДЕМОНСТРАЦИЯ ---
def run_demonstration():
    """Демонстрирует результаты для разных параметров."""
    print("--- ДЕМОНСТРАЦИЯ РЕЗУЛЬТАТОВ ---\n")
    
    p0 = 0.5
    p1 = 1.2
    print(f"Базовые параметры: p0 = {p0}, p1 = {p1}\n")
    
    # Пример 1: Точка близко к центру
    r, theta_deg = 0.5, 45
    theta_rad = np.deg2rad(theta_deg)
    vx, vy = calculate_vortex_vector(r, theta_rad, p0, p1)
    mag = np.sqrt(vx**2 + vy**2)
    print(f"Точка 1 (близко к центру): r={r}, θ={theta_deg}°")
    print(f"  -> Вектор (vx, vy) = ({vx:.3f}, {vy:.3f})")
    print(f"  -> Модуль = {mag:.3f}\n")
    
    # Пример 2: Точка далеко от центра
    r, theta_deg = 5.0, 45
    theta_rad = np.deg2rad(theta_deg)
    vx, vy = calculate_vortex_vector(r, theta_rad, p0, p1)
    mag = np.sqrt(vx**2 + vy**2)
    print(f"Точка 2 (далеко от центра): r={r}, θ={theta_deg}°")
    print(f"  -> Вектор (vx, vy) = ({vx:.3f}, {vy:.3f})")
    print(f"  -> Модуль = {mag:.3f} (почти равен p1={p1})\n")
    
    # Пример 3: Изменение p0 на π/2 (идеальный вихрь)
    p0_vortex = np.pi / 2
    r, theta_deg = 2.0, 90
    theta_rad = np.deg2rad(theta_deg)
    vx, vy = calculate_vortex_vector(r, theta_rad, p0_vortex, p1)
    print(f"Точка 3 (идеальный вихрь): r={r}, θ={theta_deg}°, p0={p0_vortex:.3f}")
    print(f"  -> Положение точки (x,y) = (0.000, 2.000)")
    print(f"  -> Вектор (vx, vy) = ({vx:.3f}, {vy:.3f}) (направлен строго по горизонтали)\n")

# --- Основной блок ---
if __name__ == "__main__":
    run_tests()
    run_demonstration()

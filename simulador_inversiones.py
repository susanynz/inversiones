# Definir las tasas de interés según el rango de monto y plazo
interest_rates = {
    (20000, 50000): {3: 0.05, 6: 0.06, 12: 0.07, 18: 0.08, 24: 0.09},  # Monto entre 20,000 y 50,000
    (50001, 100000): {3: 0.06, 6: 0.07, 12: 0.09, 18: 0.10, 24: 0.11},  # Monto entre 50,001 y 100,000
    (100001, 250000): {3: 0.07, 6: 0.08, 12: 0.10, 18: 0.11, 24: 0.13},  # Monto entre 100,001 y 250,000
    (250001, float('inf')): {3: 0.08, 6: 0.09, 12: 0.11, 18: 0.13, 24: 0.15},  # Monto mayor a 250,000
}

def calculate_investment_return(amount: float, months: int, additional_contribution: float = 0, compound: bool = False) -> float:
    """
    Calcula el rendimiento de una inversión considerando tasas anualizadas,
    con opción a reinversión automática y posibilidad de extender la inversión por un segundo año con beneficios.

    Args:
        amount (float): Monto de inversión inicial.
        months (int): Plazo en meses (3, 6, 12, 18, 24).
        additional_contribution (float): Aportación adicional que se sumará al monto de la inversión en cada ciclo de reinversión.
        compound (bool): Indica si se reinvierte automáticamente los rendimientos.

    Returns:
        float: Monto final después de aplicar el rendimiento.
    """
    # Encontrar el rango de tasas de interés correspondiente al monto
    applicable_rate = None
    for (lower_bound, upper_bound), rates in interest_rates.items():
        if lower_bound <= amount <= upper_bound:
            applicable_rate = rates.get(months if not compound else 3)  # Usar 3 meses para reinversión
            break

    if applicable_rate is None:
        print("No hay una tasa de interés disponible para el plazo ingresado.")
        return None

    print(f"\nMonto de inversión: ${amount:,.2f}")
    print(f"Plazo seleccionado: {months} meses")
    print(f"Tasa de interés otorgada: {applicable_rate * 100:.2f}% anualizada")

    initial_amount = amount
    total_cycles = 12 // months if compound else 1  # Ciclos dentro del primer año
    rate_increment = 0  # Para el segundo año

    # Calcular rendimiento del primer año
    for cycle in range(total_cycles):
        adjusted_rate = (1 + applicable_rate) ** (months / 12) - 1
        interest_earned = amount * adjusted_rate
        amount += interest_earned + additional_contribution
        print(f"Ciclo {cycle + 1}: Monto acumulado: ${amount:,.2f}")

    print(f"\nReinversión completa del primer año. Monto acumulado: ${amount:,.2f}")

    # Preguntar si desea extender la inversión por un segundo año
    extend_question = "¿Desea extender la inversión por un segundo año con un incremento en la tasa? [sí/no]: "
    if input(extend_question).strip().lower() == "sí":
        rate_increment = 0.01  # Incrementar la tasa en 1%
        applicable_rate += rate_increment

        # Preguntar si desea incrementar el monto inicial
        additional_contribution_year2 = float(input("Ingrese la cantidad adicional para el segundo año (si no desea, ingrese 0): "))
        amount += additional_contribution_year2

        # Calcular rendimiento del segundo año (12 meses con la nueva tasa)
        adjusted_rate = (1 + applicable_rate) ** (12 / 12) - 1
        interest_earned_year2 = amount * adjusted_rate
        amount += interest_earned_year2

        print(f"\nInversión extendida al segundo año:")
        print(f"Tasa de interés anualizada: {(applicable_rate - rate_increment) * 100:.2f}% incrementada a {applicable_rate * 100:.2f}%")
        print(f"Monto inicial en el segundo año (incluyendo aportaciones adicionales): ${amount - interest_earned_year2:,.2f}")
        print(f"Interés ganado en el segundo año: ${interest_earned_year2:,.2f}")
        print(f"Monto final después del segundo año: ${amount:,.2f}")

    return amount


# Ejemplo de uso
try:
    # Pedir al usuario que ingrese el monto de la inversión, el plazo en meses
    amount = float(input("Ingrese el monto de inversión: "))
    months = int(input("Ingrese el plazo en meses (3, 6, 12, 18, 24): "))
    compound_question = (
        "¿Desea reinvertir automáticamente los rendimientos durante el primer año? [sí/no]: "
    )
    compound = input(compound_question).strip().lower() == "sí"

    # Si el usuario desea reinvertir, preguntamos si desea aumentar la inversión con aportaciones adicionales
    additional_contribution = 0
    if compound:
        increase_question = (
            "¿Desea incrementar su monto de inversión con aportaciones adicionales durante la reinversión? [sí/no]: "
        )
        additional_contribution_enabled = input(increase_question).strip().lower() == "sí"
        if additional_contribution_enabled:
            additional_contribution = float(input("Ingrese la cantidad adicional a invertir en cada reinversión: "))

    # Validar el plazo
    if months not in [3, 6, 12, 18, 24]:
        print("Plazo no válido. Ingrese uno de los siguientes plazos: 3, 6, 12, 18, 24 meses.")
    elif compound and months not in [3, 6]:
        print("La opción de reinversión automática solo está disponible para plazos de 3 o 6 meses.")
    else:
        calculate_investment_return(amount, months, additional_contribution, compound)
except ValueError:
    print("Por favor, ingrese valores numéricos válidos para el monto, plazo y aportación adicional.") 

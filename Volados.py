import streamlit as st
import numpy as np
import pandas as pd

#Menu de opciones
st.image("banner.png", use_container_width=True)
st.write("Bienvenido a la calculadora para resolver problemas de volados, para continuar seleccione una de las siguientes calculadoras:")
selected = st.radio("Seleccione una calculadora:", 
            ["Calculadora para volados con números aleatorios generados", 
            "Calculadora para volados por número de corridas"])

# Contenido basado en la selección del menú
if selected == "Calculadora para volados con números aleatorios generados":
    st.title("Calculadora para volados por cantidad de números aleatorios")
    st.write("Calculadora para resolver problemas de volados con un número limitado de números aleatorios")

    # Inputs para cantidad inicial, meta, apuesta inicial
    cantidad_inicial = st.number_input("Ingrese la cantidad de dinero inicial:", min_value=1, value=50)
    meta = st.number_input("Ingrese la meta deseada:", min_value=cantidad_inicial + 1, value=80)
    apuesta_inicial = st.number_input("Ingrese la cantidad de la apuesta inicial:", min_value=1, value=10)
    st.markdown(
        '<p style="font-size: 12px; font-style: italic;">(Si se pierde el volado, la apuesta se duplica; si se gana, vuelve a su valor inicial).</p>',
        unsafe_allow_html=True
    )

    #Función para simular volados basados los números aleatorios
    def simular_volados(cantidad_numeros):
        numeros_aleatorios = np.random.rand(cantidad_numeros)
        resultados = []
        corrida = 1
        indice_numero = 0

        while indice_numero < cantidad_numeros:  # Continuar mientras haya números aleatorios
            cantidad = cantidad_inicial
            apuesta = apuesta_inicial
            corrida_incompleta = True  # Indica si la corrida fue completa o no
            
            while cantidad > 0 and cantidad < meta:
                if indice_numero >= cantidad_numeros:
                    # Si no hay más números aleatorios, la corrida queda incompleta
                    corrida_incompleta = True
                    break

                numero_aleatorio = numeros_aleatorios[indice_numero]
                indice_numero += 1 
                se_gano_volado = numero_aleatorio <= 0.5

                cantidad_antes = cantidad

                # Si la apuesta es mayor a la cantidad disponible, se apuesta todo
                if apuesta > cantidad:
                    apuesta = cantidad

                if se_gano_volado:  # Gana y se reinicia la apuesta
                    cantidad += apuesta
                    resultado = "Sí"
                    apuesta = apuesta_inicial
                else:  # Pierde y se duplica la apuesta
                    cantidad -= apuesta
                    resultado = "No"
                    apuesta *= 2

                resultado_final = "-"
                if cantidad >= meta:
                    resultado_final = "Meta"
                    corrida_incompleta = False
                elif cantidad <= 0:
                    resultado_final = "Quiebra"
                    corrida_incompleta = False

                resultados.append({
                    "No. Corrida": corrida,
                    "Cant. antes": cantidad_antes,
                    "Apuesta": apuesta,
                    "Número aleatorio": numero_aleatorio,
                    "¿Se ganó?": resultado,
                    "Cant. después": cantidad,
                    "Resultado": resultado_final,
                    "Estado": "Completa" if not corrida_incompleta else "Incompleta"
                })

                if not corrida_incompleta:
                    break  # Salir si la corrida terminó en meta o quiebra

            corrida += 1  # Incrementar el contador de corridas incluso si es incompleta

        return pd.DataFrame(resultados)

    # Función para calcular probabilidades
    def probabilidades(total_corridas, meta_alcanzada, quiebra):
        prob_meta = (meta_alcanzada / total_corridas) * 100 if total_corridas > 0 else 0
        prob_quie = (quiebra / total_corridas) * 100 if total_corridas > 0 else 0
        return prob_meta, prob_quie

    # Input para la cantidad de números aleatorios a generar
    cantidad_numeros = st.number_input("Ingrese la cantidad de números aleatorios a generar:", min_value=1, value=100)

    if st.button("Simular"):
        df_resultados = simular_volados(cantidad_numeros)
        st.write(f"Simulación con una cantidad inicial de {cantidad_inicial}, una meta de {meta}, y una apuesta inicial de {apuesta_inicial}. Si se pierde el volado, la apuesta se duplica; si se gana, vuelve a su valor inicial.")
        
        st.write("Resultados de todas las corridas (completas e incompletas):")
        st.dataframe(df_resultados, use_container_width=True)

        # Contar cuántas veces se llegó a la meta y cuántas veces a la quiebra en corridas completas
        meta_alcanzada = df_resultados[(df_resultados["Resultado"] == "Meta") & (df_resultados["Estado"] == "Completa")].shape[0]
        quiebra = df_resultados[(df_resultados["Resultado"] == "Quiebra") & (df_resultados["Estado"] == "Completa")].shape[0]
        total_corridas_completas = df_resultados[df_resultados["Estado"] == "Completa"]["No. Corrida"].nunique()

        # Calcular probabilidades solo para corridas completas
        prob_meta, prob_quie = probabilidades(total_corridas_completas, meta_alcanzada, quiebra)
        
        st.success(f"Probabilidad de alcanzar la meta (en corridas completas): {prob_meta:.2f}% (alcanzada {meta_alcanzada} veces)")
        st.warning(f"Probabilidad de llegar a la quiebra (en corridas completas): {prob_quie:.2f}% (llegada {quiebra} veces)")

elif selected == "Calculadora para volados por número de corridas":
    st.title("Bienvenido a la calculadora para volados por número de corridas")
    st.write("Esta es una calculadora para resolver los problemas de volados usando un número de corridas a simular")
    
    # Inputs para cantidad inicial, meta, apuesta inicial
    cantidad_inicial = st.number_input("Ingrese la cantidad de dinero inicial:", min_value=1, value=50)
    meta = st.number_input("Ingrese la meta deseada:", min_value=cantidad_inicial + 1, value=80)
    apuesta_inicial = st.number_input("Ingrese la cantidad de la apuesta inicial:", min_value=1, value=10)
    
    st.markdown(
        '<p style="font-size: 12px; font-style: italic;">(Una vez se pierde el volado la apuesta aumenta el doble y regresa a su valor inicial cuando se gana).</p>',
        unsafe_allow_html=True
    )

    # Función para simular volados
    def simular_volados(num_corridas, cantidad_inicial, meta, apuesta_inicial):
        resultados = []
        progress_bar = st.progress(0)  # Barra de progreso
    
        for corrida in range(1, num_corridas + 1):
            cantidad = cantidad_inicial
            apuesta = apuesta_inicial
            while cantidad > 0 and cantidad < meta:
                numero_aleatorio = np.random.rand()  # Genera un número aleatorio entre 0 y 1
                se_gano_volado = numero_aleatorio <= 0.5

                cantidad_antes = cantidad

                # Si la apuesta es mayor a la cantidad disponible se apuesta todo
                if apuesta > cantidad:
                    apuesta = cantidad 

                if se_gano_volado:  # Gana y se reinicia la apuesta
                    cantidad += apuesta
                    resultado = "Sí"
                    apuesta = apuesta_inicial
                else:  # Pierde y se duplica la apuesta
                    cantidad -= apuesta
                    resultado = "No"
                    apuesta *= 2 

                resultado_final = "-"
                if cantidad >= meta:
                    resultado_final = "Meta"
                elif cantidad <= 0:
                    resultado_final = "Quiebra"

                resultados.append({
                    "No. Corrida": corrida,
                    "Cant. antes": cantidad_antes,
                    "Apuesta": apuesta,
                    "Número aleatorio": numero_aleatorio,
                    "¿Se ganó?": resultado,
                    "Cant. después": cantidad,
                    "Resultado": resultado_final
                })
            # Actualizar barra de progreso
            progress_bar.progress(corrida / num_corridas)
        
        return pd.DataFrame(resultados)

    # Función para calcular probabilidades
    def probabilidades(num_corridas, meta_alcanzada, quiebra):
        # Inicializar las probabilidades
        prob_meta = 0
        prob_quie = 0

        # Calcular la probabilidad de alcanzar la meta
        if num_corridas > 0:  # Evitar división por cero
            prob_meta = (meta_alcanzada / num_corridas) * 100
            prob_quie = (quiebra / num_corridas) * 100

        return prob_meta, prob_quie

    # Input para número de corridas
    num_corridas = st.number_input("Ingrese el número de corridas a simular:", min_value=1, value=100)

    if st.button("Simular"):
        df_resultados = simular_volados(num_corridas, cantidad_inicial, meta, apuesta_inicial)
        st.write(f"En base a los datos anteriores se tiene una cantidad inicial de dinero de {cantidad_inicial} y se quiere llegar a una meta de ${meta} con una apuesta inicial de {apuesta_inicial}. Si se pierde, se duplica la apuesta y así sucesivamente. Se gana el volado cuando el número aleatorio es menor o igual a 0.5 y se pierde cuando es mayor.")
        
        st.markdown(
            '<p style="font-size: 16px; font-style: italic;">¿Cuál es la probabilidad de llegar a la meta? ¿Cuál es la probabilidad de llegar a la quiebra? ¿Cuántas veces se llegó a la meta? ¿Cuántas veces se llegó a la quiebra?</p>',
            unsafe_allow_html=True
        )
        
        st.write("Resultados de las Simulaciones:")
        st.dataframe(df_resultados, use_container_width=True)

        meta_alcanzada = df_resultados[df_resultados["Resultado"] == "Meta"].shape[0]
        quiebra = df_resultados[df_resultados["Resultado"] == "Quiebra"].shape[0]

        # Calcular probabilidades
        prob_meta, prob_quie = probabilidades(num_corridas, meta_alcanzada, quiebra)
        st.success(f"Probabilidad de alcanzar la meta: {prob_meta:.2f}% dado que se alcanzó la meta {meta_alcanzada} veces")
        st.warning(f"Probabilidad de llegar a la quiebra: {prob_quie:.2f}% dado que se llegó a la quiebra {quiebra} veces")

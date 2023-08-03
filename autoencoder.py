import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import wntr

# Create a water network model
inp_file = "./Networks/Djurdevik.inp"
wn = wntr.network.WaterNetworkModel(inp_file)
# Definir los parámetros del autoencoder
input_dim = 30  # Número de características de entrada
hidden_dim = 15  # Número de neuronas en la capa oculta
output_dim = input_dim  # La salida del autoencoder tiene la misma dimensión que la entrada

# Crear el modelo del autoencoder
inputs = tf.keras.Input(shape=(input_dim,))
encoder = tf.keras.layers.Dense(hidden_dim, activation=tf.nn.relu)(inputs)
decoder = tf.keras.layers.Dense(output_dim, activation=None)(encoder)
autoencoder = tf.keras.Model(inputs=inputs, outputs=decoder)

# Compilar el modelo
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el autoencoder
num_iterations = 100
batch_size = 32
loss_history = []

Batch_data = np.zeros((batch_size,num_iterations))

for iteration in range(num_iterations):

    # Simulate hydraulics
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    # Plot results on the network
    pressure_at_5hr = results.node['pressure'].loc[5*3600, :]
    np.zeros(())

    # Generar un lote de datos de entrenamiento (aquí debes proporcionar tus propios datos)
    batch_data = np.random.rand(batch_size, input_dim)

    # Ejecutar una iteración de entrenamiento
    loss = autoencoder.train_on_batch(batch_data, batch_data)
    loss_history.append(loss)

    # Visualizar los datos de entrada y salida cada 10 iteraciones
    if (iteration + 1) % 10 == 0:
        reconstructed_data = autoencoder.predict(batch_data)

        # Elegir una muestra aleatoria del lote
        sample_index = np.random.randint(batch_size)

        # Obtener los datos de entrada y salida reconstruidos
        input_sample = batch_data[sample_index]
        output_sample = reconstructed_data[sample_index]

        # Visualizar los datos de entrada y salida
        plt.figure()
        plt.plot(input_sample, label='Input')
        plt.plot(output_sample, label='Output')
        plt.legend()
        plt.title(f"Iteration {iteration+1}/{num_iterations}")
        plt.show()

# Visualizar la curva de pérdida
plt.figure()
plt.plot(loss_history)
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
import os


class QNet:
    def __init__(self, input_shape, num_actions, load=False):
        inputs = layers.Input(shape=input_shape)
        layer1 = layers.Conv2D(128, 8, strides=4, activation='relu')(inputs)
        layer2 = layers.Conv2D(64, 4, strides=2, activation='relu')(layer1)
        layer3 = layers.Conv2D(64, 3, strides=1, activation='relu')(layer2)
        layer4 = layers.Flatten()(layer3)
        layer5 = layers.Dense(512, activation='relu')(layer4)
        layer6 = layers.Dense(128, activation='relu')(layer5)
        action = layers.Dense(num_actions, activation='linear')(layer6)
        
        self.model = tf.keras.Model(inputs=inputs, outputs=action)
        self.model.summary()
        if load:
            self.model = keras.models.load_model("model")
        
    def predict(self, state):
         # Take best action
         action_probs = self.model(state, training=False)
         #print('probs_shape: ' + str(action_probs))
         return action_probs
    
    def save(self, file_name):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        self.model.save(model_folder_path)
        
        
class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = Adam(learning_rate=self.lr)
        self.loss_function = tf.keras.losses.Huber()
    
    
    # TODO: introduce target and live network
    def train_step(self, state, action, reward, next_state, done):
        
        with tf.GradientTape() as tape:
        
            state = np.asarray(state)
        
            #1 Current Q
            pred = self.model.predict(state)
        
            #2 Q_new = r + y*max(next_predicted Q value)
            target = np.array(pred, copy=True)
            for idx in range(len(done)):
                Q_new = reward[idx]
                if not done[idx]:
                    Q_new = reward[idx] + self.gamma*np.max(self.model.predict(tf.expand_dims(next_state[idx], 0)))
        
                target[idx][np.argmax(action[idx])] = Q_new
        
        
            loss = self.loss_function(target, pred)
            tape.watch(self.model.model.trainable_variables)
            grads = tape.gradient(loss, self.model.model.trainable_variables)
            print(loss)
            self.optimizer.apply_gradients(zip(grads, self.model.model.trainable_variables))
        
        
        
    
if __name__ == "__main__":
    
    net = QNet((128, 128, 2), 4 )
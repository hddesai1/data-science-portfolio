# script for training a CNN classifier 

from config import PROCESSED_IMAGES_DIR, MODELS_DIR
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from dagshub import dagshub_logger
import os
import mlflow
import dagshub
from src.get_or_create_mlflow_experiment import get_experiment_id

def load_data_splits(validation_ratio=0.2, target_img_size=64, batch_size=32):
    """
    Train/validation_data/test_data split based on this SO answer:
    https://stackoverflow.com/questions/42443936/keras-split-training_data-test_data-set-when-using-imagedatagenerator
    """
    train_generator = ImageDataGenerator(rescale = 1./255,
                                       zoom_range=[0.5, 1.5],
                                       validation_split=validation_ratio)

    val_generator = ImageDataGenerator(rescale=1./255, 
                                       validation_split=validation_ratio)

    test_generator = ImageDataGenerator(rescale = 1./255)

    train_loader = train_generator.flow_from_directory(f"{PROCESSED_IMAGES_DIR}/training_data",
                                                     target_size = (target_img_size, target_img_size),
                                                     color_mode="grayscale",
                                                     batch_size = batch_size,
                                                     class_mode = "binary",
                                                     shuffle=True,
                                                     subset="training")

    val_loader = val_generator.flow_from_directory(f"{PROCESSED_IMAGES_DIR}/training_data",
                                                  target_size = (target_img_size, target_img_size),
                                                  color_mode="grayscale",
                                                  batch_size = batch_size,
                                                  class_mode = "binary",
                                                  shuffle=False,
                                                  subset="validation")

    test_loader = test_generator.flow_from_directory(f"{PROCESSED_IMAGES_DIR}/test_data",
                                                target_size = (target_img_size, target_img_size),
                                                color_mode="grayscale",
                                                batch_size = batch_size,
                                                class_mode = "binary")

    return train_loader, val_loader, test_loader

def build_classifier(input_img_size, lr):
    """
    Returns a compiled classifier. 
    Architecture is fixed, inputs change the image size and the learning rate.
    """ 
    # Initializing 
    classifier = Sequential()

    # First convolutional layer
    classifier.add(Conv2D(32, (3, 3), input_shape = (input_img_size, input_img_size, 1), activation = "relu"))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))

    # Second convolutional layer
    classifier.add(Conv2D(32, (3, 3), activation = "relu")) 
    classifier.add(MaxPooling2D(pool_size = (2, 2)))

    # Third convolutional layer
    classifier.add(Conv2D(64, (3, 3), activation = "relu")) 
    classifier.add(MaxPooling2D(pool_size = (2, 2)))

    # Flatten layer
    classifier.add(Flatten())

    # Fully connected layers
    classifier.add(Dense(units = 64, activation = "relu"))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(units = 1, activation = "sigmoid"))

    classifier.compile(optimizer = tensorflow.keras.optimizers.Adam(learning_rate=lr),
                    loss = "binary_crossentropy", 
                    metrics = ["accuracy"])

    return classifier

if __name__ == "__main__":
    
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    IMG_SIZE = 128
    LR = 0.001
    EPOCHS = 5
    


    train_loader, val_loader, test_loader = load_data_splits(validation_ratio=0.2,
                                                     target_img_size=IMG_SIZE,
                                                     batch_size=32)
    classifier = build_classifier(IMG_SIZE, LR)
    
    mlflow.tensorflow.autolog()
    with mlflow.start_run(experiment_id = get_experiment_id('mario_wario')):
      # # Single parameter
      # mlflow.log_param("img_size", IMG_SIZE)

      # # Multiple parameters
      # mlflow.log_params({
      #     "img_size": IMG_SIZE,
      #     "learning_rate": LR,
      #     "epochs": EPOCHS
      # })

      # # Single metric
      # mlflow.log_metric("test_set_loss", test_loss, step=1)


      # # Multiple metrics
      # mlflow.log_metrics(
      #     {
      #         "test_set_loss": test_loss,
      #         "test_set_accuracy": test_accuracy,
      #     }
      # )

      # mlflow.log_artifact(MODELS_DIR)

      # mlflow.log_text("Here you can add general inforamtion about the run","run_info.txt")

      print("Training the classifier...")
      classifier.fit(train_loader,
                validation_data=val_loader,
                epochs = EPOCHS)
      print("Training completed.")

      print("Evaluating the classifier...")
      test_loss, test_accuracy = classifier.evaluate(test_loader)
      print("Evaluating completed.")
      print("Saving the classifier...")
      classifier.save(os.path.join(MODELS_DIR, 'my_model.keras'))
      print("done.")
    # with dagshub_logger() as logger:
    #     logger.log_metrics(loss=test_loss, accuracy=test_accuracy)
    #     logger.log_hyperparams({
    #         "img_size": IMG_SIZE,
    #         "learning_rate": LR,
    #         "epochs": EPOCHS
    #     })



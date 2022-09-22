from config import Config
from model.classifier import SlotClassifier
import torch.nn as nn
if __name__ == '__main__':
    config = Config()
    slot_classifier = SlotClassifier(config.hidden_size, config.slot_labels_num, config.dropout_rate)
    print(slot_classifier)

    sequence_classification = nn.Sequential(
        nn.Dropout(config.dropout_rate),
        nn.Linear(config.hidden_size, config.slot_labels_num),
    )
    print(sequence_classification)
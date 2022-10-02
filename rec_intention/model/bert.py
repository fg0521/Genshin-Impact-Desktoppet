import torch.nn as nn
from transformers import BertModel, BertPreTrainedModel,DistilBertModel,AlbertModel
from rec_intention.model.classifier import IntentClassifier, SlotClassifier


class JointBert(nn.Module):

    def __init__(self, config):
        super(JointBert,self).__init__()
        self.bert = AlbertModel.from_pretrained(config.pre_train_model)
        self.intent_classifier = IntentClassifier(config.hidden_size, config.intent_labels_num,config.dropout_rate)
        self.slot_classifier = SlotClassifier(config.hidden_size, config.slot_labels_num,config.dropout_rate)
        self.criterion = nn.CrossEntropyLoss()

    def forward(self,input_ids,attention_mask,token_type_ids,intent_label_ids=None, slot_labels_ids=None):
        output = self.bert(input_ids,attention_mask,token_type_ids)
        token_output = output[0]
        pooled_output = output[1]
        intent_output = self.intent_classifier(pooled_output)
        slot_output = self.slot_classifier(token_output)
        if intent_label_ids is not None and slot_labels_ids is not None:
            active_loss = attention_mask.view(-1) == 1
            active_logits = slot_output.view(-1, slot_output.shape[2])[active_loss]
            active_labels = slot_labels_ids.view(-1)[active_loss]

            intent_loss = self.criterion(intent_output, intent_label_ids)
            slot_loss = self.criterion(active_logits, active_labels)

            total_loss = intent_loss + slot_loss
            return total_loss
        else:
            return intent_output,slot_output
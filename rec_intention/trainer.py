import os
import numpy as np
import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertConfig
import torch.nn as nn
from config import Config
from dataset import BertDataset
from model.bert import JointBert
from preprocess import Processor, get_features


class Trainer():
    def __init__(self,model,config):
        self.model = model
        self.config = config
        self.optimizer = Adam(self.model.parameters(),lr=config.lr)
        self.epoch = config.epoch
        self.device = config.device
        self.criterion = nn.CrossEntropyLoss()

    def train(self,train_loader):
        now_step = 0
        total_step = len(train_loader)*self.epoch
        self.model.train()
        for epoch in range(self.epoch):
            for step,train_batch in enumerate(train_loader):
                for key in train_batch.keys():
                    train_batch[key] = train_batch[key].to(self.device)
                input_ids = train_batch['input_ids']
                attention_mask = train_batch['attention_mask']
                token_type_ids = train_batch['token_type_ids']
                seq_label_ids = train_batch['seq_label_ids']
                token_label_ids = train_batch['token_label_ids']
                total_loss = self.model(input_ids,attention_mask,token_type_ids,seq_label_ids,token_label_ids)
                self.model.zero_grad()
                total_loss.backward()
                self.optimizer.step()
                print(f'[train] eopch{epoch+1}: {round(now_step/total_step*100,2)}% loss:{total_loss.item()}')
                now_step+=1
            if (epoch+1)%self.config.save_epoch == 0:
                if not os.path.exists(self.config.checkpoint_path):
                    os.mkdir(self.config.checkpoint_path)
                torch.save(self.model.state_dict(), os.path.join(self.config.checkpoint_path, f'epoch{epoch+1}_loss{total_loss.item()}'))

if __name__ == '__main__':
    config = Config()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    config.device = device
    tokenizer = BertTokenizer.from_pretrained(config.pre_train_model)
    raw_examples = Processor.get_examples(config.train_path, 'train')
    train_features = get_features(raw_examples, tokenizer, config)
    train_dataset = BertDataset(train_features)
    train_loader = DataLoader(train_dataset, batch_size=config.batchsize, shuffle=True)
    model = JointBert(config)
    model.to(device)
    trainer = Trainer(model,config)
    trainer.train(train_loader)
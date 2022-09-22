
class Config():


    hidden_size = 768
    dropout_rate = 0.1
    lr = 2e-5
    epoch = 10
    save_epoch = 2
    batchsize = 32
    max_len = 40
    checkpoint_path = 'checkpoints'
    pre_train_model = 'pre_train_model/chinese-bert-wwm-ext'
    train_path = 'data/train_process.json'
    device = 'cpu'
    seq_labels_path = 'data/intents.txt'
    token_labels_path = 'data/slots.txt'
    seqlabel2id = {}
    id2seqlabel = {}
    with open(seq_labels_path, 'r') as fp:
        seq_labels = fp.read().split('\n')
        for i, label in enumerate(seq_labels):
            seqlabel2id[label] = i
            id2seqlabel[i] = label

    tokenlabel2id = {}
    id2tokenlabel = {}
    with open(token_labels_path, 'r') as fp:
        token_labels = fp.read().split('\n')
        for i, label in enumerate(token_labels):
            tokenlabel2id[label] = i
            id2tokenlabel[i] = label
    tmp = ['O']
    for label in token_labels:
        B_label = 'B-' + label
        I_label = 'I-' + label
        tmp.append(B_label)
        tmp.append(I_label)
    nerlabel2id = {}
    id2nerlabel = {}
    for i, label in enumerate(tmp):
        nerlabel2id[label] = i
        id2nerlabel[i] = label

    intent_labels_num = len(seq_labels)
    slot_labels_num = len(tmp)
# coding:utf-8
import torch
import numpy as np
import json
import opennre
from opennre import encoder, model, framework

ckpt = 'ckpt/wiki80_cnn_softmax.pth.tar'
wordi2d = json.load(open('pretrain/glove/glove.6B.50d_word2id.json'))
word2vec = np.load('pretrain/glove/glove.6B.50d_mat.npy')
rel2id = json.load(open('benchmark/wiki80/wiki80_rel2id.json'))
sentence_encoder = opennre.encoder.CNNEncoder(token2id=wordi2d,
                                             max_length=40,
                                             word_size=50,
                                             position_size=5,
                                             hidden_size=230,
                                             blank_padding=True,
                                             kernel_size=3,
                                             padding_size=1,
                                             word2vec=word2vec,
                                             dropout=0.5)
model = opennre.model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)
framework = opennre.framework.SentenceRE(
    train_path='benchmark/wiki80/wiki80_train.txt',
    val_path='benchmark/wiki80/wiki80_val.txt',
    test_path='benchmark/wiki80/wiki80_val.txt',
    model=model,
    ckpt=ckpt,
    batch_size=64,
    max_epoch=100,
    lr=0.1,
    weight_decay=1e-5,
    opt='sgd')
# Train
framework.train_model()
# Test
framework.load_state_dict(torch.load(ckpt)['state_dict'])
result = framework.eval_model(framework.test_loader)
print('Accuracy on test set: {}'.format(result['acc']))

#!/usr/bin/env python
# coding: utf-8

# # **一、项目背景介绍**
# 
# 垃圾分类的意义在于增加对环境的保护和降低垃圾的处理成本。减少土地侵蚀、提高经济价值、减少环境污染、保护生态环境变废为宝，有效利用资源；提高垃圾的资源价值和经济价值，力争物尽其用;可以减少垃圾处理量和处理设备，降低处理成本，减少土地资源的消耗;具有社会、经济、生态等几方面的效益。我们可以将模型部署在相关的硬件上来实现落地应用。
# 

# # **二、数据介绍**
# 
# 
# 数据集来源： [垃圾分类](https://aistudio.baidu.com/aistudio/datasetdetail/108025)
# 
# 归类领域：计算机视觉、分类任务
# 
# 数据类型：图片、文件
# 
# 保存格式：jpg,txt
# 
# 垃圾分类数据集 包含6个分类：纸板（393），玻璃（491），金属（400），纸（584），塑料（472）和垃圾（127）。
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/d4b70d1cf5d9436499037eaa3e77589c41dbcadee9f74d17bc8b91b3989f047c)
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/f5816c7699cf4239ad102fc07b24095b27cdf0c30dfa41f1a86758e9168d92bd)
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/d728c04b91f6413297337542eedc064a8168d3d237424855ab6c5092c800afe4)
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/96ae98316156427b992b1f958c23253a5038b785d4bb4a9e9cb741511e6da891)
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/0f0d4d4adfd24dd388c6d408bcb0d4fa39badfbebdf94cf7ae6e8b2c5023f8e0)
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/4c70fd7d359043429d33e1b64846eb37525cc034a8664e01af08693fbac37fca)
# 

# ## **2.1 解压数据集**
# 
# 解压后把Garbage classification改为 Garbage_classification

# In[ ]:


# 样例：解压你所挂载的数据集在同级目录下
get_ipython().system('unzip -oq /home/aistudio/data/data128034/垃圾分类.zip  -d work/laji')
# 查看数据集的目录结构
get_ipython().system('tree work/laji -d')


# ## **2.2 划分数据集**
# 
# 'train'： 'val'： 'test'=0.8：0.1,0.1

# In[ ]:


import os
import random
import shutil
from shutil import copy2

def data_set_split(src_data_folder, target_data_folder, train_scale=0.8, val_scale=0.1, test_scale=0.1):
    print("开始数据集划分")
    class_names = os.listdir(src_data_folder)
    split_names = ['train', 'val', 'test']
    for split_name in split_names:
        split_path = os.path.join(target_data_folder, split_name)
        if os.path.isdir(split_path):
            pass
        else:
            os.mkdir(split_path)
        for class_name in class_names:
            class_split_path = os.path.join(split_path, class_name)
            if os.path.isdir(class_split_path):
                pass
            else:
                os.mkdir(class_split_path)

    for class_name in class_names:
        current_class_data_path = os.path.join(src_data_folder, class_name)
        current_all_data = os.listdir(current_class_data_path)
        current_data_length = len(current_all_data)
        current_data_index_list = list(range(current_data_length))
        random.shuffle(current_data_index_list)

        train_folder = os.path.join(os.path.join(target_data_folder, 'train'), class_name)
        val_folder = os.path.join(os.path.join(target_data_folder, 'val'), class_name)
        test_folder = os.path.join(os.path.join(target_data_folder, 'test'), class_name)
        train_stop_flag = current_data_length * train_scale
        val_stop_flag = current_data_length * (train_scale + val_scale)
        current_idx = 0
        train_num = 0
        val_num = 0
        test_num = 0
        for i in current_data_index_list:
            src_img_path = os.path.join(current_class_data_path, current_all_data[i])
            if current_idx <= train_stop_flag:
                copy2(src_img_path, train_folder)
                train_num = train_num + 1
            elif (current_idx > train_stop_flag) and (current_idx <= val_stop_flag):
                copy2(src_img_path, val_folder)
                val_num = val_num + 1
            else:
                copy2(src_img_path, test_folder)
                test_num = test_num + 1
            
            current_idx = current_idx + 1

        print("*********************************{}*************************************".format(class_name))
        print("{}类按照{}：{}：{}的比例划分完成，一共{}张图片".format(class_name, train_scale, val_scale, test_scale, current_data_length))
        print("训练集{}：{}张".format(train_folder, train_num))
        print("验证集{}：{}张".format(val_folder, val_num))
        print("测试集{}：{}张".format(test_folder, test_num))


if __name__ == '__main__':
    src_data_folder = "work/laji/Garbage_classification/Garbage_classification"
    target_data_folder = "work/laji/Garbage_classification"
    data_set_split(src_data_folder, target_data_folder)


# # **三、定义部分超参数**

# In[ ]:


import paddle
paddle.seed(8888)
import numpy as np
from typing import Callable
#参数配置
config_parameters = {
    "class_dim": 6,  #分类数
    "target_path":"/home/aistudio/work/laji/",                     
    'train_image_dir': 'work/laji/Garbage_classification/train',
    'eval_image_dir': 'work/laji/Garbage_classification/val',
    'epochs':50,
    'batch_size': 64,
    'lr': 0.01
}
#数据集的定义
class TowerDataset(paddle.io.Dataset):
    """
    步骤一：继承paddle.io.Dataset类
    """
    def __init__(self, transforms: Callable, mode: str ='train'):
        """
        步骤二：实现构造函数，定义数据读取方式
        """
        super(TowerDataset, self).__init__()
        
        self.mode = mode
        self.transforms = transforms

        train_image_dir = config_parameters['train_image_dir']
        eval_image_dir = config_parameters['eval_image_dir']

        train_data_folder = paddle.vision.DatasetFolder(train_image_dir)
        eval_data_folder = paddle.vision.DatasetFolder(eval_image_dir)
        if self.mode  == 'train':
            self.data = train_data_folder
        elif self.mode  == 'eval':
            self.data = eval_data_folder

    def __getitem__(self, index):
        """
        步骤三：实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据，对应的标签）
        """
        data = np.array(self.data[index][0]).astype('float32')

        data = self.transforms(data)

        label = np.array([self.data[index][1]]).astype('int64')
        
        return data, label
        
    def __len__(self):
        """
        步骤四：实现__len__方法，返回数据集总数目
        """
        return len(self.data)


from paddle.vision import transforms as T

#数据增强
transform_train =T.Compose([T.Resize((256,256)),
                            #T.RandomVerticalFlip(10),
                            #T.RandomHorizontalFlip(10),
                            T.RandomRotation(10),
                            T.Transpose(),
                            T.Normalize(mean=[0, 0, 0],                           # 像素值归一化
                                        std =[255, 255, 255]),                    # transforms.ToTensor(), # transpose操作 + (img / 255),并且数据结构变为PaddleTensor
                            T.Normalize(mean=[0.50950350, 0.54632660, 0.57409690],# 减均值 除标准差    
                                        std= [0.26059777, 0.26041326, 0.29220656])# 计算过程：output[channel] = (input[channel] - mean[channel]) / std[channel]
                            ])
transform_eval =T.Compose([ T.Resize((256,256)),
                            T.Transpose(),
                            T.Normalize(mean=[0, 0, 0],                           # 像素值归一化
                                        std =[255, 255, 255]),                    # transforms.ToTensor(), # transpose操作 + (img / 255),并且数据结构变为PaddleTensor
                            T.Normalize(mean=[0.50950350, 0.54632660, 0.57409690],# 减均值 除标准差    
                                        std= [0.26059777, 0.26041326, 0.29220656])# 计算过程：output[channel] = (input[channel] - mean[channel]) / std[channel]
                            ])

train_dataset = TowerDataset(mode='train',transforms=transform_train)
eval_dataset  = TowerDataset(mode='eval', transforms=transform_eval )
#数据异步加载
train_loader = paddle.io.DataLoader(train_dataset, 
                                    places=paddle.CUDAPlace(0), 
                                    batch_size=16, 
                                    shuffle=True,
                                    #num_workers=2,
                                    #use_shared_memory=True
                                    )
eval_loader = paddle.io.DataLoader (eval_dataset, 
                                    places=paddle.CUDAPlace(0), 
                                    batch_size=16,
                                    #num_workers=2,
                                    #use_shared_memory=True
                                    )

print('训练集样本量: {}，验证集样本量: {}'.format(len(train_loader), len(eval_loader)))


# # **四、模型介绍——MobileViT组网**
# 
# MobileViT：一种用于移动设备的轻量级通用视觉Transformer，据作者称，这是首个能比肩轻量级CNN网络性能的轻量级ViT工作，表现SOTA！性能优于MobileNetV3、CrossViT等网络。
# 
# 轻量级卷积神经网络 (CNN) 是移动视觉任务的de-facto。他们的空间归纳偏差使他们能够在不同的视觉任务中以较少的参数学习表示。然而，这些网络在空间上是局部的。为了学习全局表示，已经采用了基于自注意力的视觉Transformer（ViT）。与 CNN 不同，ViT 是"重量级"的。在本文中，我们提出以下问题：是否有可能结合 CNNs 和 ViTs 的优势，为移动视觉任务构建一个轻量级、低延迟的网络？为此，我们推出了 MobileViT，这是一种用于移动设备的轻量级通用视觉Transformer。
# 
# 结构上也非常简单，但是同样能够实现一个不错的精度表现
# 
# 原论文下载：https://arxiv.org/pdf/2110.02178.pdf
# 
# MobileViT 与 Mobilenet 系列模型一样模型的结构都十分简单
# 
# MobileViT带来了一些新的结果:
# 
# 1.更好的性能:在相同的参数情况下,余现有的轻量级CNN相比,mobilevit模型在不同的移动视觉任务中实现了更好的性能.
# 
# 2.更好的泛化能力:泛化能力是指训练和评价指标之间的差距.对于具有相似的训练指标的两个模型,具有更好评价指标的模型更具有通用性,因为它可以更好地预测未见的数据集.与CNN相比,即使有广泛的数据增强,其泛化能力也很差,mobilevit显示出更好的泛化能力(如下图).
# 
# 3.更好的鲁棒性:一个好的模型应该对超参数具有鲁棒性,因为调优这些超参数会消耗时间和资源.与大多数基于ViT的模型不同,mobilevit模型使用基于增强训练,与L2正则化不太敏感.
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/4090a9935e794caab9332f03b88ddcf76692c80b3086464faacb790b118d4063)
# 

# In[ ]:


import paddle
import paddle.nn as nn




def conv_1x1_bn(inp, oup):
    return nn.Sequential(
        nn.Conv2D(inp, oup, 1, 1, 0, bias_attr=False),
        nn.BatchNorm2D(oup),
        nn.Silu()
    )


def conv_nxn_bn(inp, oup, kernal_size=3, stride=1):
    return nn.Sequential(
        nn.Conv2D(inp, oup, kernal_size, stride, 1, bias_attr=False),
        nn.BatchNorm2D(oup),
        nn.Silu()
    )


class PreNorm(nn.Layer):
    def __init__(self, axis, fn):
        super().__init__()
        self.norm = nn.LayerNorm(axis)
        self.fn = fn
    
    def forward(self, x, **kwargs):
        return self.fn(self.norm(x), **kwargs)


class FeedForward(nn.Layer):
    def __init__(self, axis, hidden_axis, dropout=0.):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(axis, hidden_axis),
            nn.Silu(),
            nn.Dropout(dropout),
            nn.Linear(hidden_axis, axis),
            nn.Dropout(dropout)
        )
    
    def forward(self, x):
        return self.net(x)


class Attention(nn.Layer):
    def __init__(self, axis, heads=8, axis_head=64, dropout=0.):
        super().__init__()
        inner_axis = axis_head *  heads
        project_out = not (heads == 1 and axis_head == axis)

        self.heads = heads
        self.scale = axis_head ** -0.5

        self.attend = nn.Softmax(axis = -1)
        self.to_qkv = nn.Linear(axis, inner_axis * 3, bias_attr = False)

        self.to_out = nn.Sequential(
            nn.Linear(inner_axis, axis),
            nn.Dropout(dropout)
        ) if project_out else nn.Identity()

    def forward(self, x):
 
        q,k,v = self.to_qkv(x).chunk(3, axis=-1)

        b,p,n,hd = q.shape
        b,p,n,hd = k.shape
        b,p,n,hd = v.shape
        q = q.reshape((b, p, n, self.heads, -1)).transpose((0, 1, 3, 2, 4))
        k = k.reshape((b, p, n, self.heads, -1)).transpose((0, 1, 3, 2, 4))
        v = v.reshape((b, p, n, self.heads, -1)).transpose((0, 1, 3, 2, 4))

        dots = paddle.matmul(q, k.transpose((0, 1, 2, 4, 3))) * self.scale
        attn = self.attend(dots)

        out = (attn.matmul(v)).transpose((0, 1, 3, 2, 4)).reshape((b, p, n,-1))
        return self.to_out(out)



class Transformer(nn.Layer):
    def __init__(self, axis, depth, heads, axis_head, mlp_axis, dropout=0.):
        super().__init__()
        self.layers = nn.LayerList([])
        for _ in range(depth):
            self.layers.append(nn.LayerList([
                PreNorm(axis, Attention(axis, heads, axis_head, dropout)),
                PreNorm(axis, FeedForward(axis, mlp_axis, dropout))
            ]))
    
    def forward(self, x):
        for attn, ff in self.layers:
            x = attn(x) + x
            x = ff(x) + x
        return x


class MV2Block(nn.Layer):
    def __init__(self, inp, oup, stride=1, expansion=4):
        super().__init__()
        self.stride = stride
        assert stride in [1, 2]

        hidden_axis = int(inp * expansion)
        self.use_res_connect = self.stride == 1 and inp == oup

        if expansion == 1:
            self.conv = nn.Sequential(
                # dw
                nn.Conv2D(hidden_axis, hidden_axis, 3, stride, 1, groups=hidden_axis, bias_attr=False),
                nn.BatchNorm2D(hidden_axis),
                nn.Silu(),
                # pw-linear
                nn.Conv2D(hidden_axis, oup, 1, 1, 0, bias_attr=False),
                nn.BatchNorm2D(oup),
            )
        else:
            self.conv = nn.Sequential(
                # pw
                nn.Conv2D(inp, hidden_axis, 1, 1, 0, bias_attr=False),
                nn.BatchNorm2D(hidden_axis),
                nn.Silu(),
                # dw
                nn.Conv2D(hidden_axis, hidden_axis, 3, stride, 1, groups=hidden_axis, bias_attr=False),
                nn.BatchNorm2D(hidden_axis),
                nn.Silu(),
                # pw-linear
                nn.Conv2D(hidden_axis, oup, 1, 1, 0, bias_attr=False),
                nn.BatchNorm2D(oup),
            )

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)


class MobileViTBlock(nn.Layer):
    def __init__(self, axis, depth, channel, kernel_size, patch_size, mlp_axis, dropout=0.):
        super().__init__()
        self.ph, self.pw = patch_size

        self.conv1 = conv_nxn_bn(channel, channel, kernel_size)
        self.conv2 = conv_1x1_bn(channel, axis)

        self.transformer = Transformer(axis, depth, 1, 32, mlp_axis, dropout)

        self.conv3 = conv_1x1_bn(axis, channel)
        self.conv4 = conv_nxn_bn(2 * channel, channel, kernel_size)
    
    def forward(self, x):
        y = x.clone()

        # Local representations
        x = self.conv1(x)
        x = self.conv2(x)
        
        # Global representations
        n, c, h, w = x.shape

        x = x.transpose((0,3,1,2)).reshape((n,self.ph * self.pw,-1,c))
        x = self.transformer(x)
        x = x.reshape((n,h,-1,c)).transpose((0,3,1,2))


        # Fusion
        x = self.conv3(x)
        x = paddle.concat((x, y), 1)
        x = self.conv4(x)
        return x


class MobileViT(nn.Layer):
    def __init__(self, image_size, axiss, channels, num_classes, expansion=4, kernel_size=3, patch_size=(2, 2)):
        super().__init__()
        ih, iw = image_size
        ph, pw = patch_size
        assert ih % ph == 0 and iw % pw == 0

        L = [2, 4, 3]

        self.conv1 = conv_nxn_bn(3, channels[0], stride=2)

        self.mv2 = nn.LayerList([])
        self.mv2.append(MV2Block(channels[0], channels[1], 1, expansion))
        self.mv2.append(MV2Block(channels[1], channels[2], 2, expansion))
        self.mv2.append(MV2Block(channels[2], channels[3], 1, expansion))
        self.mv2.append(MV2Block(channels[2], channels[3], 1, expansion))   # Repeat
        self.mv2.append(MV2Block(channels[3], channels[4], 2, expansion))
        self.mv2.append(MV2Block(channels[5], channels[6], 2, expansion))
        self.mv2.append(MV2Block(channels[7], channels[8], 2, expansion))
        
        self.mvit = nn.LayerList([])
        self.mvit.append(MobileViTBlock(axiss[0], L[0], channels[5], kernel_size, patch_size, int(axiss[0]*2)))
        self.mvit.append(MobileViTBlock(axiss[1], L[1], channels[7], kernel_size, patch_size, int(axiss[1]*4)))
        self.mvit.append(MobileViTBlock(axiss[2], L[2], channels[9], kernel_size, patch_size, int(axiss[2]*4)))

        self.conv2 = conv_1x1_bn(channels[-2], channels[-1])

        self.pool = nn.AvgPool2D(ih//32, 1)
        self.fc = nn.Linear(channels[-1], num_classes, bias_attr=False)

    def forward(self, x):
        x = self.conv1(x)
        x = self.mv2[0](x)

        x = self.mv2[1](x)
        x = self.mv2[2](x)
        x = self.mv2[3](x)      # Repeat

        x = self.mv2[4](x)
        x = self.mvit[0](x)

        x = self.mv2[5](x)
        x = self.mvit[1](x)

        x = self.mv2[6](x)
        x = self.mvit[2](x)
        x = self.conv2(x)

        x = self.pool(x)
        x = x.reshape((-1, x.shape[1]))
        x = self.fc(x)
        return x


def mobilevit_xxs():
    axiss = [64, 80, 96]
    channels = [16, 16, 24, 24, 48, 48, 64, 64, 80, 80, 320]
    return MobileViT((256, 256), axiss, channels, num_classes=1000, expansion=2)


def mobilevit_xs():
    axiss = [96, 120, 144]
    channels = [16, 32, 48, 48, 64, 64, 80, 80, 96, 96, 384]
    return MobileViT((256, 256), axiss, channels, num_classes=1000)


def mobilevit_s():
    axiss = [144, 192, 240]
    channels = [16, 32, 64, 64, 96, 96, 128, 128, 160, 160, 640]
    return MobileViT((256, 256), axiss, channels, num_classes=6)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ## **4.1 模型测试**

# In[ ]:


if __name__ == '__main__':
    img = paddle.rand([5, 3, 256, 256])

    vit = mobilevit_xxs()
    out = vit(img)
    print(out.shape)


    vit = mobilevit_xs()
    out = vit(img)
    print(out.shape)


    vit = mobilevit_s()
    out = vit(img)
    print(out.shape)


# ## **五、模型训练**
# 
# # **5.1实例化模型**

# In[ ]:


model = mobilevit_s()
model = paddle.Model(model)


# In[ ]:


#优化器选择
class SaveBestModel(paddle.callbacks.Callback):
    def __init__(self, target=0.5, path='work/best_model2', verbose=0):
        self.target = target
        self.epoch = None
        self.path = path

    def on_epoch_end(self, epoch, logs=None):
        self.epoch = epoch

    def on_eval_end(self, logs=None):
        if logs.get('acc') > self.target:
            self.target = logs.get('acc')
            self.model.save(self.path)
            print('best acc is {} at epoch {}'.format(self.target, self.epoch))

callback_visualdl = paddle.callbacks.VisualDL(log_dir='work/no_SA')
callback_savebestmodel = SaveBestModel(target=0.5, path='work/best_model1')
callbacks = [callback_visualdl, callback_savebestmodel]

base_lr = config_parameters['lr']
epochs = config_parameters['epochs']

def make_optimizer(parameters=None):
    momentum = 0.9

    learning_rate= paddle.optimizer.lr.CosineAnnealingDecay(learning_rate=base_lr, T_max=epochs, verbose=False)
    weight_decay=paddle.regularizer.L2Decay(0.0001)
    optimizer = paddle.optimizer.Momentum(
        learning_rate=learning_rate,
        momentum=momentum,
        weight_decay=weight_decay,
        parameters=parameters)
    return optimizer

optimizer = make_optimizer(model.parameters())


model.prepare(optimizer,
              paddle.nn.CrossEntropyLoss(),
              paddle.metric.Accuracy())


# ## **5.2 训练模型需要说明：**
# 
# **lr_schedule:** CosineAnnealingDecay
# 
# **optimize:** Momentum
# 
# **epoch:** 50
#  
# **batch_size:** 64
# 
# **Loss function:** CrossEntropyLoss

# In[ ]:


model.fit(train_loader,
          eval_loader,
          epochs=50,
          batch_size=64,     # 是否打乱样本集     
          callbacks=callbacks, 
          verbose=1)   # 日志展示格式


# # **六、模型评估**

# In[ ]:


# 模型评估
# 加载训练过程保存的最后一个模型
model__state_dict = paddle.load('work/best_model1.pdparams')
model_eval = mobilevit_s()
model_eval.set_state_dict(model__state_dict) 
model_eval.eval()
accs = []
# 开始评估
for _, data in enumerate(eval_loader()):
    x_data = data[0]
    y_data = data[1]
    predicts = model_eval(x_data)
    acc = paddle.metric.accuracy(predicts, y_data)
    accs.append(acc.numpy()[0])
print('模型在验证集上的准确率为：',np.mean(accs))


# # **七、可视化测试模型效果**

# In[104]:


import time
import sys
# 加载训练过程保存的最后一个模型
model__state_dict = paddle.load('work/best_model1.pdparams')
model_predict = mobilevit_s()
model_predict.set_state_dict(model__state_dict) 
model_predict.eval()
infer_imgs_path = os.listdir('work/laji/Garbage_classification/test/glass')
# print(infer_imgs_path)

label_dic={'0': 'cardboard', '1': 'plastic', '2': 'metal', '3': 'paper','4':' glass','5':'trash'}

def load_image(img_path):
    '''
    预测图片预处理
    '''
    img = Image.open(img_path) 
    if img.mode != 'RGB': 
        img = img.convert('RGB') 
    img = img.resize((256, 256), Image.BILINEAR)
    img = np.array(img).astype('float32') 
    img = img.transpose((2, 0, 1)) / 255 # HWC to CHW 及归一化
    return img

# 预测所有图片
for infer_img_path in infer_imgs_path:
    infer_img = load_image('work/laji/Garbage_classification/test/glass/'+infer_img_path)
    infer_img = infer_img[np.newaxis,:, : ,:]  #reshape(-1,3,224,224)
    infer_img = paddle.to_tensor(infer_img)
    result = model_predict(infer_img)
    lab = np.argmax(result.numpy())
    print("样本: {},被预测为:{}".format(infer_img_path,label_dic[str(lab)]))
    img = Image.open('work/laji/Garbage_classification/test/glass/'+infer_img_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    sys.stdout.flush()
    time.sleep(0.5)


# ## **7.1测试模型效果**
# 
# 可以看到预测预测效果还是挺好的
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/7c6e19c826054d93af6a977cd04dbf306cbafd104dba4f1bb8a39f6e638d99c8)
# 

# # **总结与升华**
# 
# 分类模型Mobile-ViT实现一个垃圾分类检测即可完成，MobileViT：一种用于移动设备的轻量级通用视觉Transformer，据作者称，这是首个能比肩轻量级CNN网络性能的轻量级ViT工作，表现SOTA！性能优于MobileNetV3、CrossViT等网络。本次项目实质是属于一个6分类的问题。
# 
# 早期的遇到的问题就是自己对数据进行处理后送入网络，报图片尺寸、维度错误，debug后也找不到问题，然后fork原作者项目进行操作后就可以跑的通，具体之前问题出在哪儿，仍然没得到解决。

# # **参考项目：**
# 
# [Mobile-ViT：改进的一种更小更轻精度更高的模型](https://aistudio.baidu.com/aistudio/projectdetail/2683037?channelType=0&channel=0)

# # **关于作者**
# 
# >- [个人主页](https://aistudio.baidu.com/aistudio/personalcenter/thirdview/474269)
# 
# >- 感兴趣的方向为：目标检测，图像分类，图像分割等。
# 
# >- 不定期更新感兴趣的CV比赛baseline等
# 
# >- 个人荣誉：飞桨开发者技术专家（PPDE）
# 
# >- 欢迎大家有问题留言交流学习，共同进步成长。

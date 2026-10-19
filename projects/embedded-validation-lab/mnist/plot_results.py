"""실제 기록으로 loss/accuracy, confusion matrix, 추론 영상을 저장한다."""
import json
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # 창을 열지 않고 파일로 렌더링한다.
import matplotlib.pyplot as plt
import numpy as np
import torch
from torchvision import datasets, transforms
from train_mnist import DigitCNN

root=Path(__file__).parent
ap=argparse.ArgumentParser()
ap.add_argument('--data',type=Path,default=Path('data'))
args=ap.parse_args()
r=json.loads((root/'results/metrics.json').read_text())
h=r['history']; epochs=[x['epoch'] for x in h]
fig,axes=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
for key,label in [('train','Train'),('validation','Validation')]:
    axes[0].plot(epochs,[x[key+'_loss'] for x in h],'o-',label=label)
    axes[1].plot(epochs,[x[key+'_accuracy']*100 for x in h],'o-',label=label)
for ax in axes: ax.set_xlabel('Epoch');ax.set_xticks(epochs);ax.grid(alpha=.3);ax.legend()
axes[0].set_ylabel('Mean cross-entropy loss');axes[1].set_ylabel('Accuracy (%)')
fig.savefig(root/'results/learning_curves.png',dpi=180);plt.close(fig)
cm=np.array(r['confusion_matrix'])
fig,ax=plt.subplots(figsize=(7,6),layout='constrained')
im=ax.imshow(cm,cmap='Blues');fig.colorbar(im,ax=ax,label='Number of images')
for i in range(10):
    for j in range(10):
        ax.text(j,i,str(cm[i,j]),ha='center',va='center',fontsize=8,
                color='white' if cm[i,j]>cm.max()/2 else '#173247')
ax.set(xticks=range(10),yticks=range(10),xlabel='Predicted digit',ylabel='True digit',
       title=f'Test: {r["correct"]}/10000 = {r["test_accuracy"]*100:.2f}%')
fig.savefig(root/'results/confusion.png',dpi=180);plt.close(fig)
tf=transforms.Compose([transforms.ToTensor(),transforms.Normalize((.1307,),(.3081,))])
test=datasets.MNIST(args.data,train=False,download=True,transform=tf)
model=DigitCNN();model.load_state_dict(torch.load(root/'results/best.pt',weights_only=True)['state_dict'])
model.eval()
with torch.inference_mode():
    images=torch.stack([test[i][0] for i in range(10000)])
    preds=torch.cat([model(b).argmax(1) for b in images.split(256)])
truth=test.targets; wrong=torch.nonzero(preds!=truth).flatten()
indices=list(range(8))+wrong[:8].tolist()
fig,axes=plt.subplots(2,8,figsize=(12,4),layout='constrained')
for ax,i in zip(axes.flat,indices):
    ax.imshow(test.data[i],cmap='gray');ax.axis('off')
    ax.set_title(f'#{i}\nTrue {int(truth[i])} / Pred {int(preds[i])}',fontsize=9,
                 color='#087E82' if preds[i]==truth[i] else '#BC3040')
fig.savefig(root/'results/predictions.png',dpi=180);plt.close(fig)
print(json.dumps({'correct':r['correct'],'incorrect':len(wrong),
                  'class_accuracy':[(i,float(cm[i,i]/cm[i].sum())) for i in range(10)]}))

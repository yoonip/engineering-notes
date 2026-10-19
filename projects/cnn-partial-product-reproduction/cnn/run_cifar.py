"""Independent educational CIFAR/ResNet experiment.

This is newly written reproduction code, not recovered manuscript source or
evidence of a deployed product. No original documents, datasets, trained
checkpoints, or device power claims are bundled. Torchvision supplies the model
definitions and dataset readers; see the repository attribution and README.

GPU training uses AMP, but quantized inference uses IEEE FP32 convolutions with
bounded chunks and INT64 summation: every partial dot has absolute sum <2**24.
PP column removal is implemented before accumulation, never by masking outputs.
"""
from __future__ import annotations
import argparse, copy, csv, hashlib, json, math, os, random, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torchvision import datasets, transforms, models

HERE=Path(__file__).resolve().parent
MEAN=(.491,.482,.446); STD=(.202,.199,.201)

def write_json(path,data):
    Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')

def portable_reference(path,base):
    """Record paths relative to an output directory; never serialize drive roots."""
    try:
        return Path(os.path.relpath(Path(path).resolve(),Path(base).resolve())).as_posix()
    except ValueError:  # Different drives on Windows cannot have a relative path.
        return Path(path).name

def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)
    torch.set_num_threads(8)

def ieee():
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    torch.backends.cudnn.benchmark=False
    torch.backends.cudnn.deterministic=True

def make_model(classes=10,arch='resnet18'):
    m=getattr(models,arch)(weights=None,num_classes=classes)
    m.conv1=nn.Conv2d(3,64,3,1,1,bias=False)
    m.maxpool=nn.Identity()
    return m

def load_data(data_dir,seed,batch,workers,dataset='cifar10',recipe='basic'):
    mean,std=(MEAN,STD) if dataset=='cifar10' else ((.507,.487,.441),(.267,.257,.276))
    dataset_cls=datasets.CIFAR10 if dataset=='cifar10' else datasets.CIFAR100
    classes=10 if dataset=='cifar10' else 100
    plain=transforms.Compose([transforms.ToTensor(),transforms.Normalize(mean,std)])
    augment=transforms.Compose([transforms.RandomCrop(32,padding=4),transforms.RandomHorizontalFlip(),
                               transforms.ToTensor(),transforms.Normalize(mean,std)])
    if recipe=='thesis':
        from thesis_recipe import build_training_transform
        augment=build_training_transform(mean,std)
    train=dataset_cls(data_dir,train=True,download=True,transform=augment)
    val=dataset_cls(data_dir,train=True,download=False,transform=plain)
    test=dataset_cls(data_dir,train=False,download=False,transform=plain)
    y=np.array(train.targets); rng=np.random.default_rng(2026)
    vi=np.concatenate([rng.permutation(np.flatnonzero(y==c))[:5000//classes] for c in range(classes)])
    vi=np.sort(vi); ti=np.setdiff1d(np.arange(50000),vi)
    gen=torch.Generator().manual_seed(seed)
    kwargs=dict(batch_size=batch,num_workers=workers,pin_memory=torch.cuda.is_available(),
                persistent_workers=workers>0)
    train_subset=torch.utils.data.Subset(train,ti)
    if recipe=='thesis':
        from thesis_recipe import repeat_dataset
        train_subset=repeat_dataset(train_subset,repeats=3)
    tr=torch.utils.data.DataLoader(train_subset,shuffle=True,generator=gen,**kwargs)
    vl=torch.utils.data.DataLoader(torch.utils.data.Subset(val,vi),shuffle=False,**kwargs)
    te=torch.utils.data.DataLoader(test,shuffle=False,**kwargs)
    return tr,vl,te,ti,vi

@torch.no_grad()
def evaluate(m,loader,device,max_samples=None):
    m.eval(); loss=0.; labels=[]; preds=[]; logits=[]; start=time.time()
    for x,y in loader:
        if max_samples and sum(len(z) for z in labels)>=max_samples: break
        if max_samples:
            rem=max_samples-sum(len(z) for z in labels); x=x[:rem]; y=y[:rem]
        x=x.to(device,non_blocking=True); y=y.to(device,non_blocking=True)
        z=m(x); loss+=F.cross_entropy(z,y,reduction='sum').item()
        labels.append(y.cpu().numpy()); preds.append(z.argmax(1).cpu().numpy()); logits.append(z.cpu().numpy())
    y=np.concatenate(labels); p=np.concatenate(preds); z=np.concatenate(logits)
    return dict(accuracy=float((p==y).mean()*100),correct=int((p==y).sum()),n=len(y),
                loss=loss/len(y),seconds=time.time()-start),y,p,z

def int_dot(x,w,op):
    """IEEE FP32 exact integer partial dots, INT64 accumulation (groups=1).
    Inputs integral FP32. Triangle bound makes FP32 products/additions exact.
    TF32, AMP and reduced precision must be disabled by caller.
    """
    kernel=math.prod(w.shape[2:]) if w.ndim==4 else 1
    bound=max(1,int(x.abs().max().item()))*max(1,int(w.abs().max().item()))*kernel
    chunk=max(1,min(w.shape[1],((1<<24)-1)//bound))
    acc=None
    for start in range(0,w.shape[1],chunk):
        part=op(x[:,start:start+chunk].contiguous(),w[:,start:start+chunk].contiguous())
        part=part.round().to(torch.int64)
        acc=part if acc is None else acc+part
    return acc

def quantized_dot(xi,wi,op,k,mode):
    raw=int_dot(xi,wi,op)
    if k==0 or mode=='quant': return raw
    if mode=='postacc':
        return torch.bitwise_left_shift(torch.bitwise_right_shift(raw,k),k)
    if mode!='columns': raise ValueError(mode)
    # For k<n: omitted columns contain no sign-bit partial products.
    # This is the same Baugh-Wooley function as circuit/arithmetic.py.
    ai=xi.to(torch.int64); bi=wi.to(torch.int64)
    correction=torch.zeros_like(raw)
    for i in range(k):
        abits=((ai>>i)&1).to(torch.float32)
        blow=(bi&((1<<(k-i))-1)).to(torch.float32)
        correction+=int_dot(abits,blow,op)*(1<<i)
    return raw-correction

def direct_conv(x,w,stride,padding,dilation):
    """Explicit im2col/GEMM: excludes Winograd/FFT transformed arithmetic.
    IEEE matmul plus bounded integer chunks is exact in the input integer dot.
    """
    patches=F.unfold(x,kernel_size=w.shape[2:],dilation=dilation,padding=padding,stride=stride)
    out=torch.matmul(w.flatten(1),patches)
    oh=(x.shape[2]+2*padding[0]-dilation[0]*(w.shape[2]-1)-1)//stride[0]+1
    ow=(x.shape[3]+2*padding[1]-dilation[1]*(w.shape[3]-1)-1)//stride[1]+1
    return out.view(x.shape[0],w.shape[0],oh,ow)

def quantized_conv(x,w,stride,padding,dilation,k,mode):
    """Unfold once and reuse its integer bit planes for all PP columns."""
    patches=F.unfold(x,kernel_size=w.shape[2:],dilation=dilation,padding=padding,stride=stride)
    acc=quantized_dot(patches,w.flatten(1),lambda a,b:torch.matmul(b,a),k,mode)
    oh=(x.shape[2]+2*padding[0]-dilation[0]*(w.shape[2]-1)-1)//stride[0]+1
    ow=(x.shape[3]+2*padding[1]-dilation[1]*(w.shape[3]-1)-1)//stride[1]+1
    return acc.view(x.shape[0],w.shape[0],oh,ow)

class QuantLayer(nn.Module):
    def __init__(self,layer,bits,k,mode,activation_max):
        super().__init__(); self.base=layer
        self.bits=bits; self.k=k; self.mode=mode; self.activation_max=float(activation_max)
        self.qmax=(1<<(bits-1))-1; self.qmin=-(1<<(bits-1))
        self.clipped=0;self.observed=0
        self.register_buffer('bias_codes',None)
        if mode=='columns' and not 0<=k<=bits-1: raise ValueError('Unsupported sign-column truncation')
    def forward(self,x):
        w=self.base.weight; sx=max(self.activation_max,1e-8)/self.qmax
        sw=w.detach().abs().max().clamp_min(1e-8)/self.qmax
        with torch.no_grad(),torch.autocast(device_type=x.device.type,enabled=False):
            scaled=(x.detach().float()/sx).round()
            if not self.training:
                self.clipped+=int(((scaled<self.qmin)|(scaled>self.qmax)).sum().item())
                self.observed+=scaled.numel()
            xi=scaled.clamp(self.qmin,self.qmax)
            wi=(w.detach().float()/sw).round().clamp(self.qmin,self.qmax)
            if isinstance(self.base,nn.Conv2d):
                acc=quantized_conv(xi,wi,self.base.stride,self.base.padding,self.base.dilation,self.k,self.mode)
            else:
                acc=quantized_dot(xi,wi,lambda a,b:F.linear(a,b,None),self.k,self.mode)
            if self.bias_codes is not None:acc=acc+self.bias_codes
            out=acc.float()*(sx*sw)
            if self.base.bias is not None: out=out+self.base.bias.float()
        if self.training:
            # STE surrogate: true quantized PP forward, ordinary real-dot backward.
            fp=self.base(x)
            return fp+(out-fp).detach()
        return out

def replace_quant(m,bits,mode,stage_k,amax):
    for name,child in list(m.named_modules()):
        if isinstance(child,(nn.Conv2d,nn.Linear)):
            stage=name.split('.')[0]
            k=stage_k.get(stage,stage_k.get('all',0))
            parent=m
            path=name.split('.')
            for part in path[:-1]: parent=getattr(parent,part)
            setattr(parent,path[-1],QuantLayer(child,bits,k,mode,amax[name]))
    return m

@torch.no_grad()
def calibrate(m,loader,device,max_samples=1024):
    """Activation clipping maxima on training-derived validation data only."""
    amax={}; hooks=[]
    for name,child in m.named_modules():
        if isinstance(child,(nn.Conv2d,nn.Linear)):
            def hook(module,args,name=name):
                amax[name]=max(amax.get(name,0.),float(args[0].abs().max().item()))
            hooks.append(child.register_forward_pre_hook(hook))
    evaluate(m,loader,device,max_samples)
    for hook in hooks: hook.remove()
    return amax

def paired_metrics(y,baseline,p,seed=2026):
    b=baseline==y; a=p==y; d=a.astype(float)-b.astype(float)
    # Paired bootstrap via multinomial counts over -1,0,+1; same estimator.
    rng=np.random.default_rng(seed); probs=np.array([(d==-1).mean(),(d==0).mean(),(d==1).mean()])
    boot=rng.multinomial(len(y),probs,size=5000)
    delta=(boot[:,2]-boot[:,0])*100/len(y)
    return dict(delta_pp=float(d.mean()*100),paired_bootstrap95_pp=np.quantile(delta,[.025,.975]).tolist(),
        baseline_only_correct=int((b&~a).sum()),variant_only_correct=int((a&~b).sum()),
        changed_predictions=int((p!=baseline).sum()))

def train(args):
    seed_all(args.seed); device='cuda' if torch.cuda.is_available() else 'cpu'; ieee()
    tr,vl,te,ti,vi=load_data(args.data,args.seed,args.batch,args.workers,args.dataset,args.recipe)
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    np.savez(out/'split_indices.npz',train_indices=ti,validation_indices=vi,test_indices=np.arange(10000))
    config=vars(args).copy()
    for key in ('data','out','resume','checkpoint','bias_file'):
        if config.get(key):config[key]=portable_reference(config[key],out)
    config.update(device=device,torch=torch.__version__,numpy=np.__version__,
        gpu=torch.cuda.get_device_name(0) if device=='cuda' else None,
        requested_train_n=args.train_n,train_unique_available=len(ti),
        train_n=min(args.train_n,len(tr.dataset)) if args.train_n else len(tr.dataset),validation_n=len(vi),test_n=10000,
        architecture=args.arch+' CIFAR stem3x3 stride1 no maxpool',normalization=dict(mean=MEAN,std=STD) if args.dataset=='cifar10' else dict(mean=(.507,.487,.441),std=(.267,.257,.276)),
        augmentation='crop padding4 + horizontal flip'+(' + RandAugment(2,9) + Mixup(.2)/CutMix(1)' if args.recipe=='thesis' else ''),optimizer='SGD momentum0.9 weight_decay5e-4',
        amp_training=device=='cuda' and args.recipe=='basic',tf32=False,label_smoothing=.1,sam=args.recipe=='thesis',sam_rho=.05 if args.recipe=='thesis' else None,repeat_augmentation=3 if args.recipe=='thesis' else 1,
        train_examples_per_epoch=min(args.train_n,len(tr.dataset)) if args.train_n else len(tr.dataset),
        validation_split='5000 stratified from official train50k, FIXED seed2026 across training seeds',test_selection=False)
    files=[]
    data_folder=Path(args.data)/('cifar-10-batches-py' if args.dataset=='cifar10' else 'cifar-100-python')
    for p in sorted(data_folder.glob('*')):
        if p.is_file(): files.append(dict(path=portable_reference(p,out),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    config['dataset_files']=files; write_json(out/'config.json',config)
    m=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device)
    if args.resume:
        saved=torch.load(args.resume,map_location=device,weights_only=False)
        m.load_state_dict(saved['model'])
    opt=torch.optim.SGD(m.parameters(),lr=args.lr,momentum=.9,weight_decay=5e-4)
    sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,args.epochs)
    scaler=torch.amp.GradScaler(device,enabled=device=='cuda' and args.recipe=='basic'); best=-1; rows=[]; started=time.time()
    for epoch in range(args.epochs):
        m.train(); n=0; correct=0; loss_total=0; start=time.time()
        for x,y in tr:
            if args.train_n and n>=args.train_n:break
            if args.train_n:x=x[:args.train_n-n];y=y[:args.train_n-n]
            x=x.to(device,non_blocking=True); y=y.to(device,non_blocking=True)
            if args.recipe=='thesis':
                from thesis_recipe import mix_batch,sam_step
                mixed,targets=mix_batch(x,y,10 if args.dataset=='cifar10' else 100)
                loss_value,z=sam_step(m,opt,mixed,targets,rho=.05,label_smoothing=.1)
            else:
                opt.zero_grad(set_to_none=True)
                with torch.autocast(device_type=device,dtype=torch.float16,enabled=device=='cuda'):
                    z=m(x); loss=F.cross_entropy(z,y,label_smoothing=.1)
                scaler.scale(loss).backward(); scaler.step(opt); scaler.update()
                loss_value=loss.item()
            loss_total+=loss_value*len(y); correct+=(z.argmax(1)==y).sum().item(); n+=len(y)
        val,*_=evaluate(m,vl,device)
        row=dict(epoch=epoch+1,train_n=n,train_loss=loss_total/n,train_accuracy=correct*100/n,
                 validation_accuracy=val['accuracy'],learning_rate=opt.param_groups[0]['lr'],seconds=time.time()-start)
        rows.append(row); print(json.dumps(row),flush=True)
        state=dict(model=m.state_dict(),epoch=epoch+1,config=config,validation_accuracy=val['accuracy'])
        torch.save(state,out/'last.pt')
        if val['accuracy']>best:
            best=val['accuracy']; torch.save(state,out/'best.pt')
        sched.step()
        with (out/'training.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_json(out/'training_complete.json',dict(seconds=time.time()-started,best_validation_accuracy=best,epochs=args.epochs))
    print('TRAINING_COMPLETE',flush=True)

def infer(args):
    seed_all(args.seed); ieee(); device='cuda' if torch.cuda.is_available() else 'cpu'
    tr,vl,te,ti,vi=load_data(args.data,args.seed,args.batch,args.workers,args.dataset,args.recipe)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    fp=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device);fp.load_state_dict(state['model']);fp.eval()
    write_json(out/'inference_config.json',dict(checkpoint=portable_reference(args.checkpoint,out),
        checkpoint_sha256=hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest(),
        torch=torch.__version__,device=device,dataset=args.dataset,architecture=args.arch,
        split_seed=2026,training_seed=args.seed,test_n=args.test_n,calibration_n=args.calibration_n,
        product_semantics='two-complement signed Baugh-Wooley column removal for k <= bits-1',
        integer_engine='IEEE FP32 explicit unfold/GEMM bounded chunks below 2^24, INT64 chunk summation',
        tf32=False,amp_inference=False,weight_quantization='per tensor absmax',
        activation_quantization='per layer validation absmax, static, signed asymmetric integer bounds',
        bn='unfused FP32, baseline running statistics',bias='floating point added after integer accumulation'))
    amax=calibrate(fp,vl,device,args.calibration_n)
    write_json(out/'calibration.json',dict(source='validation only',n=args.calibration_n,method='maximum absolute per layer',amax=amax))
    rows=[]; baseline={}; predictions={}
    configs=[('fp32',None,'fp32',dict(all=0))]
    for bits in [6,8]:
        configs.append((f'int{bits}_k0',bits,'quant',dict(all=0)))
        for k in ([2,4,5] if bits==6 else [4,6,7]):
            configs.append((f'int{bits}_postacc_k{k}',bits,'postacc',dict(all=k)))
            configs.append((f'int{bits}_columns_k{k}',bits,'columns',dict(all=k)))
        k=bits-1
        configs.append((f'int{bits}_columns_k{k}_stem_fc_protected',bits,'columns',
                        dict(conv1=0,layer1=k,layer2=k,layer3=k,layer4=k,fc=0)))
    if args.quick: configs=configs[:2]+[c for c in configs if 'columns_k5' in c[0]]
    if args.compact:
        configs=[c for c in configs if c[0] in ['fp32','int6_k0','int6_columns_k4','int8_k0','int8_columns_k4']]
    if args.conservative:
        configs=[('fp32',None,'fp32',dict(all=0)),
                 ('int6_k0',6,'quant',dict(all=0)),('int6_columns_k1',6,'columns',dict(all=1)),
                 ('int8_k0',8,'quant',dict(all=0)),('int8_columns_k1',8,'columns',dict(all=1))]
    if args.add_int8_k1 and not any(c[0]=='int8_columns_k1' for c in configs):
        configs.append(('int8_columns_k1',8,'columns',dict(all=1)))
    for name,bits,mode,ks in configs:
        m=copy.deepcopy(fp)
        if bits: replace_quant(m,bits,mode,ks,amax)
        m.eval()
        metrics,y,p,z=evaluate(m,te,device,args.test_n)
        base_name='fp32' if bits is None else f'int{bits}_k0'
        if name==base_name: baseline[base_name]=p
        comparison=paired_metrics(y,baseline[base_name],p,args.seed)
        row=dict(name=name,bits=bits,mode=mode,stage_k=ks,**metrics,**comparison)
        rows.append(row);predictions[name]=p
        write_json(out/f'{name}_activation_clipping.json',
            {ln:dict(clipped=child.clipped,observed=child.observed,
                     percent=100*child.clipped/max(1,child.observed))
             for ln,child in m.named_modules() if isinstance(child,QuantLayer)})
        np.savez_compressed(out/f'{name}_predictions.npz',labels=y,predictions=p,logits=z)
        print(json.dumps(row),flush=True); write_json(out/'inference_results.json',rows)
        flat={k:v for k,v in row.items() if not isinstance(v,(list,dict))}
        with (out/'inference_results.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(flat));w.writeheader()
            for r in rows:w.writerow({k:r[k] for k in flat})
        del m
        if device=='cuda':torch.cuda.empty_cache()
    plot_results(out,rows,args.dataset,args.arch)

def finetune(args):
    seed_all(args.seed);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    tr,vl,te,ti,vi=load_data(args.data,args.seed,args.batch,args.workers,args.dataset,args.recipe)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    fp=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device);fp.load_state_dict(state['model'])
    amax=calibrate(fp,vl,device,args.calibration_n)
    ks=dict(conv1=0,layer1=args.k,layer2=args.k,layer3=args.k,layer4=args.k,fc=0)
    m=replace_quant(copy.deepcopy(fp),args.bits,'columns',ks,amax)
    opt=torch.optim.SGD(m.parameters(),lr=args.lr,momentum=.9,weight_decay=5e-4)
    sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,args.epochs)
    rows=[];best=-1;start_all=time.time()
    pre,*_=evaluate(m,vl,device);print('QAT_PRE_VALIDATION',json.dumps(pre),flush=True)
    for epoch in range(args.epochs):
        m.train();start=time.time();count=0;loss_total=0
        for x,y in tr:
            if args.train_n and count>=args.train_n:break
            if args.train_n:x=x[:args.train_n-count];y=y[:args.train_n-count]
            x=x.to(device);y=y.to(device)
            if args.recipe=='thesis':
                from thesis_recipe import mix_batch,sam_step
                mixed,targets=mix_batch(x,y,10 if args.dataset=='cifar10' else 100)
                loss_value,_=sam_step(m,opt,mixed,targets,rho=.05,label_smoothing=.1)
            else:
                opt.zero_grad(set_to_none=True)
                z=m(x);loss=F.cross_entropy(z,y,label_smoothing=.1);loss.backward();opt.step()
                loss_value=loss.item()
            loss_total+=loss_value*len(y);count+=len(y)
        val,*_=evaluate(m,vl,device)
        row=dict(epoch=epoch+1,train_n=count,train_loss=loss_total/count,validation_accuracy=val['accuracy'],seconds=time.time()-start)
        rows.append(row);print('QAT',json.dumps(row),flush=True)
        # Save underlying ordinary model weights, reconstruct quantization via config.
        plain=copy.deepcopy(m)
        for name,child in list(plain.named_modules()):
            if isinstance(child,QuantLayer):
                parent=plain;path=name.split('.')
                for part in path[:-1]:parent=getattr(parent,part)
                setattr(parent,path[-1],child.base)
        payload=dict(model=plain.state_dict(),epoch=epoch+1,amax=amax,bits=args.bits,stage_k=ks,
                     mode='columns',ste='ordinary floating point dot backward; bit accurate forward',
                     validation_accuracy=val['accuracy'],train_n_per_epoch=count,seed=args.seed,
                     dataset=args.dataset,arch=args.arch,recipe=args.recipe,learning_rate=args.lr)
        torch.save(payload,out/'last_qat.pt')
        if val['accuracy']>best:best=val['accuracy'];torch.save(payload,out/'best_qat.pt')
        write_json(out/'qat_training.json',rows)
        if args.recipe=='thesis':sched.step()
    best_state=torch.load(out/'best_qat.pt',map_location=device,weights_only=False)
    best_model=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device);best_model.load_state_dict(best_state['model'])
    replace_quant(best_model,args.bits,'columns',ks,amax)
    post,y,p,z=evaluate(best_model,te,device)
    before_model=replace_quant(copy.deepcopy(fp),args.bits,'columns',ks,amax)
    before,_,bp,_=evaluate(before_model,te,device)
    post.update(paired_metrics(y,bp,p,args.seed));post.update(bits=args.bits,stage_k=ks,mode='columns',
        epochs=args.epochs,train_n_per_epoch=rows[0]['train_n'],total_seconds=time.time()-start_all)
    write_json(out/'qat_test_results.json',dict(before=before,after=post))
    np.savez_compressed(out/'qat_test_predictions.npz',labels=y,before_predictions=bp,predictions=p,logits=z)
    print('QAT_TEST',json.dumps(dict(before=before,after=post)),flush=True)

def bnadapt(args):
    """Control experiment: update BN statistics using train images, no gradients."""
    if args.train_n<=0:raise ValueError('bnadapt requires --train-n > 0')
    seed_all(args.seed);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    tr,vl,te,ti,vi=load_data(args.data,args.seed,args.batch,args.workers,args.dataset)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    fp=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device);fp.load_state_dict(state['model'])
    amax=calibrate(fp,vl,device,args.calibration_n)
    ks=dict(conv1=0,layer1=args.k,layer2=args.k,layer3=args.k,layer4=args.k,fc=0)
    m=replace_quant(fp,args.bits,'columns',ks,amax)
    before,y,bp,_=evaluate(m,te,device)
    m.train()
    for module in m.modules():
        if isinstance(module,nn.BatchNorm2d):
            module.reset_running_stats();module.momentum=None
    count=0;start=time.time()
    with torch.no_grad():
        for x,labels_unused in tr:
            if count>=args.train_n:break
            x=x[:args.train_n-count].to(device);m(x);count+=len(x)
    after,_,p,z=evaluate(m,te,device)
    after.update(paired_metrics(y,bp,p,args.seed))
    report=dict(before=before,after=after,training_images_for_bn=count,gradient_updates=0,
                bits=args.bits,stage_k=ks,seconds=time.time()-start,
                selection='BN sample count and k chosen before test evaluation')
    write_json(out/'bn_adaptation_results.json',report)
    np.savez_compressed(out/'bn_adaptation_predictions.npz',labels=y,before_predictions=bp,predictions=p,logits=z)
    print('BN_ADAPTATION',json.dumps(report),flush=True)

def qat_eval(args):
    """Evaluate a saved QAT model with its original fixed scales and PP schedule."""
    seed_all(args.seed);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    dataset=state.get('dataset',args.dataset);arch=state.get('arch',args.arch)
    _,_,te,_,_=load_data(args.data,args.seed,args.batch,args.workers,dataset)
    m=make_model(10 if dataset=='cifar10' else 100,arch).to(device);m.load_state_dict(state['model'])
    replace_quant(m,state['bits'],state['mode'],state['stage_k'],state['amax'])
    metrics,y,p,z=evaluate(m,te,device,args.test_n)
    metrics.update(checkpoint=portable_reference(args.checkpoint,args.out),dataset=dataset,arch=arch,
                   checkpoint_sha256=hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest(),
                   activation_maxima_sha256=hashlib.sha256(json.dumps(state['amax'],sort_keys=True).encode()).hexdigest(),
                   bits=state['bits'],stage_k=state['stage_k'],mode=state['mode'],
                   workers=args.workers,batch=args.batch)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    write_json(out/'qat_inference.json',metrics)
    np.savez_compressed(out/'qat_inference_predictions.npz',labels=y,predictions=p,logits=z)
    print('SAVED_QAT_INFERENCE',json.dumps(metrics),flush=True)

def biascomp(args):
    """Independent variant: static expected-PP-error offsets from validation only.

    Every multiplier still implements uncorrected PP column removal. Learned
    INTEGER offsets initialize the accumulator; these are additional hardware
    work/storage whose circuit power has not been measured.
    """
    if not 1<=args.k<args.bits:raise ValueError('biascomp requires 1 <= k < bits')
    seed_all(args.seed);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    _,vl,te,_,_=load_data(args.data,args.seed,args.batch,args.workers,args.dataset)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    fp=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device);fp.load_state_dict(state['model'])
    amax=calibrate(fp,vl,device,args.calibration_n)
    q=replace_quant(fp,args.bits,'quant',dict(all=0),amax)
    ks=dict(conv1=0,layer1=args.k,layer2=args.k,layer3=args.k,layer4=args.k,fc=0)
    statistics={};hooks=[]
    for name,layer in q.named_modules():
        if isinstance(layer,QuantLayer) and name.split('.')[0] not in ('conv1','fc'):
            def hook(module,inputs,name=name):
                x=inputs[0];qi=(x.detach().float()/(max(module.activation_max,1e-8)/module.qmax)).round().clamp(module.qmin,module.qmax).to(torch.int32)
                dims=(0,2,3) if qi.ndim==4 else (0,)
                vals=torch.stack([((qi>>i)&1).sum(dims).double() for i in range(args.k)])
                count=x.shape[0]*(x.shape[2]*x.shape[3] if x.ndim==4 else 1)
                if name not in statistics:statistics[name]=dict(total=vals,count=count,input_shape=list(x.shape[1:]))
                else:statistics[name]['total']+=vals;statistics[name]['count']+=count
            hooks.append(layer.register_forward_pre_hook(hook))
    evaluate(q,vl,device,args.calibration_n)
    for h in hooks:h.remove()
    saved={};detail={};extra_adds=0;compressed_codes=0
    for name,layer in q.named_modules():
        if not isinstance(layer,QuantLayer):continue
        layer.mode='columns';layer.k=ks[name.split('.')[0]]
        if not layer.k:continue
        stat=statistics[name];prob=(stat['total']/stat['count']).float()
        wi=(layer.base.weight.detach().float()/(layer.base.weight.detach().abs().max().clamp_min(1e-8)/layer.qmax)).round().clamp(layer.qmin,layer.qmax).to(torch.int32)
        shape=stat['input_shape'];expect=None
        for i in range(args.k):
            if len(shape)==3:
                plane=prob[i].view(1,-1,1,1).expand(1,*shape)
                part=F.conv2d(plane,(wi&((1<<(args.k-i))-1)).float(),None,
                             layer.base.stride,layer.base.padding,layer.base.dilation)
            else:
                part=F.linear(prob[i].view(1,-1),(wi&((1<<(args.k-i))-1)).float())
            part=part*(1<<i);expect=part if expect is None else expect+part
        codes=expect.round().to(torch.int64);layer.bias_codes=codes
        saved[name]=codes.cpu();extra_adds+=codes.numel()
        compressed=sum(len(np.unique(ch)) for ch in codes[0].cpu().numpy())
        compressed_codes+=compressed
        detail[name]=dict(input_bit_probabilities=prob.cpu().tolist(),offset_shape=list(codes.shape),
                         minimum_offset=int(codes.min()),maximum_offset=int(codes.max()),
                         int32_storage_bytes=codes.numel()*4,padding_class_unique_codes=compressed)
    metrics,y,p,z=evaluate(q,te,device,args.test_n)
    baseline_path=Path(args.checkpoint).parent/'int6_k0_predictions.npz'
    if args.bits==8:baseline_path=Path(args.checkpoint).parent/'int8_k0_predictions.npz'
    if baseline_path.exists():
        original=np.load(baseline_path);assert np.array_equal(y,original['labels'])
        metrics.update(paired_metrics(y,original['predictions'],p,args.seed))
    report=dict(test=metrics,bits=args.bits,stage_k=ks,calibration_samples=args.calibration_n,
                source_checkpoint=portable_reference(args.checkpoint,out),
                source_checkpoint_relative=portable_reference(args.checkpoint,out),
                source_checkpoint_sha256=hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest(),
                paired_baseline_predictions=portable_reference(baseline_path,out) if baseline_path.exists() else None,
                calibration_source=f'fixed first {args.calibration_n} training-derived validation images, no test labels',
                method='per-channel input-bit means; padding-aware expected removed PP sums rounded to INTEGER accumulator offsets',
                gradient_updates=0,bn='original frozen statistics',extra_additions_per_image=extra_adds,
                full_offset_map_storage_int32_bytes=extra_adds*4,
                compressed_boundary_class_unique_offsets_int32_bytes=compressed_codes*4,
                compressed_storage_note='Offset codes only: lower bound excludes lookup indices, addresses, and controller state',
                offset_power_measured=False,original_thesis_method=False,layer_details=detail)
    write_json(out/'bias_compensation_results.json',report)
    np.savez_compressed(out/'bias_compensation_predictions.npz',labels=y,predictions=p,logits=z)
    torch.save(dict(bias_codes=saved,amax=amax,bits=args.bits,stage_k=ks,mode='columns',dataset=args.dataset,
                    arch=args.arch,source_checkpoint_sha256=hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest()),out/'bias_offsets.pt')
    print('INDEPENDENT_BIAS_COMPENSATION',json.dumps({k:v for k,v in report.items() if k!='layer_details'}),flush=True)

def bias_eval(args):
    seed_all(args.seed);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    saved=torch.load(args.bias_file,map_location=device,weights_only=False)
    if hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest()!=saved['source_checkpoint_sha256']:
        raise ValueError('Bias offsets require the exact source checkpoint')
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    _,_,te,_,_=load_data(args.data,args.seed,args.batch,args.workers,saved['dataset'])
    m=make_model(10 if saved['dataset']=='cifar10' else 100,saved['arch']).to(device);m.load_state_dict(state['model'])
    replace_quant(m,saved['bits'],saved['mode'],saved['stage_k'],saved['amax'])
    for name,layer in m.named_modules():
        if isinstance(layer,QuantLayer) and name in saved['bias_codes'] and not args.disable_bias:layer.bias_codes=saved['bias_codes'][name]
    metrics,y,p,z=evaluate(m,te,device,args.test_n)
    metrics.update(bits=saved['bits'],mode=saved['mode'],stage_k=saved['stage_k'],offsets_applied=not args.disable_bias,
                   checkpoint_sha256=saved['source_checkpoint_sha256'],activation_maxima_sha256=hashlib.sha256(json.dumps(saved['amax'],sort_keys=True).encode()).hexdigest())
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    prefix='uncorrected_same_schedule' if args.disable_bias else 'bias_saved_inference'
    write_json(out/f'{prefix}.json',metrics)
    np.savez_compressed(out/f'{prefix}_predictions.npz',labels=y,predictions=p,logits=z)
    if args.disable_bias and (out/'bias_compensation_predictions.npz').exists():
        compensated=np.load(out/'bias_compensation_predictions.npz');assert np.array_equal(y,compensated['labels'])
        comparison=paired_metrics(y,p,compensated['predictions'],args.seed)
        report_path=out/'bias_compensation_results.json';report=json.loads(report_path.read_text(encoding='utf8'))
        report.update(uncorrected_same_schedule=metrics,paired_compensation_vs_uncorrected=comparison)
        write_json(report_path,report)
        print('MATCHED_BIAS_CONTROL',json.dumps(dict(uncorrected=metrics,compensation_vs_uncorrected=comparison)),flush=True)
    print('SAVED_BIAS_INFERENCE',json.dumps(metrics),flush=True)

def export_stimulus(args):
    """Twelve consecutive real operands from the fixed validation center patch."""
    if args.bits!=8 or args.k!=1:raise ValueError('Exported trace protocol requires INT8 k1')
    seed_all(args.seed);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    _,vl,_,_,vi=load_data(args.data,args.seed,args.batch,args.workers,args.dataset)
    state=torch.load(args.checkpoint,map_location=device,weights_only=False)
    m=make_model(10 if args.dataset=='cifar10' else 100,args.arch).to(device);m.load_state_dict(state['model'])
    amax=calibrate(m,vl,device,args.calibration_n)
    replace_quant(m,args.bits,'columns',dict(all=args.k),amax)
    name='layer1.0.conv1';layer=dict(m.named_modules())[name];captured={}
    def hook(module,inputs):captured['x']=inputs[0].detach().clone()
    h=layer.register_forward_pre_hook(hook);evaluate(m,vl,device,max_samples=1);h.remove()
    sx=max(layer.activation_max,1e-8)/layer.qmax
    sw=float(layer.base.weight.detach().abs().max().clamp_min(1e-8).item()/layer.qmax)
    xi=(captured['x'].float()/sx).round().clamp(layer.qmin,layer.qmax).to(torch.int64).cpu().numpy()
    wi=(layer.base.weight.detach().float()/sw).round().clamp(layer.qmin,layer.qmax).to(torch.int64).cpu().numpy()
    rows=[];acc0=0;acc1=0;cy=xi.shape[2]//2;cx=xi.shape[3]//2
    for j in range(12):
        channel=j//9;kr=(j%9)//3;kc=j%3
        a=int(xi[0,channel,cy+kr-1,cx+kc-1]);b=int(wi[0,channel,kr,kc])
        p0=a*b;p1=p0-((a&1)*(b&1));acc0+=p0;acc1+=p1
        rows.append(dict(index=j,a=a,b=b,validation_ordinal=0,official_train_index=int(vi[0]),
            output_channel=0,input_channel=channel,output_y=cy,output_x=cx,kernel_y=kr,kernel_x=kc,
            product_k0=p0,product_k1=p1,partial_accumulator_k0=acc0,partial_accumulator_k1=acc1))
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    with (out/'cnn_int8_pairs.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_json(out/'cnn_int8_trace_provenance.json',dict(dataset=args.dataset,layer=name,source='first fixed validation image',
        official_train_index=int(vi[0]),captured_from_model=dict(bits=args.bits,mode='columns',uniform_k=args.k),
        selection='first12 consecutive channel/kernel operands for output_channel0 and center output; no selection by activity/label',
        activation_scale=sx,weight_scale=sw,activation_max=layer.activation_max,
        checkpoint=portable_reference(args.checkpoint,out),checkpoint_sha256=hashlib.sha256(Path(args.checkpoint).read_bytes()).hexdigest(),
        checkpoint_relative_to_provenance=portable_reference(args.checkpoint,out),
        calibration_source=f'first {args.calibration_n} validation images',samples=12,activation_signed=True,weight_signed=True,
        accumulation='partial first12 of576 MAC terms, zero initial accumulator',
        limitations='One patch trace; no estimate of full neural network energy or confidence in process power'))
    print('CNN_OPERAND_TRACE',str(out/'cnn_int8_pairs.csv'),flush=True)

def plot_results(out,rows,dataset='cifar10',arch='resnet18'):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(11,6)); names=[r['name'] for r in rows]
    ax.barh(names,[r['accuracy'] for r in rows],color=['#3b82f6' if r['mode']!='columns' else '#ef774d' for r in rows])
    ax.set_xlabel(f'{dataset.upper()} test top-1 accuracy (%)');ax.set_xlim(0,100);ax.invert_yaxis()
    ax.set_title(f'Independent {arch}: quantization vs arithmetic semantics')
    fig.tight_layout();fig.savefig(out/'accuracy_comparison.png',dpi=180);plt.close(fig)

def microtests(args):
    seed_all(2026);ieee();device='cuda' if torch.cuda.is_available() else 'cpu'
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('arithmetic',HERE.parent/'circuit'/'arithmetic.py');ar=module_from_spec(spec);spec.loader.exec_module(ar)
    rows=[];rng=np.random.default_rng(2026)
    for bits in (6,8):
        for k in range(bits):
            a=rng.integers(-(1<<(bits-1)),1<<(bits-1),size=(2,7,5,5),dtype=np.int64)
            b=rng.integers(-(1<<(bits-1)),1<<(bits-1),size=(4,7,3,3),dtype=np.int64)
            xt=torch.tensor(a,dtype=torch.float32,device=device);wt=torch.tensor(b,dtype=torch.float32,device=device)
            y=quantized_conv(xt,wt,(1,1),(1,1),(1,1),k,'columns').cpu().numpy()
            ap=np.pad(a,((0,0),(0,0),(1,1),(1,1)));ref=np.zeros_like(y)
            for ni in range(2):
                for co in range(4):
                    for h in range(5):
                        for ww in range(5):
                            ref[ni,co,h,ww]=ar.column_mask_mul(ap[ni,:,h:h+3,ww:ww+3],b[co],bits,k).sum()
            assert np.array_equal(y,ref),(bits,k,np.abs(y-ref).max())
            rows.append(dict(bits=bits,k=k,outputs=y.size,max_absolute_error=int(np.abs(y-ref).max())))
    # Deliberately exceeds 2**24: validates channel-chunk INT64 accumulation.
    xt=torch.full((1,512,3,3),127.,device=device);wt=torch.full((1,512,3,3),127.,device=device)
    test=quantized_conv(xt,wt,(1,1),(0,0),(1,1),0,'columns');expected=512*9*127*127
    assert test.item()==expected
    xt_min=torch.full((1,512,3,3),-128.,device=device);wt_min=torch.full((1,512,3,3),-128.,device=device)
    test_min=quantized_conv(xt_min,wt_min,(1,1),(0,0),(1,1),0,'columns');expected_min=512*9*128*128
    assert test_min.item()==expected_min
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    write_json(out/'arithmetic_tests.json',dict(conv_microtests=rows,large_dot_expected=expected,
        large_dot_actual=test.item(),signed_minimum_dot_expected=expected_min,signed_minimum_dot_actual=test_min.item(),device=device,tf32=False,passed=True))
    print('ARITHMETIC_TESTS_PASS',flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['train','infer','finetune','qat_eval','bnadapt','biascomp','bias_eval','export_stimulus','microtests'])
    p.add_argument('--data',default='data');p.add_argument('--out',default='results/run_seed2026')
    p.add_argument('--seed',type=int,default=2026);p.add_argument('--batch',type=int,default=128)
    p.add_argument('--dataset',choices=['cifar10','cifar100'],default='cifar10')
    p.add_argument('--arch',choices=['resnet18','resnet50'],default='resnet18')
    p.add_argument('--recipe',choices=['basic','thesis'],default='basic')
    p.add_argument('--workers',type=int,default=0);p.add_argument('--epochs',type=int,default=30)
    p.add_argument('--lr',type=float,default=.1);p.add_argument('--resume',help='Weights-only warm start; optimizer/schedule reset');p.add_argument('--checkpoint')
    p.add_argument('--calibration-n',type=int,default=1024);p.add_argument('--test-n',type=int,default=10000)
    p.add_argument('--train-n',type=int,default=0);p.add_argument('--bits',type=int,choices=[6,8],default=6)
    p.add_argument('--k',type=int,default=2);p.add_argument('--quick',action='store_true')
    p.add_argument('--compact',action='store_true')
    p.add_argument('--conservative',action='store_true')
    p.add_argument('--add-int8-k1',action='store_true')
    p.add_argument('--bias-file')
    p.add_argument('--disable-bias',action='store_true')
    args=p.parse_args()
    needs_checkpoint={'infer','finetune','qat_eval','bnadapt','biascomp','bias_eval','export_stimulus'}
    if args.command in needs_checkpoint and not args.checkpoint:p.error('--checkpoint is required for this command')
    if args.command=='bias_eval' and not args.bias_file:p.error('--bias-file is required for bias_eval')
    if min(args.batch,args.epochs,args.test_n,args.calibration_n)<=0:p.error('batch, epochs, test-n and calibration-n must be positive')
    if args.workers<0 or args.train_n<0:p.error('workers and train-n must be nonnegative')
    globals()[args.command](args)

if __name__=='__main__':main()

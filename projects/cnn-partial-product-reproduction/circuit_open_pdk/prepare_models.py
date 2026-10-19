"""Prepare geometry bins from a user-provided SKY130 checkout; never download models.

Vendor model content is generated only outside this source checkout. The source
repository contains this selection code and provenance URLs, not PDK model cards.
"""
from pathlib import Path
import argparse,hashlib,json,re,shutil

HERE=Path(__file__).resolve().parent
REFERENCE_REPOSITORY='https://github.com/google/skywater-pdk-libs-sky130_fd_pr'
REFERENCE_COMMIT='f62031a1be9aefe902d6d54cddd6f59b57627436'


def prepare(model_root,output_dir):
    model_root=Path(model_root).expanduser().resolve()
    output_dir=Path(output_dir).expanduser().resolve()
    if output_dir.is_relative_to(HERE.parent):
        raise ValueError('Prepared vendor models must be stored outside the public source checkout')
    lod=next((p for p in [model_root/'models/parameters/lod.spice',model_root/'parameters/lod.spice'] if p.is_file()),None)
    if lod is None:raise FileNotFoundError('Expected models/parameters/lod.spice or parameters/lod.spice beneath --model-root')
    source_files=[lod]
    for device in ('nfet_01v8','pfet_01v8'):
        for suffix in ('tt.pm3.spice','tt.corner.spice','mismatch.corner.spice'):
            path=model_root/'cells'/device/f'sky130_fd_pr__{device}__{suffix}'
            if not path.is_file():raise FileNotFoundError('Missing SKY130 source file: '+str(path.relative_to(model_root)))
            source_files.append(path)
    if output_dir==model_root or model_root.is_relative_to(output_dir):
        raise ValueError('Output directory must be separate from the input model root')
    output_dir.mkdir(parents=True,exist_ok=True);reduced=output_dir/'reduced';reduced.mkdir(exist_ok=True)
    (output_dir/'parameters').mkdir(exist_ok=True);shutil.copyfile(lod,output_dir/'parameters/lod.spice')
    records=[]
    for device,widths in [('nfet_01v8',[.42,.84,1.26]),('pfet_01v8',[1.26])]:
        official=model_root/'cells'/device
        text=(official/f'sky130_fd_pr__{device}__tt.pm3.spice').read_text()
        positions=list(re.finditer(r'^\.model\s+([^\s]+).*$',text,re.M))
        if not positions:raise ValueError('No binned .model statements for '+device)
        prefix=text[:positions[0].start()];kept=[];found=set()
        for index,pos in enumerate(positions):
            stop=positions[index+1].start() if index+1<len(positions) else text.index('.ends',pos.start())
            block=text[pos.start():stop]
            match=re.search(r'lmin\s*=\s*(\S+)\s+lmax\s*=\s*(\S+)\s+wmin\s*=\s*(\S+)\s+wmax\s*=\s*(\S+)',block)
            if not match:raise ValueError('No geometry bounds '+pos.group(1))
            lmin,lmax,wmin,wmax=map(float,match.groups())
            matching=[w for w in widths if lmin-1e-15<=.15e-6<=lmax+1e-15 and wmin-1e-15<=w*1e-6<=wmax+1e-15]
            if matching:
                kept.append(block);found.update(matching)
                records.append({'device':device,'model':pos.group(1),'widths_um':matching,'length_um':.15,'original_block_sha256':hashlib.sha256(block.encode()).hexdigest(),'parameters_changed':False})
        if found!=set(widths):raise ValueError('Input model lacks a required W/L bin for '+device)
        (reduced/f'{device}_selected.spice').write_text(prefix+''.join(kept)+f'.ends sky130_fd_pr__{device}\n',encoding='ascii')
        corner=(official/f'sky130_fd_pr__{device}__tt.corner.spice').read_text().replace(f'sky130_fd_pr__{device}__tt.pm3.spice',f'{device}_selected.spice')
        (reduced/f'{device}_corner.spice').write_text(corner,encoding='ascii')
        shutil.copyfile(official/f'sky130_fd_pr__{device}__mismatch.corner.spice',reduced/f'{device}_mismatch.spice')
    wrapper='* User-local official TT geometry subset. Numerical coefficients unchanged.\n.include "parameters/lod.spice"\n'
    for device in ('nfet_01v8','pfet_01v8'):
        wrapper+=f'.include "reduced/{device}_corner.spice"\n.include "reduced/{device}_mismatch.spice"\n'
    wrapper_path=output_dir/'sky130_tt_reduced.spice';wrapper_path.write_text(wrapper,encoding='ascii')
    provenance={'reference_repository':REFERENCE_REPOSITORY,'reference_commit':REFERENCE_COMMIT,'reference_commit_verification':'Reference only; this command does not assume the user checkout matches that commit. Actual input hashes follow.','source_files':[{'file':str(p.relative_to(model_root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in source_files],'geometry_bins':records,'model_coefficients_changed':False,'license':'Read and preserve the license from your externally acquired SKY130 source checkout; no vendor license or model content is distributed with this code.'}
    (output_dir/'model_provenance.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
    return wrapper_path,provenance


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model-root',type=Path,required=True,help='Existing official primitive repository or extracted models root')
    p.add_argument('--output-dir',type=Path,required=True,help='Private local destination outside the source checkout')
    args=p.parse_args();wrapper,provenance=prepare(args.model_root,args.output_dir)
    print(json.dumps({'selected_bins':len(provenance['geometry_bins']),'wrapper_filename':wrapper.name,'status':'prepared_not_simulated'}))
if __name__=='__main__':main()

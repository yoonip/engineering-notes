"""과거 checkpoint의 알려진 정규화 설명 오기를 실제 옵션과 맞춘다."""


def canonical_config(config: dict) -> tuple[dict, list[dict]]:
    """계산 옵션은 유지하고 두 종류의 알려진 사람용 설명 문자열만 정정한다.

    normalization을 통째로 삭제해서 다른 epsilon/순서의 모델을 같다고
    취급하지 않는다. 모르는 문자열은 그대로 둬 엄격한 비교가 실패하게 한다.
    원본 파일과 가중치를 바꾸지 않으며 수정 목록을 보고서에 보존한다.
    """
    copy = dict(config)
    prefix = 'post-residual LayerNorm, epsilon=1/256, '
    allowed = (prefix+'no learned affine parameters', prefix+'learned gamma/beta affine parameters')
    changes = []
    before = copy.get('normalization')
    affine = copy.get('layernorm_affine',False)
    if before in allowed and isinstance(affine,bool):
        after = allowed[1 if affine else 0]
        if after != before:
            copy['normalization'] = after
            changes.append({'field':'normalization','before':before,'after':after,
                            'reason_ko':'실제 layernorm_affine boolean과 설명 문자열을 일치시켰다. 가중치/계산은 동일하다.'})
    return copy, changes

"""SDF 검사 프로필의 고정 정책과 결과 폴더를 정의한다.

이 모듈은 파일을 읽거나 도구를 실행하지 않는다. UART/SDF 성공을 만들지
않으며, 현재 선택할 프로필을 결정하지도 않는다. 검증기는 이 계약을 통과한
설정과 실제 로그·SHA·프레임을 별도로 확인해야 한다.

Transport0는 기존 기본 검사의 0/0/0/0/O2 조건이다. UG900의 reject 0
권고에 해당하는 것은 두 reject 값이며, error 0은 이 프로젝트의 명시적
추가 설정이다. Inertial100은 네 pulse 값을 100으로 고정한 추가 실험이다.
이 추가 조건의 성공을 기본 Transport0 성공으로 바꾸어 해석하지 않는다.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import MappingProxyType


POLICY_FIELDS = (
    'pulse_r_percent', 'pulse_int_r_percent', 'pulse_e_percent',
    'pulse_int_e_percent', 'optimization_level',
)
PROFILE_NAMES = ('Transport0', 'Inertial100')
PROFILE_POLICIES = MappingProxyType({
    'Transport0': MappingProxyType(dict(zip(POLICY_FIELDS, (0, 0, 0, 0, 2)))),
    'Inertial100': MappingProxyType(dict(zip(POLICY_FIELDS, (100, 100, 100, 100, 2)))),
})
PROFILE_DESCRIPTIONS = MappingProxyType({
    'Transport0': MappingProxyType({
        'kind_ko': '기본 엄격 검사',
        'additional_profile': False,
        'reject_matches_ug900_recommendation': True,
        'description_ko': '경로·배선 reject/error를 모두 0, simulator 최적화를 O2로 고정한다. '
                          'UG900의 reject 0 권고는 두 reject 설정을 가리킨다. '
                          'error 0은 이 프로젝트의 명시적 설정이며, 실제 UART 성공은 별도 원문으로 검사한다.',
    }),
    'Inertial100': MappingProxyType({
        'kind_ko': '추가 짧은 펄스 필터 조건 검사',
        'additional_profile': True,
        'reject_matches_ug900_recommendation': False,
        'description_ko': '경로·배선 reject/error를 모두 100, simulator 최적화를 O2로 고정한 추가 실험이다. '
                          '짧은 펄스 처리 정책이 다르므로 이 조건의 성공이 기본 Transport0 성공을 대신하지 않는다. '
                          'timing check·specify·SDF 지연 활성과 실제 UART 성공은 별도로 검사한다.',
    }),
})
FIXED_COMBINATIONS = ((8, 'slow', 'max'), (8, 'fast', 'min'),
                      (32, 'slow', 'max'), (32, 'fast', 'min'))
_PULSE_FLAGS = MappingProxyType({
    '--pulse_r': 'pulse_r_percent',
    '--pulse_int_r': 'pulse_int_r_percent',
    '--pulse_e': 'pulse_e_percent',
    '--pulse_int_e': 'pulse_int_e_percent',
})


def get_profile_policy(profile: str) -> dict[str, int]:
    """알려진 프로필의 다섯 값을 새 사본으로 반환한다. 원 계약은 불변이다."""
    if not isinstance(profile, str) or profile not in PROFILE_POLICIES:
        raise ValueError('알려지지 않은 SDF 검사 프로필입니다: ' + repr(profile))
    return dict(PROFILE_POLICIES[profile])


def get_profile_description(profile: str) -> dict:
    """기본 권고 범위와 추가 조건의 한글 설명을 분리해 반환한다."""
    get_profile_policy(profile)
    return dict(PROFILE_DESCRIPTIONS[profile])


def fixed_result_folder(profile: str, context: int, corner: str, delay: str) -> str:
    """프로젝트 상대경로 한 개를 반환한다. 최신 폴더 자동 탐색은 하지 않는다."""
    get_profile_policy(profile)
    if type(context) is not int or (context, corner, delay) not in FIXED_COMBINATIONS:
        raise ValueError('허용된 조합은 문맥 8/32의 slow/max 또는 fast/min입니다: '
                         + repr((context, corner, delay)))
    marker = '' if profile == 'Transport0' else '_inertial100'
    return f'build/nexys4_ddr/timing_netlist{context}{marker}_{corner}_{delay}'


def fixed_cases(profile: str) -> list[dict]:
    """네 결과의 고정 조건을 반환한다. 이것은 실행/성공 판정 목록이 아니다."""
    policy = get_profile_policy(profile)
    return [dict(context=context, corner=corner, delay=delay,
                 folder=fixed_result_folder(profile, context, corner, delay),
                 policy=dict(policy)) for context, corner, delay in FIXED_COMBINATIONS]


def require_exact_policy(actual: Mapping, profile: str) -> dict[str, int]:
    """추출한 정책 dict에 다섯 필드만 존재하고 타입·값까지 같아야 한다.

    Python의 False==0, True==1 비교 때문에 bool을 정수 정책으로 받아들이지
    않도록 type(value) is int를 사용한다. 전체 report에서는 아래 별도 함수로
    다섯 필드를 추출한다. 누락 값을 임의 기본값으로 채우지 않는다.
    """
    wanted = get_profile_policy(profile)
    if not isinstance(actual, Mapping) or set(actual) != set(POLICY_FIELDS):
        raise ValueError('실제 정책에는 다섯 필드가 빠짐없이 한 번씩 있어야 합니다.')
    if any(type(actual[field]) is not int or actual[field] != wanted[field]
           for field in POLICY_FIELDS):
        raise ValueError('실제 정책이 고정 프로필과 다릅니다: ' + profile)
    return dict(wanted)


def require_metadata_policy(metadata: Mapping, profile: str) -> dict[str, int]:
    """result/manifest 등에서 다섯 정책값을 추출한다. UART PASS는 검사하지 않는다."""
    get_profile_policy(profile)
    if not isinstance(metadata, Mapping) or any(field not in metadata for field in POLICY_FIELDS):
        raise ValueError('metadata에 다섯 정책 필드가 모두 필요합니다.')
    return require_exact_policy({field: metadata[field] for field in POLICY_FIELDS}, profile)


def parse_actual_command_policy(tokens: Sequence[str]) -> dict[str, int]:
    """xelab argv 또는 실제 Compile_Options를 나눈 token에서 명시한 값을 읽는다.

    실제 생성 옵션도 네 pulse flag와 --O2가 정확히 한 번씩 있어야 한다.
    100의 문서상 기본값을 추론하거나 0/100 혼합·O3를 허용하지 않는다.
    이 순수 parser는 명령을 실행하지 않으며 도구의 timing 활성 검사 전체를
    대체하지 않는다. --notimingchecks/--nospecify는 이 계약에서도 거부한다.
    """
    if isinstance(tokens, (str, bytes)) or not isinstance(tokens, Sequence) or any(
            not isinstance(token, str) for token in tokens):
        raise ValueError('실제 명령은 문자열 token 목록이어야 합니다.')
    if any(token in ('--notimingchecks', '--nospecify') for token in tokens):
        raise ValueError('타이밍 검사나 specify를 비활성화한 명령은 허용하지 않습니다.')
    levels = [token for token in tokens if token.startswith('--O')]
    if levels != ['--O2']:
        raise ValueError('실제 명령에 유일한 --O2가 명시되어야 합니다.')
    actual = {'optimization_level': 2}
    for flag, field in _PULSE_FLAGS.items():
        if any(token.startswith(flag) and token != flag for token in tokens):
            raise ValueError('실제 옵션은 flag와 값을 분리한 유일한 형식이어야 합니다: ' + flag)
        positions = [index for index, token in enumerate(tokens) if token == flag]
        if len(positions) != 1 or positions[0] + 1 >= len(tokens):
            raise ValueError('실제 명령의 옵션이 없거나 중복됐습니다: ' + flag)
        value = tokens[positions[0] + 1]
        if value not in ('0', '100'):
            raise ValueError('실제 명령의 정책은 명시적 0 또는 100이어야 합니다: ' + flag)
        actual[field] = int(value)
    if len({actual[field] for field in POLICY_FIELDS if field != 'optimization_level'}) != 1:
        raise ValueError('0/100을 섞은 pulse 정책은 어느 고정 프로필에도 해당하지 않습니다.')
    return {field: actual[field] for field in POLICY_FIELDS}


def require_command_policy(tokens: Sequence[str], profile: str) -> dict[str, int]:
    """실제 명령의 명시된 다섯 설정을 지정한 프로필과 정확히 비교한다."""
    get_profile_policy(profile)
    return require_exact_policy(parse_actual_command_policy(tokens), profile)

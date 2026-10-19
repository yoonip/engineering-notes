"""설명 오기만 정정하고 의미 있는 모델 설정 차이는 보존하는지 검증한다."""
import unittest
from model.config_metadata import canonical_config


class MetadataTests(unittest.TestCase):
    def test_known_affine_label_is_fixed_without_mutating_source(self):
        source = {'layernorm_affine':True,'normalization':'post-residual LayerNorm, epsilon=1/256, no learned affine parameters','d_model':16}
        result, changes = canonical_config(source)
        self.assertIn('learned gamma/beta',result['normalization'])
        self.assertEqual(len(changes),1)
        self.assertIn('no learned',source['normalization'])
        self.assertEqual(result['d_model'],16)

    def test_different_epsilon_is_not_rewritten(self):
        source = {'layernorm_affine':True,'normalization':'post-residual LayerNorm, epsilon=1/1024, no learned affine parameters'}
        result, changes = canonical_config(source)
        self.assertEqual(result,source)
        self.assertEqual(changes,[])

    def test_pre_norm_is_not_rewritten(self):
        source = {'layernorm_affine':True,'normalization':'pre-residual LayerNorm'}
        self.assertEqual(canonical_config(source),(source,[]))

    def test_non_boolean_affine_is_not_assumed_true(self):
        source = {'layernorm_affine':'False','normalization':'post-residual LayerNorm, epsilon=1/256, learned gamma/beta affine parameters'}
        self.assertEqual(canonical_config(source),(source,[]))


if __name__=='__main__':
    unittest.main()

import unittest
import torch
from model import BrailleTransformer, ModelConfig, Vocabulary, PairDataset, collate_pairs, BOS, EOS, UNK
from inference import normalize_braille_input
from evaluate import edit_distance

class CoreTests(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1)
        torch.manual_seed(7)
        self.rows = [{"braille":"⠁⠃", "korean":"가나"}, {"braille":"⠉", "korean":"각"}]
        self.vocab = Vocabulary.from_training_rows(self.rows)

    def test_nfd_roundtrip_and_unknown(self):
        self.assertEqual(self.vocab.decode_target(self.vocab.encode_target("가나")), "가나")
        self.assertIn(UNK, self.vocab.encode_target("힣"))
        self.assertEqual(self.vocab.decode_target([BOS, UNK, EOS]), "�")

    def test_input_validation(self):
        text,warnings = normalize_braille_input("⠁\r\n⠃")
        self.assertEqual(text,"⠁ ⠃")
        self.assertTrue(warnings)
        for text in ["", " ", "hello", "⣿"]:
            with self.assertRaises(ValueError): normalize_braille_input(text)

    def test_length_policy(self):
        with self.assertRaises(ValueError): PairDataset(self.rows,self.vocab,3,10)
        data=PairDataset(self.rows,self.vocab,3,10,"filter")
        self.assertEqual(len(data),1)

    def test_forward_backward_and_causality(self):
        cfg=ModelConfig(len(self.vocab.source_tokens),len(self.vocab.target_tokens),d_model=16,heads=2,encoder_layers=1,decoder_layers=1,ffn_dim=32,dropout=0,max_source_length=16,max_target_length=16)
        model=BrailleTransformer(cfg).eval()
        batch=collate_pairs(PairDataset(self.rows,self.vocab,16,16).items)
        source,target=batch["source"],batch["target"][:,:-1]
        output=model(source,target)
        self.assertEqual(tuple(output.shape),(2,target.size(1),cfg.target_vocab_size))
        altered=target.clone(); altered[:,-1]=BOS
        torch.testing.assert_close(output[:,:-1],model(source,altered)[:,:-1],rtol=1e-5,atol=1e-6)
        output.square().mean().backward()
        self.assertTrue(all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None))

    def test_reference_parameter_count(self):
        model=BrailleTransformer(ModelConfig(68,243))
        self.assertEqual(sum(p.numel() for p in model.parameters()),5672691)
        self.assertEqual(sum(p.numel() for p in model.encoder.layers[0].parameters()),789760)
        self.assertEqual(sum(p.numel() for p in model.decoder.layers[0].parameters()),1053440)

    def test_edit_distance(self):
        self.assertEqual(edit_distance("abc","adc"),1)
        self.assertEqual(edit_distance("","가"),1)

if __name__ == "__main__": unittest.main()

# DeepSeek-R1-Distill investigation
Status: **Planned — not run**

Official source: https://github.com/deepseek-ai/DeepSeek-R1

Start by selecting an exact checkpoint, such as DeepSeek-R1-Distill-Qwen-1.5B or a larger variant if the available hardware supports it. The distilled models and the original large R1 model are different artifacts; record the exact identity in all reports.

Planned steps:
- [ ] Read the model card, paper and checkpoint-specific terms.
- [ ] Record upstream revision and the inference framework.
- [ ] Run fixed test inputs and collect a baseline.
- [ ] Compare precision/quantization or inference configuration.
- [ ] If justified, test an adapter/fine-tuning change on a separate training split.
- [ ] Compare answer quality, latency, peak memory and failure cases.
- [ ] Record exactly what changed: prompt, inference configuration, weights or code.

Do not commit model weights or private datasets here. Keep source links and reproducible download/run instructions instead.

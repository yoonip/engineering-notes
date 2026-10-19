"""Export a trained 64-50-10 MLP to fixed-resistor circuit examples.

Run with the bundled Python or a Python environment containing NumPy and Pillow:
    python export_circuit.py
    ngspice -b circuit_sample_00008.cir
    python export_circuit.py --parse-ngspice ngspice_sample_00008_logits.txt

This exporter executes Python equations and writes unexecuted SPICE decks. It
does not program memristors, design transistors, or run a simulator. Amplifiers,
normalization, bias addition and activation are ideal behavioral elements.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import platform
import shutil
import time

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
EXPORTS = ROOT / "circuit_exports"
PWL_ROOT = ROOT / "pwl"
GMIN = 1e-6
GMAX = 100e-6
STATES = 64
GAIN = 1e8
RF = 1e3
SX = 0.1
SH = 0.01
SZ = 0.01
SAMPLE_TIME = 8e-6


def number(value):
    """17 significant digits preserve the Python mapping in both netlists."""
    return format(float(value), ".17g")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n",
                          encoding="utf-8")


def load_inputs(directory):
    model_path, inputs_path = directory / "model.npz", directory / "inputs.npz"
    if not model_path.exists() or not inputs_path.exists():
        raise FileNotFoundError("Run prepare_demo.py first: model.npz and inputs.npz are required.")
    with np.load(model_path, allow_pickle=False) as source:
        model = {key: np.asarray(source[key], dtype=np.float64) for key in ("w1", "b1", "w2", "b2")}
    with np.load(inputs_path, allow_pickle=False) as source:
        x = np.asarray(source["x_test"], dtype=np.float64)
        y = np.asarray(source["y_test"], dtype=np.int64)
    for key, shape in {"w1": (64, 50), "b1": (50,), "w2": (50, 10), "b2": (10,)}.items():
        if model[key].shape != shape:
            raise ValueError(f"{key} must have shape {shape}, received {model[key].shape}")
        if not np.isfinite(model[key]).all():
            raise ValueError(f"{key} contains non-finite values")
    if x.ndim != 2 or x.shape[1] != 64 or y.shape != (len(x),):
        raise ValueError("Expected x_test shape (N,64) and y_test shape (N,)")
    if not np.isfinite(x).all() or np.any(x < 0) or np.any(x > 1):
        raise ValueError("Expected finite normalized pixels in [0,1]")
    if np.any(y < 0) or np.any(y > 9):
        raise ValueError("Expected digit labels from 0 through 9")
    return model, x, y, model_path, inputs_path


def map_layer(weights):
    """Affine split-magnitude mapping with round-half-up to 64 cell states.

    Both physical cells have positive conductance. A signed coefficient is
    reconstructed as (G_plus-G_minus)/kg. No negative resistance is used.
    """
    weights = np.asarray(weights, dtype=np.float64)
    wmax = float(np.max(np.abs(weights)))
    # The all-zero corner needs a defined normalization despite zero wmax.
    reference_wmax = wmax if wmax > 0 else 1.0
    kg = (GMAX - GMIN) / reference_wmax
    raw_code = np.abs(weights) / reference_wmax * (STATES - 1)
    magnitude_code = np.clip(np.floor(raw_code + 0.5), 0, STATES - 1).astype(np.int64)
    plus_code = np.where(weights > 0, magnitude_code, 0)
    minus_code = np.where(weights < 0, magnitude_code, 0)
    conductance_step = (GMAX - GMIN) / (STATES - 1)
    gp = GMIN + conductance_step * plus_code
    gm = GMIN + conductance_step * minus_code
    # This signed-code expression avoids subtractive cancellation at zero.
    wq = (plus_code - minus_code) * reference_wmax / (STATES - 1)
    recovered = (gp - gm) / kg
    if not np.allclose(recovered, wq, atol=1e-14, rtol=1e-13):
        raise ArithmeticError("Conductance mapping did not reconstruct quantized weights")
    return {"weight_float": weights, "weight_quantized": wq,
            "plus_code": plus_code, "minus_code": minus_code,
            "G_plus": gp, "G_minus": gm, "R_plus": 1.0 / gp, "R_minus": 1.0 / gm,
            "wmax": wmax, "reference_wmax": reference_wmax, "kg": kg,
            "conductance_step": conductance_step}


def ideal_forward(x, w1, b1, w2, b2):
    hidden_pre = x @ w1 + b1
    hidden = np.maximum(hidden_pre, 0.0)
    logits = hidden @ w2 + b2
    return hidden_pre, hidden, logits


def tia_output(row_voltage, conductance):
    """Independent column KCL solution; no virtual-ground approximation.

    Vout = -A*(Vin @ G)/(sum_i G_i + (1+A)/Rf), since Vout=-A*Vsum.
    Each column has its own denominator and therefore its own loading error.
    """
    return -GAIN * (row_voltage @ conductance) / (
        conductance.sum(axis=0) + (1.0 + GAIN) / RF)


def finite_gain_forward(x, layers, b1, b2):
    first, second = layers
    p1, m1 = tia_output(SX * x, first["G_plus"]), tia_output(SX * x, first["G_minus"])
    hidden_pre = (m1 - p1) / (RF * SX * first["kg"]) + b1
    hidden = np.maximum(hidden_pre, 0.0)
    p2, m2 = tia_output(SH * hidden, second["G_plus"]), tia_output(SH * hidden, second["G_minus"])
    logits = (m2 - p2) / (RF * SH * second["kg"]) + b2
    return {"hidden_pre": hidden_pre, "hidden": hidden, "logits": logits,
            "layer1_tia_plus_V": p1, "layer1_tia_minus_V": m1,
            "layer2_tia_plus_V": p2, "layer2_tia_minus_V": m2}


def kcl_residual(row_voltage, conductance, output_voltage):
    summing_voltage = -output_voltage / GAIN
    residual = (summing_voltage * conductance.sum(axis=0)
                - row_voltage @ conductance + (summing_voltage - output_voltage) / RF)
    return float(np.max(np.abs(residual)))


def save_mappings(layers, model):
    EXPORTS.mkdir(parents=True, exist_ok=True)
    values = {"b1": model["b1"], "b2": model["b2"], "Gmin_S": GMIN,
              "Gmax_S": GMAX, "states_per_device": STATES}
    with (EXPORTS / "mapped_weights.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(["layer", "row", "logical_column", "weight_float", "weight_quantized",
                         "code_plus", "code_minus", "G_plus_S", "G_minus_S", "R_plus_ohm", "R_minus_ohm"])
        for layer_id, layer in enumerate(layers, start=1):
            prefix = f"layer{layer_id}_"
            for key in ("weight_float", "weight_quantized", "plus_code", "minus_code",
                        "G_plus", "G_minus", "R_plus", "R_minus", "wmax", "reference_wmax", "kg"):
                values[prefix + key] = layer[key]
            for key in ("G_plus", "G_minus", "R_plus", "R_minus"):
                unit = "S" if key.startswith("G_") else "ohm"
                np.savetxt(EXPORTS / f"layer{layer_id}_{key}_{unit}.csv", layer[key], delimiter=",", fmt="%.17g")
            for row, col in np.ndindex(layer["weight_float"].shape):
                writer.writerow([layer_id, row, col, layer["weight_float"][row, col],
                                 layer["weight_quantized"][row, col], layer["plus_code"][row, col],
                                 layer["minus_code"][row, col], layer["G_plus"][row, col],
                                 layer["G_minus"][row, col], layer["R_plus"][row, col],
                                 layer["R_minus"][row, col]])
    np.savez(EXPORTS / "conductance_mapping.npz", **values)


def write_neuron_model():
    model = r'''// Ideal behavioral neuron, not a transistor-level implementation.
// Inputs are the two column TIA output voltages; their negative sign is corrected.
`include "constants.vams"
`include "disciplines.vams"
module normalized_neuron(tia_plus, tia_minus, out);
    input tia_plus, tia_minus;
    output out;
    electrical tia_plus, tia_minus, out;
    parameter real rf = 1000.0;
    parameter real input_scale = 0.1;
    parameter real conductance_per_weight = 1.0e-4;
    parameter real output_scale = 0.01;
    parameter real bias = 0.0;
    parameter integer rectify = 1;
    real preactivation;
    analog begin
        preactivation = (V(tia_minus)-V(tia_plus)) /
                        (rf*input_scale*conductance_per_weight) + bias;
        if ((rectify != 0) && (preactivation < 0.0))
            V(out) <+ 0.0;
        else
            V(out) <+ output_scale*preactivation;
    end
endmodule
'''
    (ROOT / "neuron.va").write_text(model, encoding="ascii")


def write_pwl(index, x):
    folder = PWL_ROOT / f"sample_{index:05d}"
    folder.mkdir(parents=True, exist_ok=True)
    times = np.array([0, 1e-6, 1.1e-6, 9e-6, 9.1e-6, 10e-6])
    for row, pixel in enumerate(x):
        values = np.array([0, 0, SX * pixel, SX * pixel, 0, 0])
        np.savetxt(folder / f"pixel_{row:02d}.pwl", np.column_stack([times, values]), fmt="%.17g")
    np.savetxt(EXPORTS / f"sample_{index:05d}_pixels.csv", x.reshape(8, 8), delimiter=",", fmt="%.17g")
    image = Image.fromarray(np.floor(x.reshape(8, 8) * 255 + 0.5).astype(np.uint8))
    image.resize((320, 320), Image.Resampling.NEAREST).save(EXPORTS / f"sample_{index:05d}_8x8.png")


def pwl_inline(pixel):
    voltage = number(SX * pixel)
    return f"0 0 1u 0 1.1u {voltage} 9u {voltage} 9.1u 0 10u 0"


def layer_nodes(layer_id, col, sign):
    return f"l{layer_id}_{sign}sum_{col}", f"l{layer_id}_{sign}out_{col}"


def append_ngspice_layer(lines, layer_id, rows, layer, biases, input_scale, output_scale, rectified):
    ncols = len(biases)
    lines.append(f"* Layer {layer_id}: {len(rows)} rows, {2*ncols} physical columns, {ncols} logical outputs")
    for col in range(ncols):
        for sign, key in (("p", "R_plus"), ("m", "R_minus")):
            summing, output = layer_nodes(layer_id, col, sign)
            for row, input_node in enumerate(rows):
                lines.append(f"R_L{layer_id}_{sign}_{row}_{col} {input_node} {summing} {number(layer[key][row,col])}")
            # E out 0 0 sum A means V(out)=-A*V(sum).
            lines.append(f"E_TIA_L{layer_id}_{sign}_{col} {output} 0 0 {summing} {number(GAIN)}")
            lines.append(f"R_FB_L{layer_id}_{sign}_{col} {output} {summing} {number(RF)}")
        plus = layer_nodes(layer_id, col, "p")[1]
        minus = layer_nodes(layer_id, col, "m")[1]
        output_node = f"hidden_{col}" if rectified else f"logit_{col}"
        denom = RF * input_scale * layer["kg"]
        pre = f"((V({minus})-V({plus}))/{number(denom)}+({number(biases[col])}))"
        expression = f"max({pre},0)" if rectified else pre
        lines.append(f"B_NEURON_L{layer_id}_{col} {output_node} 0 V={{{number(output_scale)}*{expression}}}")


def write_ngspice(index, x, layers, model):
    path = ROOT / f"circuit_sample_{index:05d}.cir"
    lines = [f"Fixed-resistor 64-50-10 MLP, fixed MNIST test index {index}",
             "* Generated by export_circuit.py. This deck has not been run by the exporter.",
             "* 64 device conductance states, positive resistors, signed differential columns.",
             "* Ideal finite-gain VCVS TIA; ideal behavioral bias, scaling, ReLU and output.",
             "* No transistor model, memristor dynamics, programming pulses or extracted parasitics.",
             "* hidden voltage = 0.01*activation; output voltage = 0.01*dimensionless logit.",
             ".options reltol=1e-6 abstol=1e-12 vntol=1e-9"]
    for row, pixel in enumerate(x):
        lines.append(f"V_PIXEL_{row} pixel_{row} 0 PWL({pwl_inline(pixel)})")
    append_ngspice_layer(lines, 1, [f"pixel_{i}" for i in range(64)], layers[0], model["b1"], SX, SH, True)
    append_ngspice_layer(lines, 2, [f"hidden_{i}" for i in range(50)], layers[1], model["b2"], SH, SZ, False)
    outputs = " ".join(f"v(logit_{col})" for col in range(10))
    lines += [f".save {outputs}", ".tran 10n 10u 0 10n"]
    for col in range(10):
        lines.append(f".measure tran logit_{col}_V find v(logit_{col}) at=8u")
    lines += [".control", "set wr_vecnames", "set wr_singlescale", "set numdgt=17", "run",
              f"wrdata ngspice_sample_{index:05d}_logits.txt {outputs}", ".endc", ".end"]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")
    return path


def append_spectre_layer(lines, layer_id, rows, layer, biases, input_scale, output_scale, rectified):
    lines.append(f"// Layer {layer_id}: {len(rows)} rows, {2*len(biases)} physical columns")
    for col in range(len(biases)):
        for sign, key in (("p", "R_plus"), ("m", "R_minus")):
            summing, output = layer_nodes(layer_id, col, sign)
            for row, input_node in enumerate(rows):
                lines.append(f"R_L{layer_id}_{sign}_{row}_{col} ({input_node} {summing}) resistor r={number(layer[key][row,col])}")
            lines.append(f"E_TIA_L{layer_id}_{sign}_{col} ({output} 0 0 {summing}) vcvs gain={number(GAIN)}")
            lines.append(f"R_FB_L{layer_id}_{sign}_{col} ({output} {summing}) resistor r={number(RF)}")
        plus, minus = layer_nodes(layer_id, col, "p")[1], layer_nodes(layer_id, col, "m")[1]
        output_node = f"hidden_{col}" if rectified else f"logit_{col}"
        lines.append(f"N_L{layer_id}_{col} ({plus} {minus} {output_node}) normalized_neuron "
                     f"rf={number(RF)} input_scale={number(input_scale)} "
                     f"conductance_per_weight={number(layer['kg'])} output_scale={number(output_scale)} "
                     f"bias={number(biases[col])} rectify={int(rectified)}")


def write_spectre(index, x, layers, model):
    path = ROOT / f"circuit_sample_{index:05d}.scs"
    lines = ["simulator lang=spectre", "global 0",
             f"// Fixed MNIST test index {index}. Generated deck; not executed by this exporter.",
             "// Fixed positive resistor weights; ideal VCVS TIA and Verilog-A neuron.",
             "// No transistor-level opamp or programmable memristor implementation is claimed.",
             'ahdl_include "neuron.va"',
             "simulatorOptions options reltol=1e-6 vabstol=1e-9 iabstol=1e-12 temp=27"]
    for row, pixel in enumerate(x):
        lines.append(f"V_PIXEL_{row} (pixel_{row} 0) vsource type=pwl wave=[{pwl_inline(pixel)}]")
    append_spectre_layer(lines, 1, [f"pixel_{i}" for i in range(64)], layers[0], model["b1"], SX, SH, True)
    append_spectre_layer(lines, 2, [f"hidden_{i}" for i in range(50)], layers[1], model["b2"], SH, SZ, False)
    lines += ["tran1 tran stop=10u maxstep=10n errpreset=conservative",
              "save " + " ".join(f"logit_{col}" for col in range(10))]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")
    return path


def parse_ngspice_export(path, sample_result, destination):
    """Read wrdata's one shared time column plus ten voltage columns.

    This parser never executes a simulator. The exporting run must be performed
    separately. Header lines are skipped; malformed numeric rows are rejected.
    """
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if not fields:
            continue
        try:
            float(fields[0])
        except ValueError:
            continue
        try:
            row = [float(item) for item in fields]
        except ValueError as exc:
            raise ValueError("Malformed numeric wrdata row") from exc
        if len(row) != 11:
            raise ValueError(f"Expected time + 10 voltages (11 columns), found {len(row)}. "
                             "Use set wr_singlescale in the generated deck.")
        rows.append(row)
    data = np.asarray(rows, dtype=np.float64)
    if data.ndim != 2 or len(data) < 2 or data.shape[1] != 11 or not np.isfinite(data).all():
        raise ValueError("No valid finite waveform data found")
    if np.any(np.diff(data[:, 0]) < 0) or data[0, 0] > SAMPLE_TIME or data[-1, 0] < SAMPLE_TIME:
        raise ValueError("Waveforms must have increasing time and cover 8 microseconds")
    output_voltages = np.array([np.interp(SAMPLE_TIME, data[:, 0], data[:, col + 1]) for col in range(10)])
    output_logits = output_voltages / SZ
    ideal = np.asarray(sample_result["quantized_ideal_logits"])
    finite = np.asarray(sample_result["python_finite_gain_logits"])
    result = {
        "execution_kind": "Parsed supplied ngspice wrdata export; parser did not launch SPICE",
        "input_waveform": str(Path(path).resolve()), "waveform_sha256": sha256(path),
        "sample_index": sample_result["sample_index"], "sample_true_label": sample_result["sample_true_label"],
        "sampling_time_s": SAMPLE_TIME, "output_voltage_per_logit_V": SZ,
        "sampled_output_voltages_V": output_voltages.tolist(), "sampled_dimensionless_logits": output_logits.tolist(),
        "prediction": int(output_logits.argmax()),
        "max_absolute_error_vs_quantized_ideal": float(np.max(np.abs(output_logits - ideal))),
        "max_absolute_error_vs_python_finite_gain": float(np.max(np.abs(output_logits - finite))),
        "numeric_rows": len(data),
    }
    write_json(destination, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parse-ngspice", type=Path, default=None,
                        help="Optional existing ngspice wrdata waveform file; simulator is never launched")
    parser.add_argument("--parse-index", type=int, default=None,
                        help="Test index associated with supplied waveform; default first test label 5")
    args = parser.parse_args()
    start = time.perf_counter()
    model, x, y, model_path, inputs_path = load_inputs(ROOT)
    five_indices = np.flatnonzero(y == 5)
    if len(five_indices) < 2:
        raise ValueError("Expected at least two true-label-5 test samples for the predetermined demonstration")
    # Predetermined rule: first TWO true-label-5 samples; never filter predictions.
    indices = [int(five_indices[0]), int(five_indices[1])]
    layers = [map_layer(model["w1"]), map_layer(model["w2"])]
    save_mappings(layers, model)
    write_neuron_model()
    fp_pre, fp_hidden, fp_logits = ideal_forward(x, **model)
    q_pre, q_hidden, q_logits = ideal_forward(x, layers[0]["weight_quantized"], model["b1"],
                                            layers[1]["weight_quantized"], model["b2"])
    finite = finite_gain_forward(x, layers, model["b1"], model["b2"])
    np.savez(EXPORTS / "test_inference.npz", y_test=y, floating_logits=fp_logits,
             quantized_logits=q_logits, finite_gain_logits=finite["logits"], sample_indices=indices)
    samples = []
    for index in indices:
        write_pwl(index, x[index])
        cir = write_ngspice(index, x[index], layers, model)
        scs = write_spectre(index, x[index], layers, model)
        selected = {key: np.asarray(value[index]) for key, value in finite.items()}
        residuals = [
            kcl_residual(SX * x[index], layers[0]["G_plus"], selected["layer1_tia_plus_V"]),
            kcl_residual(SX * x[index], layers[0]["G_minus"], selected["layer1_tia_minus_V"]),
            kcl_residual(SH * selected["hidden"], layers[1]["G_plus"], selected["layer2_tia_plus_V"]),
            kcl_residual(SH * selected["hidden"], layers[1]["G_minus"], selected["layer2_tia_minus_V"]),
        ]
        sample = {
            "execution_kind": "executed Python finite-gain circuit equations, not SPICE",
            "sample_rule": "first two test samples whose true label is 5; prediction was not used for selection",
            "sample_index": index, "sample_true_label": int(y[index]),
            "floating_model_prediction": int(fp_logits[index].argmax()),
            "quantized_ideal_prediction": int(q_logits[index].argmax()),
            "python_finite_gain_prediction": int(selected["logits"].argmax()),
            "floating_logits": fp_logits[index].tolist(), "floating_hidden": fp_hidden[index].tolist(),
            "quantized_ideal_logits": q_logits[index].tolist(),
            "quantized_ideal_hidden_preactivation": q_pre[index].tolist(), "quantized_ideal_hidden": q_hidden[index].tolist(),
            "python_finite_gain_logits": selected["logits"].tolist(),
            "python_finite_gain_hidden_preactivation": selected["hidden_pre"].tolist(),
            "python_finite_gain_hidden": selected["hidden"].tolist(),
            "expected_output_voltages_V": (SZ * selected["logits"]).tolist(),
            "max_absolute_logit_error_finite_vs_quantized_ideal": float(np.max(np.abs(selected["logits"] - q_logits[index]))),
            "max_absolute_logit_change_quantized_vs_float": float(np.max(np.abs(q_logits[index] - fp_logits[index]))),
            "kcl_max_absolute_residual_A": max(residuals),
            "ngspice_deck": cir.name, "spectre_deck": scs.name,
            "ngspice_deck_sha256": sha256(cir), "spectre_deck_sha256": sha256(scs),
            "SPICE_execution_status": "not executed by exporter",
        }
        np.savez(EXPORTS / f"sample_{index:05d}_expected.npz", x=x[index], y=y[index],
                 floating_logits=fp_logits[index], floating_hidden=fp_hidden[index],
                 quantized_logits=q_logits[index], quantized_hidden=q_hidden[index], **selected)
        with (EXPORTS / f"sample_{index:05d}_logits.csv").open("w", newline="", encoding="utf-8") as target:
            writer = csv.writer(target)
            writer.writerow(["class", "floating_logit", "quantized_ideal_logit", "python_finite_gain_logit", "expected_voltage_V"])
            for digit in range(10):
                writer.writerow([digit, fp_logits[index,digit], q_logits[index,digit],
                                 selected["logits"][digit], SZ * selected["logits"][digit]])
        write_json(ROOT / f"circuit_sample_{index:05d}_results.json", sample)
        samples.append(sample)
    # The default remains the first fixed sample even if it is misclassified.
    shutil.copyfile(ROOT / f"circuit_sample_{indices[0]:05d}.cir", ROOT / "network.cir")
    shutil.copyfile(ROOT / f"circuit_sample_{indices[0]:05d}.scs", ROOT / "network.scs")
    results = {
        "execution_kind": "executed Python finite-gain circuit equations, not SPICE",
        "python": platform.python_version(), "numpy": np.__version__,
        "architecture": "64-50-10 MLP; ReLU hidden; linear output; floating biases",
        "input_order": "8x8 row-major flattened pixel order",
        "mapping": "Gplus=Gmin+step*positive_code; Gminus=Gmin+step*negative_code; Wq=(Gplus-Gminus)/kg",
        "quantization": "round-half-up magnitudes floor(abs(W)/wmax*63+0.5), 64 states per positive device",
        "possible_signed_weight_values": 127, "Gmin_S": GMIN, "Gmax_S": GMAX,
        "states_per_device": STATES,
        "layer_mapping": [{"layer": i+1, "wmax": layer["wmax"], "kg_S_per_weight": layer["kg"],
                           "physical_array_shape": [layer["weight_float"].shape[0], 2*layer["weight_float"].shape[1]]}
                          for i, layer in enumerate(layers)],
        "physical_weight_resistor_count": 7400, "TIA_count": 120, "feedback_resistor_count": 120,
        "TIA_open_loop_gain": GAIN, "feedback_resistance_ohm": RF,
        "input_voltage_per_normalized_pixel_V": SX,
        "hidden_voltage_per_dimensionless_activation_V": SH, "output_voltage_per_dimensionless_logit_V": SZ,
        "pwl_time_s": [0, 1e-6, 1.1e-6, 9e-6, 9.1e-6, 10e-6],
        "read_time_s": SAMPLE_TIME, "SPICE_execution_status": "decks generated only; not executed by exporter",
        "hardware_scope": "fixed linear resistors plus ideal VCVS amplifiers and ideal behavioral neurons; no memristor programming or transistor design",
        "static_equations_only": True,
        "floating_test_accuracy": float(np.mean(fp_logits.argmax(axis=1) == y)),
        "quantized_ideal_test_accuracy": float(np.mean(q_logits.argmax(axis=1) == y)),
        "python_finite_gain_test_accuracy": float(np.mean(finite["logits"].argmax(axis=1) == y)),
        "test_count": len(y),
        "max_absolute_logit_error_finite_vs_quantized_ideal_full_test": float(np.max(np.abs(finite["logits"]-q_logits))),
        "model_sha256": sha256(model_path), "inputs_sha256": sha256(inputs_path), "neuron_va_sha256": sha256(ROOT / "neuron.va"),
        "sample_rule": "first two test label-5 samples, independent of model prediction", "default_sample_index": indices[0],
        "samples": samples, "duration_seconds": time.perf_counter() - start,
    }
    if args.parse_ngspice is not None:
        parse_index = indices[0] if args.parse_index is None else args.parse_index
        selected_sample = next((sample for sample in samples if sample["sample_index"] == parse_index), None)
        if selected_sample is None:
            raise ValueError("--parse-index must select one of the two predetermined samples")
        parsed = parse_ngspice_export(args.parse_ngspice, selected_sample,
                                     ROOT / f"ngspice_sample_{parse_index:05d}_parsed.json")
        results["parsed_external_ngspice_export"] = parsed
    write_json(ROOT / "circuit_export_results.json", results)
    print(json.dumps({"execution_kind": results["execution_kind"],
                      "quantized_test_accuracy": results["quantized_ideal_test_accuracy"],
                      "finite_gain_test_accuracy": results["python_finite_gain_test_accuracy"],
                      "samples": [{key: sample[key] for key in ("sample_index", "sample_true_label",
                                  "floating_model_prediction", "quantized_ideal_prediction",
                                  "python_finite_gain_prediction")} for sample in samples]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

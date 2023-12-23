import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.style as style
import numpy as np
from tqdm import tqdm

style.use("seaborn-poster")  # sets the size of the charts
style.use("ggplot")


def get_args():
    parser = argparse.ArgumentParser("Evaluate COCO bounding box results.")
    parser.add_argument(
        "--gt-json", type=str, required=True, help="Path to ground truth json file."
    )
    parser.add_argument(
        "--pred-json", type=str, required=True, help="Path to predicted json file."
    )
    parser.add_argument(
        "--output-dir", type=str, required=True, help="Path to output directory."
    )
    parser.add_argument(
        "--tp-distance",
        type=int,
        default=20,
        help="Distance pixel threshold for true positives.",
    )
    return parser.parse_args()


def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data


def calculate_f1(tp, fp, fn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    return f1


def calculate_tp_fp_fn(gt_json, pred_anns, tp_distance):
    tp = 0
    fp = 0
    fn = 0
    ann_to_img_map = {img["id"]: [] for img in gt_json["images"]}
    for ann in pred_anns:
        ann_to_img_map[ann["image_id"]].append(ann)

    gt_to_img_map = {img["id"]: [] for img in gt_json["images"]}
    for ann in gt_json["annotations"]:
        gt_to_img_map[ann["image_id"]].append(ann)

    for img_id, gt_anns in gt_to_img_map.items():
        frame_anns = ann_to_img_map[img_id]
        gt_matches = np.array([False for _ in gt_anns])
        pred_matches = np.array([False for _ in frame_anns])

        if len(frame_anns) > 0:
            for i, (gt_matched, gt_ann) in enumerate(zip(gt_matches, gt_anns)):
                gt_mid_x = gt_ann["bbox"][0] + gt_ann["bbox"][2] / 2
                gt_mid_y = gt_ann["bbox"][1] + gt_ann["bbox"][3] / 2
                pred_dists = []

                for j, (pred_matched, pred_ann) in enumerate(
                    zip(pred_matches, frame_anns)
                ):
                    pred_mid_x = pred_ann["bbox"][0] + pred_ann["bbox"][2] / 2
                    pred_mid_y = pred_ann["bbox"][1] + pred_ann["bbox"][3] / 2

                    dist = (
                        (pred_mid_x - gt_mid_x) ** 2 + (pred_mid_y - gt_mid_y) ** 2
                    ) ** 0.5
                    pred_dists.append(dist)

                min_idx = np.argmin(pred_dists)
                if not pred_matches[min_idx] and pred_dists[min_idx] <= tp_distance:
                    tp += 1
                    pred_matches[min_idx] = True
                    gt_matches[i] = True

        fp += np.size(pred_matches) - np.count_nonzero(pred_matches)
        fn += np.size(gt_matches) - np.count_nonzero(gt_matches)

    return tp, fp, fn


def get_detection_per_conv(pred_json, convs):
    detections = {conv: [] for conv in convs}
    for ann in pred_json:
        pred_conv = ann["score"]
        for conv in convs:
            if pred_conv >= conv:
                detections[conv].append(ann)

    return detections


def plot_f1_curve(confs, scores, output_dir, plot_name="f1_curve.png"):
    max_score = np.argmax(scores)
    plt.plot(
        confs,
        scores,
        label=f"Max F1: {scores[max_score]:.4f} at {confs[max_score]:.2f}",
    )
    plt.xlabel("Confidence")
    plt.ylabel("F1 Score")
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    plt.legend()
    plt.savefig(output_dir / plot_name)
    plt.show()


def main(args):
    gt_json = load_json(args.gt_json)
    pred_json = load_json(args.pred_json)

    conf_detections = get_detection_per_conv(pred_json, np.linspace(0, 1.0, num=100))

    conf_f1_scores = {}
    conf_stats = {}
    for conf, detections in tqdm(conf_detections.items(), desc="Calculating F1 Scores"):
        if len(detections) <= 0:
            conf_f1_scores[conf] = 0
            conf_stats[conf] = {"tp": -1, "fp": -1, "fn": -1, "f1": 0}
            break

        try:
            tp, fp, fn = calculate_tp_fp_fn(gt_json, detections, args.tp_distance)
            f1 = calculate_f1(tp, fp, fn)
        except ZeroDivisionError:
            f1 = 0
        # print(f"Confidence: {conf}, F1: {f1}, No detections: {len(detections)}")
        conf_f1_scores[conf] = f1
        conf_stats[conf] = {"tp": tp, "fp": fp, "fn": fn, "f1": f1}

    max_conv = max(conf_f1_scores, key=conf_f1_scores.get)
    max_score = conf_f1_scores[max_conv]

    stats = conf_stats[max_conv]
    print(
        f"gt_json: {len(gt_json['annotations'])}, pred_json: {len(conf_detections[max_conv])}"
    )
    print(f"tp: {stats['tp']}, fp: {stats['fp']}, fn: {stats['fn']}")
    print(f"f1: {max_score} at confidence {max_conv:.2f}")

    plot_f1_curve(
        list(conf_f1_scores.keys()),
        list(conf_f1_scores.values()),
        Path(args.output_dir),
        plot_name=f"f1_curve_{args.tp_distance}.png",
    )

    with open(Path(args.output_dir) / f"f1_stats_{args.tp_distance}.json", "w") as f:
        json.dump(conf_stats, f)


if __name__ == "__main__":
    args = get_args()
    main(args)

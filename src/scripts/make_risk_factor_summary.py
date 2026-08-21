import pandas as pd
import dataframe_image as dfi
from pathlib import Path


def make_risk_factor_summary() -> None:
    risk_factor_summary = pd.DataFrame({
        "Feature": [
            "Revolving utilization",
            "Age",
            "30-59 DPD",
            "60-89 DPD",
            "90+ DPD",
            "Debt ratio",
            "Income",
            "Open credit lines",
            "Real-estate loans",
            "Dependents"
        ],
        "Cramer's V": [0.303, 0.113, 0.278, 0.282, 0.350, 0.062, 0.073, 0.099, 0.062, 0.047],
        "Main pattern": [
            "Сильная нелинейная градация уровня риска между сегментами." ,
            "Риск в среднем в 1.57% раза выше у молодых людей - (22-45] лет.",
            "Риск быстро возрастает у людей, имеющих просрочки.",
            "Риск быстро возрастает у людей, имеющих просрочки. Сильная градация риска между сегментами.",
            "Риск быстро возрастает у людей, имеющих просрочки. Сильная градация риска между сегментами.",
            "Риск возрастает у людей с высоким Ratio - (0.7-4.0].",
            "У людей с низким-средним доходом ((900-4500]) несколько выше - 1.39 раза в среднем.",
            "Высокий риск у людей, не имевших кредитов на момент скоринга.",
            "Слабая нелинейная связь.",
            "Слабая нелинейная связь."
        ],
        "Main risk segments": [
            "(0.7, 1.0]\n(1.0, 2.0]",
            "(22.0, 30.0]\n(30.0, 45.0]",
            "[1, 2]\n(2, 13]",
            "[1, 2]\n(2, 11]",
            "[1, 2]\n(2, 17]",
            "(0.7, 1.0]\n(1.0, 4.0]",
            "(900.0, 3000.0]\n(3000.0, 4500.0]",
            "0",
            "0",
            "(2, 20]"
        ],
        "Dataset share": [
            "17.75\n1.97", 
            "6.67\n23.03",
            "13.75\n2.05",
            "4.57\n0.32",
            "4.53\n0.85",
            "4.89\n3.50",
            "13.92\n15.17",
            "1.26",
            "37.46",
            "8.89"
        ],
        "Bad share" : [
            "47.05\n11.80",
            "11.92\n37.65",
            "36.19\n12.07",
            "23.32\n2.84",
            "25.34\n7.82",
            "8.17\n6.36",
            "20.73\n19.58",
            "4.83",
            "46.6",
            "12.30"
        ],
        "BR": [
            "17.72\n40.10",
            "11.79\n9.31",
            "17.59\n39.26",
            "34.14\n58.64",
            "37.38\n61.68",
            "11.15\n12.16",
            "9.95\n8.63",
            "25.64",
            "8.31",
            "9.25"
        ],
        "Lift": [
            "2.65\n5.99",
            "1.76\n1.39",
            "2.63\n5.87",
            "5.11\n8.77",
            "5.59\n9.23",
            "1.67\n1.82",
            "1.49\n1.29",
            "3.84",
            "1.24",
            "1.38"
        ],
        "Dataset relevance": [
            "Very\nHigh",
            "Very\nNormal",
            "Very\nHigh",
            "High",
            "High",
            "Very\nNormal",
            "Normal",
            "Low",
            "Normal",
            "Low"
        ],
        "Dataset relevance num": [
            5, 3, 5, 4, 4, 3, 2, 1, 2, 1
        ]
    })

    risk_factor_summary = (
        risk_factor_summary
        .sort_values(by="Dataset relevance num", ascending=False)
        .drop(columns="Dataset relevance num")
    )
    risk_factor_summary = (
        risk_factor_summary
        .style
        .set_properties(
            **{
                "text-align": "left",
                "white-space": "pre-wrap"
            }
        )
        .set_table_styles(
            [{
                "selector": "th.col_heading",
                "props": [("text-align", "center")]
            }]
        )
    )

    out_path = Path("../docs/risk_analysis/risk_factor_summary.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dfi.export(risk_factor_summary, out_path, table_conversion="matplotlib")
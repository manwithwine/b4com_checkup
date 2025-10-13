"""
HTML шаблоны для генерации отчетов B4COM Checkup System
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B4COM Checkup Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        small {{
            font-size: 0.8em;
            opacity: 0.7;
            font-weight: normal;
        }}

        .container {{
            max-width: 95%;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}

        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .summary {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .summary-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .summary-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}

        .summary-label {{
            font-size: 0.9em;
            color: #6c757d;
            margin-top: 5px;
        }}

        .table-container {{
            overflow-x: auto;
            padding: 20px;
            position: relative;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85em;
            min-width: 2000px;
        }}

        th {{
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: 600;
            position: sticky;
            top: 0;
            border: 1px solid #34495e;
            cursor: help;
            position: relative;
        }}

        th:hover {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        }}

        td {{
            padding: 8px;
            border: 1px solid #dee2e6;
            vertical-align: top;
            background: white;
        }}

        .threshold-row {{
            cursor: default;
        }}

        .threshold-row td {{
            background: #fff3cd;
            font-weight: bold;
            color: #856404;
            text-align: center;
        }}

        .threshold-row:hover td {{
            background: #ffeaa7;
        }}

        /* Кастомные подсказки ТОЛЬКО для заголовков метрик */
        th[data-tooltip] {{
            position: relative;
        }}

        th[data-tooltip]:hover::after {{
            content: attr(data-tooltip);
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 20px;
            border-radius: 10px;
            font-size: 0.9em;
            white-space: pre-line;
            max-width: 400px;
            z-index: 10000;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            line-height: 1.5;
            border: 2px solid rgba(255, 255, 255, 0.1);
            text-align: left;
        }}

        .device-row:hover td {{
            background: #f8f9fa;
            transform: translateY(-1px);
            transition: all 0.2s ease;
        }}

        .status-ok {{
            background: #d4edda !important;
            color: #155724;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
        }}

        .status-warning {{
            background: #fff3cd !important;
            color: #856404;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
        }}

        .status-alert {{
            background: #f8d7da !important;
            color: #721c24;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
        }}

        .metric-value {{
            font-weight: bold;
            color: #2c3e50;
        }}

        .metric-details {{
            font-size: 0.8em;
            color: #6c757d;
            margin-top: 2px;
        }}

        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 20px;
        }}

        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
        }}

        /* Анимация появления подсказок */
        th[data-tooltip]:hover::after {{
            animation: fadeIn 0.2s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translate(-50%, -40%); }}
            to {{ opacity: 1; transform: translate(-50%, -50%); }}
        }}

        /* Улучшенная прокрутка для таблицы */
        .table-container::-webkit-scrollbar {{
            height: 8px;
        }}

        .table-container::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}

        .table-container::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 4px;
        }}

        .table-container::-webkit-scrollbar-thumb:hover {{
            background: #a8a8a8;
        }}

        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 10px;
            }}

            .header h1 {{
                font-size: 2em;
            }}

            .table-container {{
                padding: 10px;
            }}

            /* Уменьшаем подсказки на мобильных */
            th[data-tooltip]:hover::after {{
                max-width: 90%;
                font-size: 0.8em;
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 B4COM Checkup Report</h1>
            <div class="subtitle">Comprehensive Network Device Health Analysis created by tg: @manwithwine</div>
        </div>

        <div class="summary">
            <h3>📈 Summary</h3>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-number">{devices_count}</div>
                    <div class="summary-label">Devices Checked</div>
                </div>
                <div class="summary-item">
                    <div class="summary-number">{healthy_count}</div>
                    <div class="summary-label">Healthy Devices</div>
                </div>
                <div class="summary-item">
                    <div class="summary-number">{warning_count}</div>
                    <div class="summary-label">Warnings</div>
                </div>
                <div class="summary-item">
                    <div class="summary-number">{alert_count}</div>
                    <div class="summary-label">Alerts</div>
                </div>
            </div>
        </div>

        <div class="table-container">
            {table_content}
        </div>

        <div class="footer">
            <div class="timestamp">Report generated on {timestamp}</div>
        </div>
    </div>
</body>
</html>
"""
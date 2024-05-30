import io
import os
from pathlib import Path
import dotenv
import time
import datetime as dt
from pandas import DataFrame
from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


dotenv_path = Path(__file__).parent.parent.joinpath(".env")
if os.path.exists(dotenv_path):
    dotenv.load_dotenv(dotenv_path)


class AppointmentsPDF:
    directory_path = os.getenv("APPOINTMENTS_PDF_PATH")

    # регистрация шрифта из папки со статиками
    pdfmetrics.registerFont(
        TTFont("DejaVuSans", "api/static/reportlab_fonts/DejaVuSans.ttf")
    )

    def generate_path(self) -> str:
        """returns name for pdf"""

        current_date = dt.datetime.now()  # datetime object with time
        current_date = current_date.date()  # cuts part of time
        return str(current_date) + "_appmnts.pdf"

    def unix_filename_generator(self):
        while True:
            timespamp = "_" + str(int(time.time())) + ".pdf"
            yield timespamp

    def create_report(self, file_path: str, data: DataFrame) -> dict:
        """
        creates pdf file in bytecode
        -------------------------------
        returns a dict with keys:

        "buffer": buffer,
        "file_name": file_path
        """

        gen = self.unix_filename_generator()
        # Проверяем свободно ли имя, если нет, то добавляем значение генератора
        if os.path.exists(file_path):
            file_path = file_path[: len(file_path) - 4] + next(gen)

        # Создаем байтовый буфер
        buffer = io.BytesIO()
        # Создаем pdf файл в байтовом буфере
        pdf = SimpleDocTemplate(buffer, pagesize=A3)
        elements = []

        # Преобразование DataFrame в список списков
        data = [data.columns.tolist()] + data.values.tolist()
        print(data)

        table = Table(data)
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans"),
                ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )

        table.setStyle(style)

        # Добавление таблицы в список элементов
        elements.append(table)

        # Сборка PDF-документа
        pdf.build(elements)

        buffer.seek(0)

        return {"buffer": buffer, "file_name": file_path}


appointments_pdf = AppointmentsPDF()
